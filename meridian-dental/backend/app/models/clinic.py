import uuid
from sqlalchemy import Column, String, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from .base import TimestampMixin, Base

class Clinic(Base, TimestampMixin):
    __tablename__ = "clinics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(200))
    logo_url = Column(String(500), nullable=True)
    settings = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
