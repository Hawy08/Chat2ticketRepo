import asyncio
from sqlmodel import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import engine
from app.models.oauth_session import OAuthSession

async def check_sessions():
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        # Check for booking 20
        print("Checking for Booking 20...")
        result = await session.execute(
            select(OAuthSession).where(OAuthSession.booking_id == 20)
        )
        sessions = result.scalars().all()
        if not sessions:
            print("No OAuth sessions found for booking 20.")
        else:
            for s in sessions:
                print(f"Session ID: {s.id}, Status: {s.status}, Created: {s.created_at}")

        # Check all completed sessions
        print("\nAll Completed Sessions:")
        result = await session.execute(
            select(OAuthSession).where(OAuthSession.status == "completed")
        )
        completed = result.scalars().all()
        for s in completed:
            print(f"Session ID: {s.id}, Booking ID: {s.booking_id}, User: {s.whatsapp_user_id}")

if __name__ == "__main__":
    asyncio.run(check_sessions())
