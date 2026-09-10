import uuid
from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin

class Note(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'notes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    note_type = Column(String(50), nullable=False, default='general')
    is_clinical = Column(Boolean, nullable=False, default=False)
    patient = relationship('Patient', back_populates='notes_records')
    author = relationship('User', foreign_keys=[author_id])
