from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime
from typing import Optional


class OAuthSessionBase(SQLModel):
    # WhatsApp phone number or user ID
    whatsapp_user_id: str = SQLField(..., index=True)
    # OAuth state token
    state: str = SQLField(..., unique=True, index=True)
    status: str = SQLField(default="pending")  # pending, completed, failed
    booking_id: Optional[int] = SQLField(
        default=None, foreign_key="booking.id"
    )


class OAuthSession(OAuthSessionBase, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    created_at: datetime = SQLField(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    # Store encrypted in production
    access_token: Optional[str] = None
    # Store encrypted in production
    refresh_token: Optional[str] = None
    token_expiry: Optional[datetime] = None



class OAuthSessionCreate(SQLModel):
    whatsapp_user_id: str
    booking_id: Optional[int] = None


class OAuthSessionRead(SQLModel):
    id: int
    whatsapp_user_id: str
    state: str
    status: str
    booking_id: Optional[int]
    created_at: datetime
    completed_at: Optional[datetime]
