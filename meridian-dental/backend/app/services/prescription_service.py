from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.prescription import Prescription, PrescriptionItem
from app.models.patient_timeline import PatientTimeline
from app.schemas.prescription import PrescriptionCreate
import uuid

class PrescriptionService:
    @staticmethod
    async def create_prescription(db: AsyncSession, dentist_id: uuid.UUID, data: PrescriptionCreate):
        prescription = Prescription(
            id=uuid.uuid4(),
            patient_id=data.patient_id,
            dentist_id=dentist_id,
            diagnosis=data.diagnosis,
            notes=data.notes
        )
        db.add(prescription)
        
        for item_data in data.items:
            item = PrescriptionItem(
                id=uuid.uuid4(),
                prescription_id=prescription.id,
                medication=item_data.medication,
                dosage=item_data.dosage,
                frequency=item_data.frequency,
                duration=item_data.duration,
                instructions=item_data.instructions
            )
            db.add(item)
            
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=data.patient_id,
            event_type="prescription_created",
            title="Prescription Added",
            description=f"Prescription created with {len(data.items)} items.",
            created_by=dentist_id
        )
        db.add(event)
            
        await db.commit()
        await db.refresh(prescription)
        return prescription
        
    @staticmethod
    async def get_prescriptions(db: AsyncSession, patient_id: uuid.UUID):
        query = select(Prescription).where(Prescription.patient_id == patient_id).options(selectinload(Prescription.items))
        return (await db.execute(query)).scalars().all()
