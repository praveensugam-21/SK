from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse, PatientListResponse
from app.schemas.common import PaginatedResponse
from app.services.patient_service import PatientService

router = APIRouter(prefix='/api/patients', tags=['Patients'])

@router.get('', response_model=PaginatedResponse[PatientListResponse])
@router.get('/', response_model=PaginatedResponse[PatientListResponse])
async def list_patients(
    q: Optional[str] = None,
    search: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query_term = search or q
    result = await PatientService.get_patients(db, current_user.clinic_id, query_term, status, page, page_size)
    return result

@router.post('', response_model=PatientResponse)
@router.post('/', response_model=PatientResponse)
async def create_patient(
    data: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['admin', 'dentist', 'receptionist']))
):
    return await PatientService.create_patient(db, current_user.clinic_id, data, current_user.id)

@router.get('/{id}', response_model=PatientResponse)
async def get_patient(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await PatientService.get_patient(db, id)

@router.put('/{id}', response_model=PatientResponse)
async def update_patient(
    id: uuid.UUID,
    data: PatientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['admin', 'receptionist', 'dentist']))
):
    return await PatientService.update_patient(db, id, data)

@router.delete('/{id}')
async def delete_patient(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['admin']))
):
    await PatientService.delete_patient(db, id)
    return {"message": "Patient deleted successfully"}

@router.get('/{id}/timeline')
async def get_patient_timeline(
    id: uuid.UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await PatientService.get_timeline(db, id, page, page_size)
