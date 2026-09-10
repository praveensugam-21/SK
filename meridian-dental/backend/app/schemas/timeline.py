from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class TimelineEventResponse(BaseModel):
    id: UUID
    event_type: str
    title: str
    description: Optional[str] = None
    created_by_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
