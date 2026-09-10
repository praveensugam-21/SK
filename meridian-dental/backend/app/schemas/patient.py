from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: str = Field(..., min_length=1, max_length=20)
    email: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None
    notes: Optional[str] = None

class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class PatientResponse(BaseModel):
    id: UUID
    patient_id_display: str
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None
    notes: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PatientListResponse(BaseModel):
    id: UUID
    patient_id_display: str
    full_name: str
    date_of_birth: Optional[date] = None
    phone: str
    email: Optional[str] = None
    status: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True
