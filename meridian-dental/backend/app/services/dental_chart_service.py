from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.dental_chart import TeethRecord, ToothHistory
from app.models.patient_timeline import PatientTimeline
from app.schemas.dental_chart import ToothUpdate
import uuid
from fastapi import HTTPException

class DentalChartService:
    @staticmethod
    async def get_dental_chart(db: AsyncSession, patient_id: uuid.UUID):
        query = select(TeethRecord).where(TeethRecord.patient_id == patient_id).order_by(TeethRecord.tooth_number)
        result = await db.execute(query)
        existing_teeth = result.scalars().all()
        
        teeth_dict = {t.tooth_number: t for t in existing_teeth}
        full_chart = []
        
        for i in range(1, 33):
            if i in teeth_dict:
                full_chart.append(teeth_dict[i])
            else:
                full_chart.append(TeethRecord(
                    patient_id=patient_id,
                    tooth_number=i,
                    condition='healthy',
                    surfaces={'mesial': False, 'distal': False, 'occlusal': False, 'buccal': False, 'lingual': False}
                ))
        return full_chart

    @staticmethod
    async def update_tooth(db: AsyncSession, patient_id: uuid.UUID, tooth_number: int, data: ToothUpdate, user_id: uuid.UUID = None):
        query = select(TeethRecord).where(TeethRecord.patient_id == patient_id, TeethRecord.tooth_number == tooth_number)
        result = await db.execute(query)
        tooth = result.scalar_one_or_none()
        
        prev_condition = None
        if tooth:
            prev_condition = tooth.condition
            tooth.condition = data.condition
            if data.surfaces is not None:
                tooth.surfaces = data.surfaces.model_dump()
            tooth.diagnosis = data.diagnosis
            tooth.treatment = data.treatment
            tooth.notes = data.notes
            tooth.updated_by = user_id
        else:
            tooth = TeethRecord(
                id=uuid.uuid4(),
                patient_id=patient_id,
                tooth_number=tooth_number,
                condition=data.condition,
                surfaces=data.surfaces.model_dump() if data.surfaces else {'mesial': False, 'distal': False, 'occlusal': False, 'buccal': False, 'lingual': False},
                diagnosis=data.diagnosis,
                treatment=data.treatment,
                notes=data.notes,
                updated_by=user_id
            )
            db.add(tooth)
            
        await db.flush() # ensure tooth has an ID if new

        # History
        history = ToothHistory(
            id=uuid.uuid4(),
            record_id=tooth.id,
            previous_condition=prev_condition,
            new_condition=data.condition,
            diagnosis=data.diagnosis,
            treatment=data.treatment,
            notes=data.notes,
            changed_by=user_id
        )
        db.add(history)
        
        # Timeline
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=patient_id,
            event_type="dental_chart_updated",
            title=f"Tooth {tooth_number} Updated",
            description=f"Condition updated to {data.condition}",
            created_by=user_id
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(tooth)
        return tooth

    @staticmethod
    async def get_tooth_history(db: AsyncSession, patient_id: uuid.UUID, tooth_number: int):
        query = select(TeethRecord).where(TeethRecord.patient_id == patient_id, TeethRecord.tooth_number == tooth_number)
        result = await db.execute(query)
        tooth = result.scalar_one_or_none()
        if not tooth:
            return []
            
        hist_query = select(ToothHistory).where(ToothHistory.record_id == tooth.id).order_by(ToothHistory.changed_at.desc())
        hist_result = await db.execute(hist_query)
        return hist_result.scalars().all()
