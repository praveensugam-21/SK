from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class NoteCreate(BaseModel):
    patient_id: UUID
    content: str = Field(..., min_length=1)
    note_type: str = Field(default='general')
    is_clinical: bool = False

class NoteResponse(BaseModel):
    id: UUID
    patient_id: UUID
    author_id: UUID
    author_name: Optional[str] = None
    content: str
    note_type: str
    is_clinical: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
