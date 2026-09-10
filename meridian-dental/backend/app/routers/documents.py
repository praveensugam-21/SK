from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix='/api', tags=['Documents'])

@router.post('/documents/upload', response_model=DocumentResponse)
async def upload_document(
    patient_id: uuid.UUID = Form(...),
    category: str = Form('other'),
    notes: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await DocumentService.upload_document(db, patient_id, current_user.id, file, category, notes)

@router.get('/patients/{patient_id}/documents', response_model=List[DocumentResponse])
async def get_patient_documents(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await DocumentService.get_documents(db, patient_id)
    
@router.get('/documents/{id}/download')
async def download_document(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # This would return a FileResponse or pre-signed URL in a real app
    raise HTTPException(status_code=501, detail="Not implemented in this prototype")
