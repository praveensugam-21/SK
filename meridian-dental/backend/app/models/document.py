import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin

class Document(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'documents'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'), nullable=False)
    filename = Column(String(500), nullable=False)
    original_filename = Column(String(500), nullable=False)
    file_key = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)
    category = Column(String(50), nullable=False, default='other')
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    notes = Column(Text, nullable=True)
    patient = relationship('Patient', back_populates='documents')
    uploader = relationship('User', foreign_keys=[uploaded_by])
