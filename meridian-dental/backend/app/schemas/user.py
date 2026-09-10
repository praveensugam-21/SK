from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: str = Field(..., min_length=1, max_length=200)
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=1, max_length=200)
    phone: Optional[str] = None
    role: str = Field(...)
    specialization: Optional[str] = None
    license_number: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    clinic_id: UUID
    phone: Optional[str] = None
    specialization: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
