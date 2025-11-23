from fastapi import FastAPI
from sqlmodel import SQLModel
from app.core.db import engine
from app.routers import events, system, bookings, payments, frontend, auth, integrations
from app.models import oauth_session  # Import to register model

app = FastAPI(title="Ticketing API")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(system.router)
app.include_router(payments.router)
app.include_router(frontend.router)
app.include_router(auth.router)
app.include_router(integrations.router)

