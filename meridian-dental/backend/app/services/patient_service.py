from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, desc, func
from app.models.patient import Patient
from app.models.patient_timeline import PatientTimeline
from app.schemas.patient import PatientCreate, PatientUpdate
import uuid
import math
from fastapi import HTTPException

class PatientService:
    @staticmethod
    async def get_patients(db: AsyncSession, clinic_id: uuid.UUID, search: str = None, status: str = None, page: int = 1, page_size: int = 20):
        query = select(Patient).where(Patient.clinic_id == clinic_id, Patient.deleted_at == None)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Patient.full_name.ilike(search_term),
                    Patient.phone.ilike(search_term),
                    Patient.email.ilike(search_term),
                    Patient.patient_id_display.ilike(search_term)
                )
            )
            
        if status:
            query = query.where(Patient.status == status)
            
        total_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(total_query)
        total = total_result.scalar_one()
        
        query = query.order_by(desc(Patient.created_at)).offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        items = result.scalars().all()
        
        total_pages = math.ceil(total / page_size) if page_size else 0
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    @staticmethod
    async def get_patient(db: AsyncSession, patient_id: uuid.UUID):
        query = select(Patient).where(Patient.id == patient_id, Patient.deleted_at == None)
        result = await db.execute(query)
        patient = result.scalar_one_or_none()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    @staticmethod
    async def create_patient(db: AsyncSession, clinic_id: uuid.UUID, data: PatientCreate, created_by: uuid.UUID = None):
        # Generate patient_id_display
        count_query = select(func.count()).select_from(Patient).where(Patient.clinic_id == clinic_id)
        count_result = await db.execute(count_query)
        count = count_result.scalar_one()
        
        patient_id_display = f"P-{count + 1:05d}"
        
        patient = Patient(
            id=uuid.uuid4(),
            clinic_id=clinic_id,
            patient_id_display=patient_id_display,
            **data.model_dump(exclude_unset=True)
        )
        db.add(patient)
        
        # Add timeline event
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=patient.id,
            event_type="registration",
            title="Patient Registered",
            description=f"Patient {patient.full_name} registered.",
            created_by=created_by
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(patient)
        return patient

    @staticmethod
    async def update_patient(db: AsyncSession, patient_id: uuid.UUID, data: PatientUpdate):
        patient = await PatientService.get_patient(db, patient_id)
        update_data = data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(patient, key, value)
            
        await db.commit()
        await db.refresh(patient)
        return patient

    @staticmethod
    async def delete_patient(db: AsyncSession, patient_id: uuid.UUID):
        patient = await PatientService.get_patient(db, patient_id)
        patient.deleted_at = func.now()
        await db.commit()
        return True

    @staticmethod
    async def get_timeline(db: AsyncSession, patient_id: uuid.UUID, page: int = 1, page_size: int = 20):
        query = select(PatientTimeline).where(PatientTimeline.patient_id == patient_id).order_by(desc(PatientTimeline.created_at))
        
        total_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(total_query)
        total = total_result.scalar_one()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        items = result.scalars().all()
        
        total_pages = math.ceil(total / page_size) if page_size else 0
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
