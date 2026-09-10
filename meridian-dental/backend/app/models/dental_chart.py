import uuid
from sqlalchemy import Column, String, Text, Integer, JSON, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import TimestampMixin, Base

class TeethRecord(Base, TimestampMixin):
    __tablename__ = "teeth_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    tooth_number = Column(Integer, nullable=False)
    condition = Column(String(50), default='healthy')
    surfaces = Column(JSON, nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    __table_args__ = (UniqueConstraint('patient_id', 'tooth_number', name='_patient_tooth_uc'),)
    
    patient = relationship("Patient", back_populates="teeth_records")
    updated_by_user = relationship("User")
    history = relationship("ToothHistory", back_populates="teeth_record")

class ToothHistory(Base):
    __tablename__ = "tooth_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id = Column(UUID(as_uuid=True), ForeignKey("teeth_records.id"))
    previous_condition = Column(String(50))
    new_condition = Column(String(50))
    previous_surfaces = Column(JSON, nullable=True)
    new_surfaces = Column(JSON, nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    teeth_record = relationship("TeethRecord", back_populates="history")
