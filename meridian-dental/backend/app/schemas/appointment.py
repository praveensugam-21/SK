from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime
from uuid import UUID

class AppointmentCreate(BaseModel):
    patient_id: UUID
    dentist_id: UUID
    date: date
    start_time: time
    duration_minutes: int = Field(30, ge=5, le=480)
    appointment_type: str = Field(..., min_length=1)
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    patient_id: Optional[UUID] = None
    dentist_id: Optional[UUID] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    duration_minutes: Optional[int] = Field(None, ge=5, le=480)
    appointment_type: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    cancellation_reason: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: UUID
    clinic_id: UUID
    patient_id: UUID
    dentist_id: UUID
    patient_name: Optional[str] = None
    dentist_name: Optional[str] = None
    date: date
    start_time: time
    end_time: time
    duration_minutes: int
    appointment_type: str
    status: str
    notes: Optional[str] = None
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
