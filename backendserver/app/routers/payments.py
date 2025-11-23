from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.models.booking import Booking, BookingCreate
from app.models.event import Event
from app.core.config import settings
import stripe

router = APIRouter(prefix="/payments", tags=["payments"])

stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/checkout")
async def create_checkout_session(booking_data: BookingCreate, session: AsyncSession = Depends(get_session)):
    # 1. Validate Event and Capacity
    event = await session.get(Event, booking_data.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.tickets_sold + booking_data.quantity > event.capacity:
        raise HTTPException(status_code=400, detail="Not enough tickets available")

    # 2. Create Pending Booking
    # We create it now to reserve the spot (optimistically) or just to have a record
    # For this implementation, we'll create it as "pending"
    booking = Booking.model_validate(booking_data)
    booking.status = "pending"
    session.add(booking)
    await session.commit()
    await session.refresh(booking)

    # 3. Create Stripe Checkout Session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"Ticket for {event.name}",
                    },
                    'unit_amount': int(event.price * 100), # Price in cents
                },
                'quantity': booking_data.quantity,
            }],
            mode='payment',
            success_url='https://0b44d62428f0.ngrok-free.app/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://0b44d62428f0.ngrok-free.app/cancel',
            client_reference_id=str(booking.id),
            metadata={
                "booking_id": str(booking.id),
                "event_id": str(event.id)
            }
        )
        return {"checkout_url": checkout_session.url, "session_id": checkout_session.id}
    except Exception as e:
        # If stripe fails, delete the pending booking?
        await session.delete(booking)
        await session.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/confirm/{session_id}")
async def confirm_payment(session_id: str, session: AsyncSession = Depends(get_session)):
    try:
        # Retrieve session from Stripe
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        if checkout_session.payment_status == 'paid':
            booking_id = checkout_session.client_reference_id
            if booking_id:
                booking = await session.get(Booking, int(booking_id))
                if booking and booking.status != "confirmed":
                    booking.status = "confirmed"
                    
                    # Update event tickets sold if not already done
                    # Note: In a real app, be careful of double counting if webhook also runs
                    # We can check if we already incremented
                    event = await session.get(Event, booking.event_id)
                    if event:
                        event.tickets_sold += booking.quantity
                        session.add(event)
                    
                    session.add(booking)
                    await session.commit()
                    await session.refresh(booking)
                    
                return {"status": "confirmed", "booking": booking}
        
        return {"status": "pending"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, session: AsyncSession = Depends(get_session)):
    payload = await request.body()
    if not payload:
        raise HTTPException(status_code=400, detail="Empty payload")
    sig_header = request.headers.get('stripe-signature')
    
    # In a real app, verify signature with settings.STRIPE_WEBHOOK_SECRET
    # event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    
    # For now, just parse the json
    import json
    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        booking_id = checkout_session.get('client_reference_id')
        
        if booking_id:
            booking = await session.get(Booking, int(booking_id))
            if booking and booking.status != "confirmed":
                booking.status = "confirmed"
                
                event_obj = await session.get(Event, booking.event_id)
                if event_obj:
                    event_obj.tickets_sold += booking.quantity
                    session.add(event_obj)
                
                session.add(booking)
                await session.commit()
                
    return {"status": "success"}
