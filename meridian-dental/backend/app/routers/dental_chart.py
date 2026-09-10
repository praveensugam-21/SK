from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import List
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.dental_chart import DentalChartResponse, ToothUpdate, ToothResponse, ToothHistoryResponse
from app.services.dental_chart_service import DentalChartService

router = APIRouter(prefix='/api/patients', tags=['Dental Chart'])

@router.get('/{patient_id}/dental-chart')
async def get_dental_chart(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    teeth = await DentalChartService.get_dental_chart(db, patient_id)
    return {"patient_id": patient_id, "teeth": teeth}

@router.put('/{patient_id}/teeth/{tooth_number}', response_model=ToothResponse)
@router.put('/{patient_id}/dental-chart/{tooth_number}', response_model=ToothResponse)
async def update_tooth(
    patient_id: uuid.UUID,
    tooth_number: int,
    data: ToothUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(['dentist', 'admin']))
):
    return await DentalChartService.update_tooth(db, patient_id, tooth_number, data, current_user.id)

@router.get('/{patient_id}/teeth/{tooth_number}/history', response_model=List[ToothHistoryResponse])
@router.get('/{patient_id}/dental-chart/{tooth_number}/history', response_model=List[ToothHistoryResponse])
async def get_tooth_history(
    patient_id: uuid.UUID,
    tooth_number: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await DentalChartService.get_tooth_history(db, patient_id, tooth_number)
