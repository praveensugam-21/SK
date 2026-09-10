import uuid
from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Notification(Base, TimestampMixin):
    __tablename__ = 'notifications'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey('clinics.id'), nullable=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=True)
    notification_type = Column(String(50), nullable=False, default='system')
    is_read = Column(Boolean, nullable=False, default=False)
    action_url = Column(String(500), nullable=True)
    user = relationship('User', foreign_keys=[user_id])
