from datetime import date, time
from sqlmodel import SQLModel, Field as SQLField
from pydantic import computed_field

class EventBase(SQLModel):
    name: str = SQLField(..., min_length=1, max_length=200)
    date: date
    time: time
    description: str | None = SQLField(default=None, max_length=1000)
    location: str = SQLField(..., min_length=1, max_length=255)
    price: float = SQLField(gt=0)
    capacity: int = SQLField(gt=0)
    tickets_sold: int = SQLField(default=0, ge=0)


class Event(EventBase, table=True):
    id: int | None = SQLField(default=None, primary_key=True)


class EventCreate(EventBase):
    tickets_sold: int = 0



class EventRead(EventBase):
    id: int

    @computed_field
    @property
    def map_link(self) -> str:
        return f"https://www.google.com/maps/search/?api=1&query={self.location}"
