import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class PatientTimeline(Base):
    __tablename__ = 'patient_timeline'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_id = Column(UUID(as_uuid=True), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    patient = relationship('Patient', back_populates='timeline_events')
    creator = relationship('User', foreign_keys=[created_by])
