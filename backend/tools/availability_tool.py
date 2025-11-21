import json
from datetime import datetime, timedelta

APPOINTMENT_TYPES = {
    "consultation": 30,
    "followup": 15,
    "physical": 45,
    "specialist": 60,
}

def load_schedule():
    with open("data/doctor_schedule.json", "r") as f:
        return json.load(f)

def generate_slots(date: str, appointment_type: str):
    schedule = load_schedule()
    working = schedule["working_hours"]
    existing = schedule["existing_bookings"].get(date, [])

    duration = APPOINTMENT_TYPES.get(appointment_type)
    if not duration:
        raise ValueError("Invalid appointment type.")

    start = datetime.strptime(date + " " + working["start"], "%Y-%m-%d %H:%M")
    end = datetime.strptime(date + " " + working["end"], "%Y-%m-%d %H:%M")

    delta = timedelta(minutes=duration)
    slots = []

    current = start
    while current + delta <= end:
        slot_start = current.strftime("%H:%M")
        slot_end = (current + delta).strftime("%H:%M")

        is_booked = any(
            b["start"] == slot_start and b["end"] == slot_end
            for b in existing
        )

        slots.append({
            "start_time": slot_start,
            "end_time": slot_end,
            "available": not is_booked
        })

        current += delta

    return slots
