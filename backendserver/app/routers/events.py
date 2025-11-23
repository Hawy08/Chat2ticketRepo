from fastapi import APIRouter, Depends

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.models.event import Event, EventCreate, EventRead
from app.services.ai_generator import analyze_event_for_music
from app.services.spotify_client import get_spotify_track
from fastapi import HTTPException

router = APIRouter()


@router.post("/events", response_model=EventRead, status_code=201)
async def create_event(event: EventCreate, session: AsyncSession = Depends(get_session)):
    db_event = Event.model_validate(event)  # Pydantic v2 method
    session.add(db_event)
    await session.commit()
    await session.refresh(db_event)
    return db_event


@router.get("/events", response_model=list[EventRead])
async def list_events(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Event).order_by(Event.id))
    events = result.scalars().all()
    return events





@router.post("/events/{event_id}/playlist")
async def generate_playlist(event_id: int, session: AsyncSession = Depends(get_session)):
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # 1. Analyze with AI
    analysis = await analyze_event_for_music(event.name, event.description)
    
    if not analysis.get("is_music"):
        return {"message": "This event does not appear to be music-related."}
    
    # 2. Get Spotify Track
    query = analysis.get("search_query")
    if query:
        track = await get_spotify_track(query)
        if track:
            return {
                "message": "Track generated!",
                "analysis": analysis,
                "track": track
            }
            
    return {
        "message": "Could not find a suitable track.",
        "analysis": analysis
    }
