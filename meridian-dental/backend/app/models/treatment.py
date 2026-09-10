import uuid
from sqlalchemy import Column, String, Text, Integer, Numeric, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class TreatmentPlan(Base, TimestampMixin):
    __tablename__ = 'treatment_plans'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey('clinics.id'), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'), nullable=False)
    dentist_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default='planned')
    total_estimated_cost = Column(Numeric(12, 2), nullable=False, default=0)
    patient = relationship('Patient', back_populates='treatment_plans')
    dentist = relationship('User', foreign_keys=[dentist_id])
    treatments = relationship('Treatment', back_populates='plan', cascade='all, delete-orphan')

class Treatment(Base, TimestampMixin):
    __tablename__ = 'treatments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey('treatment_plans.id'), nullable=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'), nullable=False)
    dentist_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    tooth_number = Column(Integer, nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    cost = Column(Numeric(12, 2), nullable=False, default=0)
    status = Column(String(20), nullable=False, default='planned')
    notes = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    plan = relationship('TreatmentPlan', back_populates='treatments')
    patient = relationship('Patient', back_populates='treatments')
    dentist = relationship('User', foreign_keys=[dentist_id])
