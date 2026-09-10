from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.note import NoteCreate, NoteResponse
from app.services.note_service import NoteService

router = APIRouter(prefix='/api', tags=['Notes'])

@router.post('/notes', response_model=NoteResponse)
async def create_note(
    data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await NoteService.create_note(db, current_user.id, data)

@router.get('/notes', response_model=List[NoteResponse])
async def list_notes(
    patient_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await NoteService.get_notes(db, patient_id)

@router.get('/patients/{patient_id}/notes', response_model=List[NoteResponse])
async def get_patient_notes(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await NoteService.get_notes(db, patient_id)
