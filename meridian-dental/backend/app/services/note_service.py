from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.note import Note
from app.models.patient_timeline import PatientTimeline
from app.schemas.note import NoteCreate
import uuid

class NoteService:
    @staticmethod
    async def create_note(db: AsyncSession, author_id: uuid.UUID, data: NoteCreate):
        note = Note(
            id=uuid.uuid4(),
            patient_id=data.patient_id,
            author_id=author_id,
            content=data.content,
            note_type=data.note_type,
            is_clinical=data.is_clinical
        )
        db.add(note)
        
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=data.patient_id,
            event_type="note_added",
            title="Note Added",
            description=f"{data.note_type.capitalize()} note added.",
            created_by=author_id
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(note)
        return note

    @staticmethod
    async def get_notes(db: AsyncSession, patient_id: uuid.UUID):
        query = select(Note).where(Note.patient_id == patient_id, Note.deleted_at == None).order_by(desc(Note.created_at))
        return (await db.execute(query)).scalars().all()
