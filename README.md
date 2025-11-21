# AppointmentSchedulingAgent

This project is a FastAPI-based backend for managing doctor appointment scheduling, checking slot availability, and booking appointments.

---

## Requirements

- Python 3.8+
- pip

---

## Setup Instructions (Backend)

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/AppointmentSchedulingAgent.git
cd AppointmentSchedulingAgent/backend
```

### **2. Create a Virtual Environment**
```
python3 -m venv venv
source venv/bin/activate        # For Linux / macOS


venv\Scripts\activate           # For Windows
```

### **3. Install Dependencies**
```
pip install -r requirements.txt
```

### **4. Prepare the Data File**
```
backend/data/doctor_schedule.json
```

### **5. Run the FastAPI Server**
```
uvicorn main:app --reload
```

## API Documentation

### **Swagger UI**

```
http://127.0.0.1:8000/docs
```

### **ReDoc**
```
http://127.0.0.1:8000/redoc
```

## How to Test the APIs

#### 1. Test Availability API
##### GET /availability

```
http://127.0.0.1:8000/availability?date=2025-02-10&appointment_type=consultation
```
#### Example Response:
```
{
  "date": "2025-02-10",
  "available_slots": [
    {
      "start_time": "09:00",
      "end_time": "09:30",
      "available": true
    }
  ]
}
```

#### 2. Test Booking API
##### POST /book
#### Request Body:

```
{
  "appointment_type": "consultation",
  "date": "2025-02-10",
  "start_time": "10:00",
  "patient": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210"
  },
  "reason": "General checkup"
}
```

#### Example Response:
```
{
  "booking_id": "12345",
  "status": "confirmed",
  "confirmation_code": "A1B2C3"
}
```
