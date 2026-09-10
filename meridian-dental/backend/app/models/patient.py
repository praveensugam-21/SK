import uuid
from sqlalchemy import Column, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin


class Patient(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"))
    patient_id_display = Column(String(20), unique=True, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    phone = Column(String(20), index=True)
    email = Column(String(200), nullable=True, index=True)
    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    blood_group = Column(String(10), nullable=True)
    allergies = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    insurance_provider = Column(String(200), nullable=True)
    insurance_id = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default='active')

    # Relationships
    clinic = relationship("Clinic")
    appointments = relationship("Appointment", back_populates="patient", lazy="dynamic")
    teeth_records = relationship("TeethRecord", back_populates="patient", lazy="dynamic")
    treatment_plans = relationship("TreatmentPlan", back_populates="patient", lazy="dynamic")
    treatments = relationship("Treatment", back_populates="patient", lazy="dynamic")
    invoices = relationship("Invoice", back_populates="patient", lazy="dynamic")
    prescriptions = relationship("Prescription", back_populates="patient", lazy="dynamic")
    documents = relationship("Document", back_populates="patient", lazy="dynamic")
    notes_records = relationship("Note", back_populates="patient", lazy="dynamic")
    timeline_events = relationship("PatientTimeline", back_populates="patient", lazy="dynamic")
