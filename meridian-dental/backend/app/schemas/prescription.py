from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

class PrescriptionItemCreate(BaseModel):
    medication: str = Field(..., min_length=1, max_length=200)
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None

class PrescriptionCreate(BaseModel):
    patient_id: UUID
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    items: List[PrescriptionItemCreate] = Field(..., min_length=1)

class PrescriptionItemResponse(BaseModel):
    id: UUID
    medication: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None

    class Config:
        from_attributes = True

class PrescriptionResponse(BaseModel):
    id: UUID
    patient_id: UUID
    dentist_id: UUID
    dentist_name: Optional[str] = None
    date: date
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    items: List[PrescriptionItemResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
