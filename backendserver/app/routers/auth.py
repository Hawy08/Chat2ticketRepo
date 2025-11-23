from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from google_auth_oauthlib.flow import Flow
from app.core.config import settings
from app.core.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.booking import Booking
from app.models.event import Event
from app.models.oauth_session import OAuthSession
from app.services.google_service import (
    create_calendar_event,
    send_confirmation_email
)
from datetime import datetime, timedelta
import os
import secrets

router = APIRouter(prefix="/auth")

# Allow insecure transport for local testing (HTTP)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/gmail.send',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

@router.get("/google/login")
async def google_login(booking_id: int, redirect_url: str):
    """Initiates the Google OAuth flow."""
    
    # Create a Flow instance
    # Note: In a real app, client_config should be loaded securely, not hardcoded if possible.
    # Here we construct it from settings.
    
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    
    # Construct the redirect_uri dynamically
    # Ensure no trailing slash on base URL, and append callback path
    base_url = redirect_url.rstrip("/")
    callback_uri = f"{base_url}/auth/google/callback"
    
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=callback_uri
    )
    
    # Generate the authorization URL
    # Pass booking_id in state so we know which booking to process on callback
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=str(booking_id)
    )
    
    return {"url": authorization_url}


@router.post("/google/login/whatsapp")
async def google_login_whatsapp(
    whatsapp_user_id: str = Query(
        ..., description="WhatsApp user ID or phone number"
    ),
    booking_id: int = Query(None, description="Optional booking ID"),
    session: AsyncSession = Depends(get_session)
):
    """
    Generate Google Login Link (REQUIRED).
    
    Generates a Google OAuth link.
    **YOU MUST SEND THIS LINK TO THE USER** via WhatsApp so they can authorize access.
    This step is **REQUIRED** before you can send emails or create calendar events.
    """
    # Generate a unique state token
    state_token = secrets.token_urlsafe(32)
    
    # Create OAuth session record
    oauth_session = OAuthSession(
        whatsapp_user_id=whatsapp_user_id,
        state=state_token,
        status="pending",
        booking_id=booking_id
    )
    session.add(oauth_session)
    await session.commit()
    await session.refresh(oauth_session)
    
    # Create OAuth flow
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    
    # Ensure redirect URI matches exactly what's in Google Console
    callback_uri = settings.GOOGLE_REDIRECT_URI.rstrip('/')
    
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=callback_uri
    )
    
    # Generate authorization URL with our state token
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',  # Force consent to get refresh token
        state=state_token
    )
    
    return {
        "url": authorization_url,
        "state": state_token,
        "redirect_uri": callback_uri,  # For verification
        "message": (
            "Click this link to authorize Google access. "
            "After authorization, return to WhatsApp."
        )
    }

@router.get("/google/callback")
async def google_callback(
    request: Request,
    state: str,
    code: str = None,
    error: str = None,
    session: AsyncSession = Depends(get_session)
):
    """
    Handles the callback from Google OAuth.
    Updates OAuth session status and stores tokens.
    Returns a WhatsApp-friendly success page.
    """
    if error:
        # Handle OAuth error
        result = await session.execute(
            select(OAuthSession).where(OAuthSession.state == state)
        )
        oauth_session = result.scalar_one_or_none()
        if oauth_session:
            oauth_session.status = "failed"
            await session.commit()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authorization Failed</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: 0 auto; }
                .error { color: #e54028; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="error">Authorization Failed</h2>
                <p>Please try again from WhatsApp.</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    # Find OAuth session by state
    result = await session.execute(
        select(OAuthSession).where(OAuthSession.state == state)
    )
    oauth_session = result.scalar_one_or_none()
    
    if not oauth_session:
        raise HTTPException(status_code=404, detail="OAuth session not found")
    
    if oauth_session.status == "completed":
        # Already completed, show success page
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Already Authorized</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: 0 auto; }
                .success { color: #28a745; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="success">✓ Already Authorized</h2>
                <p>You can return to WhatsApp now.</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    try:
        # Exchange code for tokens
        client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        
        # Ensure redirect URI matches exactly what's in Google Console
        callback_uri = settings.GOOGLE_REDIRECT_URI.rstrip('/')
        
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=callback_uri
        )
        
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        # Store tokens in OAuth session
        oauth_session.access_token = creds.token
        oauth_session.refresh_token = creds.refresh_token
        if creds.expiry:
            oauth_session.token_expiry = (
                datetime.utcnow() + timedelta(seconds=creds.expiry)
            )
        oauth_session.status = "completed"
        oauth_session.completed_at = datetime.utcnow()
        await session.commit()
        
        # If there's a booking, process it
        if oauth_session.booking_id:
            booking = await session.get(Booking, oauth_session.booking_id)
            if booking:
                event = await session.get(Event, booking.event_id)
                if event:
                    desc = getattr(event, 'description', None) or "No description"
                    event_details = {
                        "name": event.name,
                        "location": event.location,
                        "description": desc,
                        "date": str(event.date),
                        "time": str(event.time)
                    }
                    
                    # Create calendar event
                    create_calendar_event(creds, event_details)
                    
                    # Send confirmation email
                    from googleapiclient.discovery import build
                    oauth_service = build('oauth2', 'v2', credentials=creds)
                    user_info = oauth_service.userinfo().get().execute()
                    user_email = user_info.get('email')
                    
                    if user_email:
                        send_confirmation_email(creds, user_email, event_details)
        
        # Return success page
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authorization Successful</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: 0 auto; }
                .success { color: #28a745; font-size: 48px; }
                h2 { color: #333; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success">✓</div>
                <h2>Authorization Successful!</h2>
                <p>You can now return to WhatsApp.</p>
                <p style="color: #666; font-size: 14px;">Your Google account has been connected.</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        oauth_session.status = "failed"
        await session.commit()
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {str(e)}")


@router.get("/google/status/{whatsapp_user_id}")
async def check_oauth_status(
    whatsapp_user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Webhook endpoint to check OAuth completion status for a WhatsApp user.
    Returns the latest OAuth session status.
    """
    result = await session.execute(
        select(OAuthSession)
        .where(OAuthSession.whatsapp_user_id == whatsapp_user_id)
        .order_by(OAuthSession.created_at.desc())
    )
    oauth_session = result.scalar_one_or_none()
    
    if not oauth_session:
        return {
            "status": "not_found",
            "message": "No OAuth session found for this user"
        }
    
    return {
        "status": oauth_session.status,
        "whatsapp_user_id": oauth_session.whatsapp_user_id,
        "booking_id": oauth_session.booking_id,
        "created_at": (
            oauth_session.created_at.isoformat()
            if oauth_session.created_at else None
        ),
        "completed_at": (
            oauth_session.completed_at.isoformat()
            if oauth_session.completed_at else None
        ),
        "has_tokens": bool(oauth_session.access_token)
    }


@router.get("/google/status")
async def check_oauth_status_by_state(
    state: str = Query(..., description="OAuth state token"),
    session: AsyncSession = Depends(get_session)
):
    """
    Check OAuth status by state token.
    Useful for webhook callbacks.
    """
    result = await session.execute(
        select(OAuthSession).where(OAuthSession.state == state)
    )
    oauth_session = result.scalar_one_or_none()
    
    if not oauth_session:
        return {
            "status": "not_found",
            "message": "OAuth session not found"
        }
    
    return {
        "status": oauth_session.status,
        "whatsapp_user_id": oauth_session.whatsapp_user_id,
        "booking_id": oauth_session.booking_id,
        "created_at": (
            oauth_session.created_at.isoformat()
            if oauth_session.created_at else None
        ),
        "completed_at": (
            oauth_session.completed_at.isoformat()
            if oauth_session.completed_at else None
        ),
        "has_tokens": bool(oauth_session.access_token)
    }
