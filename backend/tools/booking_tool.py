import json
import uuid

def load_schedule():
    with open("data/doctor_schedule.json", "r") as f:
        return json.load(f)

def save_schedule(data):
    with open("data/doctor_schedule.json", "w") as f:
        json.dump(data, f, indent=4)

def book_slot(date: str, start: str, end: str, payload):
    schedule = load_schedule()
    existing = schedule["existing_bookings"].get(date, [])

    for b in existing:
        if b["start"] == start and b["end"] == end:
            return None  # Slot already booked

    existing.append({"start": start, "end": end})
    schedule["existing_bookings"][date] = existing

    save_schedule(schedule)

    return {
        "booking_id": str(uuid.uuid4())[:8],
        "status": "confirmed",
        "confirmation_code": str(uuid.uuid4())[:6].upper(),
        "details": payload
    }
