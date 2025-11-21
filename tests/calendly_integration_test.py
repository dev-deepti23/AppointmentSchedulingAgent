import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)


@patch("backend.api.calendly_integration.generate_slots")
def test_get_availability_success(mock_generate):
    mock_generate.return_value = [
        {"start_time": "09:00", "end_time": "09:30", "available": True},
        {"start_time": "09:30", "end_time": "10:00", "available": True}
    ]

    response = client.get(
        "/api/calendly/availability?date=2025-01-10&appointment_type=general"
    )

    assert response.status_code == 200
    assert response.json() == {
        "date": "2025-01-10",
        "available_slots": [
            {"start_time": "09:00", "end_time": "09:30", "available": True},
            {"start_time": "09:30", "end_time": "10:00", "available": True},
        ]
    }


@patch("backend.api.calendly_integration.generate_slots")
def test_get_availability_invalid(mock_generate):
    mock_generate.side_effect = ValueError("Invalid appointment type")

    response = client.get(
        "/api/calendly/availability?date=2025-01-10&appointment_type=wrong"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid appointment type"


@patch("backend.api.calendly_integration.book_slot")
@patch("backend.api.calendly_integration.APPOINTMENT_TYPES", {"general": 30})
def test_book_appointment_success(mock_book_slot):
    mock_book_slot.return_value = {
        "booking_id": "bk_123",
        "status": "booked",
        "confirmation_code": "CONF123",
        "details": {
            "date": "2025-01-10",
            "start_time": "10:00",
            "end_time": "10:30"
        }
    }

    payload = {
        "appointment_type": "general",
        "date": "2025-01-10",
        "start_time": "10:00",
        "patient": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9999999999"
        },
        "reason": "General checkup"
    }

    response = client.post("/api/calendly/book", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "booked"
    assert response.json()["details"]["end_time"] == "10:30"


@patch("backend.api.calendly_integration.APPOINTMENT_TYPES", {"general": 30})
def test_book_invalid_appointment_type():
    payload = {
        "appointment_type": "wrong",
        "date": "2025-01-10",
        "start_time": "10:00",
        "patient": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9999999999"
        },
        "reason": "General checkup"
    }

    response = client.post("/api/calendly/book", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid appointment type"


@patch("backend.api.calendly_integration.book_slot")
@patch("backend.api.calendly_integration.APPOINTMENT_TYPES", {"general": 30})
def test_book_slot_already_booked(mock_book_slot):
    mock_book_slot.return_value = None

    payload = {
        "appointment_type": "general",
        "date": "2025-01-10",
        "start_time": "10:00",
        "patient": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "9999999999"
        },
        "reason": "General checkup"
    }

    response = client.post("/api/calendly/book", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "Slot already booked"
