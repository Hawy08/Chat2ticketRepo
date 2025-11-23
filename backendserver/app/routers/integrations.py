from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.google import CalendarEventRequest, EmailRequest
from app.services.google_service import create_calendar_event, send_email
from google.oauth2.credentials import Credentials
from app.core.config import settings
from app.core.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.oauth_session import OAuthSession

router = APIRouter(prefix="/integrations")


def get_creds(
    token: str,
    refresh_token: str = None,
    scopes: list = None
):
    """
    Creates Credentials object with refresh token support.
    If refresh_token is provided, credentials can auto-refresh.
    """
    return Credentials(
        token=token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=scopes
    )


async def get_creds_from_session(
    whatsapp_user_id: str,
    session: AsyncSession
) -> Credentials:
    """
    Retrieves credentials from OAuthSession database.
    Returns None if no valid session found.
    """
    result = await session.execute(
        select(OAuthSession)
        .where(OAuthSession.whatsapp_user_id == whatsapp_user_id)
        .where(OAuthSession.status == "completed")
        .order_by(OAuthSession.created_at.desc())
    )
    oauth_session = result.scalar_one_or_none()

    if not oauth_session or not oauth_session.access_token:
        return None

    return get_creds(
        token=oauth_session.access_token,
        refresh_token=oauth_session.refresh_token,
        scopes=[
            'https://www.googleapis.com/auth/calendar.events',
            'https://www.googleapis.com/auth/gmail.send',
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
    )


@router.post("/google/calendar")
async def add_calendar_event(
    request: CalendarEventRequest,
    refresh_token: str = Query(None, description="Optional refresh token")
):
    """Creates a Google Calendar event using the provided token."""
    try:
        creds = get_creds(request.token, refresh_token=refresh_token)
        event_details = {
            "name": request.name,
            "location": request.location,
            "description": request.description or "",
            "date": request.date,
            "time": request.time
        }
        result = create_calendar_event(creds, event_details)
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to create calendar event"
            )
        return {
            "message": "Calendar event created",
            "event_link": result.get('htmlLink')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from app.services.email_service import send_smtp_email

@router.post("/google/gmail")
async def send_gmail(
    request: EmailRequest,
):
    """
    Sends an email using the system's SMTP configuration.
    No Google Auth required from the user.
    """
    try:
        result = send_smtp_email(
            request.to_email, request.subject, request.body
        )
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to send email"
            )
        return {
            "message": "Email sent",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/google/gmail/by-booking/{booking_id}")
async def send_gmail_by_booking(
    booking_id: int,
    to_email: str = Query(..., description="Recipient email address"),
    subject: str = Query(..., description="Email subject"),
    body: str = Query(..., description="Email body"),
    session: AsyncSession = Depends(get_session)
):
    """
    Sends an email using the system's SMTP configuration.
    Does NOT require the user to have completed Google OAuth.
    """
    try:
        # We can still verify the booking exists if we want, but it's not strictly necessary for sending the email
        # if the caller provides all details.
        # But let's check it for consistency.
        from app.models.booking import Booking

        booking = await session.get(Booking, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        result = send_smtp_email(to_email, subject, body)
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to send email"
            )
        return {
            "message": "Email sent",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
