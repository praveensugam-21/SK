from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID

class TreatmentCreate(BaseModel):
    plan_id: Optional[UUID] = None
    patient_id: UUID
    tooth_number: Optional[int] = None
    diagnosis: Optional[str] = None
    treatment_type: str = Field(..., min_length=1)
    description: Optional[str] = None
    cost: Decimal = Field(default=Decimal('0'), ge=0)
    notes: Optional[str] = None

class TreatmentUpdate(BaseModel):
    tooth_number: Optional[int] = None
    diagnosis: Optional[str] = None
    treatment_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[Decimal] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class TreatmentResponse(BaseModel):
    id: UUID
    plan_id: Optional[UUID] = None
    patient_id: UUID
    dentist_id: UUID
    dentist_name: Optional[str] = None
    tooth_number: Optional[int] = None
    diagnosis: Optional[str] = None
    treatment_type: str
    description: Optional[str] = None
    cost: Decimal
    status: str
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TreatmentPlanCreate(BaseModel):
    patient_id: UUID
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

class TreatmentPlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TreatmentPlanResponse(BaseModel):
    id: UUID
    patient_id: UUID
    dentist_id: UUID
    dentist_name: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str
    total_estimated_cost: Decimal
    treatments: List[TreatmentResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
