import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import TimestampMixin, SoftDeleteMixin, Base

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"))
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    full_name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(String(50), nullable=False)
    specialization = Column(String(200), nullable=True)
    license_number = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    clinic = relationship("Clinic")
