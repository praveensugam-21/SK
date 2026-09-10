from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class DocumentResponse(BaseModel):
    id: UUID
    patient_id: UUID
    filename: str
    original_filename: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    category: str
    uploaded_by_name: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
