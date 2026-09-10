import uuid
from sqlalchemy import Column, String, Text, Date, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Prescription(Base, TimestampMixin):
    __tablename__ = 'prescriptions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'), nullable=False)
    dentist_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False, server_default=func.current_date())
    diagnosis = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    patient = relationship('Patient', back_populates='prescriptions')
    dentist = relationship('User', foreign_keys=[dentist_id])
    items = relationship('PrescriptionItem', back_populates='prescription', cascade='all, delete-orphan')

class PrescriptionItem(Base, TimestampMixin):
    __tablename__ = 'prescription_items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prescription_id = Column(UUID(as_uuid=True), ForeignKey('prescriptions.id'), nullable=False)
    medication = Column(String(200), nullable=False)
    dosage = Column(String(100), nullable=True)
    frequency = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    instructions = Column(Text, nullable=True)
    prescription = relationship('Prescription', back_populates='items')
