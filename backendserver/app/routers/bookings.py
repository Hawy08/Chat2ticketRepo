from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.models.booking import Booking, BookingCreate, BookingRead
from app.models.event import Event

router = APIRouter()


@router.post("/bookings", response_model=BookingRead, status_code=201)
async def create_booking(booking: BookingCreate, session: AsyncSession = Depends(get_session)):
    # Check if event exists
    event = await session.get(Event, booking.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check capacity
    if event.tickets_sold + booking.quantity > event.capacity:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough tickets available. Only {event.capacity - event.tickets_sold} left."
        )

    # Create booking
    db_booking = Booking.model_validate(booking)
    session.add(db_booking)

    # Update event tickets sold
    event.tickets_sold += booking.quantity
    session.add(event)

    await session.commit()
    await session.refresh(db_booking)
    return db_booking
