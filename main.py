from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.calendly_integration import router as calendly_router

app = FastAPI(title="Calendly Mock API")

app.include_router(calendly_router, prefix="/api/calendly")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
