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
source venv/bin/activate
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
