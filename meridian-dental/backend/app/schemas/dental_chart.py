from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from uuid import UUID

class SurfacesSchema(BaseModel):
    mesial: bool = False
    distal: bool = False
    occlusal: bool = False
    buccal: bool = False
    lingual: bool = False

class ToothUpdate(BaseModel):
    condition: str = Field(..., min_length=1)
    surfaces: Optional[SurfacesSchema] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None

class ToothResponse(BaseModel):
    tooth_number: int
    condition: str
    surfaces: Optional[dict] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None
    updated_by_name: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DentalChartResponse(BaseModel):
    patient_id: UUID
    teeth: List[ToothResponse]

class ToothHistoryResponse(BaseModel):
    id: UUID
    previous_condition: Optional[str] = None
    new_condition: str
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None
    changed_by_name: Optional[str] = None
    changed_at: datetime

    class Config:
        from_attributes = True
