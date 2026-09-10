import uuid
from sqlalchemy import Column, String, Text, Integer, Date, Time, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import TimestampMixin, Base

class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"))
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    dentist_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=30)
    appointment_type = Column(String(50), nullable=False)
    status = Column(String(20), default='scheduled')
    notes = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    patient = relationship("Patient")
    dentist = relationship("User", foreign_keys=[dentist_id])
    creator = relationship("User", foreign_keys=[created_by])
    
    # DB-level overlap check would require complex triggers or exclusion constraints in Postgres
    # Usually better handled at the application service layer.
