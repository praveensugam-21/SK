from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import List, Optional
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.treatment import TreatmentPlanCreate, TreatmentPlanUpdate, TreatmentPlanResponse, TreatmentCreate, TreatmentUpdate, TreatmentResponse
from app.services.treatment_service import TreatmentService

router = APIRouter(prefix='/api', tags=['Treatments'])

@router.get('/treatment-plans', response_model=List[TreatmentPlanResponse])
async def list_treatment_plans(
    patient_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await TreatmentService.get_treatment_plans(db, patient_id)

@router.post('/treatment-plans', response_model=TreatmentPlanResponse)
async def create_treatment_plan(
    data: TreatmentPlanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['dentist', 'admin']))
):
    return await TreatmentService.create_treatment_plan(db, current_user.clinic_id, current_user.id, data)

@router.post('/treatments', response_model=TreatmentResponse)
async def add_treatment(
    data: TreatmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['dentist', 'admin']))
):
    return await TreatmentService.add_treatment(db, current_user.id, data)

@router.put('/treatments/{id}', response_model=TreatmentResponse)
async def update_treatment(
    id: uuid.UUID,
    data: TreatmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['dentist', 'admin']))
):
    return await TreatmentService.update_treatment(db, id, data)

@router.get('/patients/{patient_id}/treatments', response_model=List[TreatmentPlanResponse])
async def get_patient_treatments(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await TreatmentService.get_treatment_plans(db, patient_id)
