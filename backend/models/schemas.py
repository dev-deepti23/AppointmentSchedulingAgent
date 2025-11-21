from pydantic import BaseModel, EmailStr
from typing import Optional

class Patient(BaseModel):
    name: str
    email: EmailStr
    phone: str

class BookingRequest(BaseModel):
    appointment_type: str
    date: str      # YYYY-MM-DD
    start_time: str
    patient: Patient
    reason: Optional[str] = None

class Slot(BaseModel):
    start_time: str
    end_time: str
    available: bool

class AvailabilityResponse(BaseModel):
    date: str
    available_slots: list[Slot]

class BookingResponse(BaseModel):
    booking_id: str
    status: str
    confirmation_code: str
    details: dict


