from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardStats, TodayScheduleItem
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix='/api/dashboard', tags=['Dashboard'])

@router.get('/stats', response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await DashboardService.get_stats(db, current_user.clinic_id)

@router.get('/today-schedule', response_model=List[TodayScheduleItem])
async def get_today_schedule(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await DashboardService.get_today_schedule(db, current_user.clinic_id)
