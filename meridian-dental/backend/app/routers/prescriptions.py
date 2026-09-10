from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from app.services.prescription_service import PrescriptionService

router = APIRouter(prefix='/api/prescriptions', tags=['Prescriptions'])

@router.post('', response_model=PrescriptionResponse)
@router.post('/', response_model=PrescriptionResponse)
async def create_prescription(
    data: PrescriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['dentist', 'admin']))
):
    return await PrescriptionService.create_prescription(db, current_user.id, data)

@router.get('', response_model=List[PrescriptionResponse])
@router.get('/', response_model=List[PrescriptionResponse])
async def list_prescriptions(
    patient_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await PrescriptionService.get_prescriptions(db, patient_id)

@router.get('/patient/{patient_id}', response_model=List[PrescriptionResponse])
async def get_patient_prescriptions(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await PrescriptionService.get_prescriptions(db, patient_id)
