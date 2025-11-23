from pydantic import BaseModel
from typing import Optional

class CalendarEventRequest(BaseModel):
    name: str
    location: str
    description: Optional[str] = None
    date: str
    time: str
    token: str

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str
    token: str
