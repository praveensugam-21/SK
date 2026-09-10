from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date
import uuid
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.schemas.common import PaginatedResponse
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix='/api/appointments', tags=['Appointments'])

@router.get('', response_model=PaginatedResponse[AppointmentResponse])
@router.get('/', response_model=PaginatedResponse[AppointmentResponse])
async def list_appointments(
    date_filter: Optional[date] = Query(None, alias="date"),
    dentist_id: Optional[uuid.UUID] = None,
    patient_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AppointmentService.get_appointments(db, current_user.clinic_id, date_filter, dentist_id, patient_id, status, page, page_size)

@router.post('', response_model=AppointmentResponse)
@router.post('/', response_model=AppointmentResponse)
async def create_appointment(
    data: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AppointmentService.create_appointment(db, current_user.clinic_id, data, current_user.id)

@router.get('/{id}', response_model=AppointmentResponse)
async def get_appointment(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AppointmentService.get_appointment(db, id)

@router.put('/{id}', response_model=AppointmentResponse)
async def update_appointment(
    id: uuid.UUID,
    data: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AppointmentService.update_appointment(db, id, data, current_user.id)

@router.delete('/{id}')
async def cancel_appointment(
    id: uuid.UUID,
    reason: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AppointmentService.cancel_appointment(db, id, reason, current_user.id)

@router.post('/{id}/check-in', response_model=AppointmentResponse)
async def check_in_appointment(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AppointmentService.check_in(db, id)
