from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.document import Document
from app.models.patient_timeline import PatientTimeline
import uuid
from fastapi import HTTPException, UploadFile
import os

class DocumentService:
    @staticmethod
    async def upload_document(db: AsyncSession, patient_id: uuid.UUID, user_id: uuid.UUID, file: UploadFile, category: str = 'other', notes: str = None):
        # Validate size, etc if needed. Simple save here.
        file_id = uuid.uuid4()
        extension = os.path.splitext(file.filename)[1]
        file_key = f"{file_id}{extension}"
        
        # Here we should save file to disk or S3. 
        # For this prototype, just keep a record.
        
        doc = Document(
            id=file_id,
            patient_id=patient_id,
            filename=file.filename,
            original_filename=file.filename,
            file_key=file_key,
            file_type=file.content_type,
            file_size=file.size,
            category=category,
            uploaded_by=user_id,
            notes=notes
        )
        db.add(doc)
        
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=patient_id,
            event_type="document_uploaded",
            title="Document Uploaded",
            description=f"Document '{file.filename}' uploaded.",
            created_by=user_id
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(doc)
        return doc
        
    @staticmethod
    async def get_documents(db: AsyncSession, patient_id: uuid.UUID):
        query = select(Document).where(Document.patient_id == patient_id, Document.deleted_at == None)
        return (await db.execute(query)).scalars().all()
