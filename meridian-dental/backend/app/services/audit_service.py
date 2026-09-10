from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
import uuid

class AuditService:
    @staticmethod
    async def log(db: AsyncSession, user_id, action: str, entity_type: str, entity_id: str = None, old_values: dict = None, new_values: dict = None, ip_address: str = None, user_agent: str = None):
        log = AuditLog(
            id=uuid.uuid4(),
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id else None,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(log)
        await db.flush()
