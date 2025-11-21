from fastapi import APIRouter, HTTPException
from backend.models.schemas import BookingRequest, BookingResponse, AvailabilityResponse
from backend.tools.availability_tool import generate_slots, APPOINTMENT_TYPES
from backend.tools.booking_tool import book_slot

router = APIRouter()

@router.get("/availability", response_model=AvailabilityResponse)
def get_availability(date: str, appointment_type: str):
    try:
        slots = generate_slots(date, appointment_type)
        return {"date": date, "available_slots": slots}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/book", response_model=BookingResponse)
def book_appointment(payload: BookingRequest):
    try:
        duration = APPOINTMENT_TYPES[payload.appointment_type]
    except:
        raise HTTPException(status_code=400, detail="Invalid appointment type")

    start = payload.start_time
    parts = start.split(":")
    hour = int(parts[0])
    minute = int(parts[1])
    end_hour = hour
    end_min = minute + duration
    if end_min >= 60:
        end_hour += 1
        end_min -= 60

    slot_end = f"{end_hour:02}:{end_min:02}"

    booking = book_slot(payload.date, payload.start_time, slot_end, payload.dict())

    if not booking:
        raise HTTPException(status_code=409, detail="Slot already booked")

    return booking
