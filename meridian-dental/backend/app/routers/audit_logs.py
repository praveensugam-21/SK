from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, func
import math
from app.database import get_db
from app.dependencies import require_role
from app.models.user import User
from app.models.audit_log import AuditLog

router = APIRouter(prefix='/api/audit-logs', tags=['Audit Logs'])

@router.get('')
@router.get('/')
async def get_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['admin']))
):
    query = select(AuditLog).order_by(desc(AuditLog.created_at))
    total_query = select(func.count()).select_from(AuditLog)
    total = (await db.execute(total_query)).scalar_one()

    items_query = query.offset((page - 1) * page_size).limit(page_size)
    items = (await db.execute(items_query)).scalars().all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if page_size else 0
    }
