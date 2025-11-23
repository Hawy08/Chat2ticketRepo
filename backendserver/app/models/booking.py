from sqlmodel import SQLModel, Field as SQLField

class BookingBase(SQLModel):
    event_id: int = SQLField(foreign_key="event.id")
    customer_name: str = SQLField(..., min_length=1, max_length=100)
    quantity: int = SQLField(gt=0)


class Booking(BookingBase, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    status: str = SQLField(default="pending")


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    id: int
    status: str
