from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: str
    clinic_id: Optional[UUID] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
