from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.treatment import TreatmentPlan, Treatment
from app.models.patient_timeline import PatientTimeline
from app.schemas.treatment import TreatmentPlanCreate, TreatmentPlanUpdate, TreatmentCreate, TreatmentUpdate
import uuid
from fastapi import HTTPException
from datetime import datetime
from decimal import Decimal

class TreatmentService:
    @staticmethod
    async def get_treatment_plans(db: AsyncSession, patient_id: uuid.UUID = None):
        query = select(TreatmentPlan).options(selectinload(TreatmentPlan.treatments))
        if patient_id:
            query = query.where(TreatmentPlan.patient_id == patient_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create_treatment_plan(db: AsyncSession, clinic_id: uuid.UUID, dentist_id: uuid.UUID, data: TreatmentPlanCreate):
        plan = TreatmentPlan(
            id=uuid.uuid4(),
            clinic_id=clinic_id,
            patient_id=data.patient_id,
            dentist_id=dentist_id,
            title=data.title,
            description=data.description
        )
        db.add(plan)
        
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=data.patient_id,
            event_type="treatment_plan_created",
            title="Treatment Plan Created",
            description=f"Treatment plan '{data.title}' created.",
            created_by=dentist_id
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(plan)
        return plan
        
    @staticmethod
    async def add_treatment(db: AsyncSession, dentist_id: uuid.UUID, data: TreatmentCreate):
        treatment = Treatment(
            id=uuid.uuid4(),
            plan_id=data.plan_id,
            patient_id=data.patient_id,
            dentist_id=dentist_id,
            tooth_number=data.tooth_number,
            diagnosis=data.diagnosis,
            treatment_type=data.treatment_type,
            description=data.description,
            cost=data.cost,
            notes=data.notes
        )
        db.add(treatment)
        
        if data.plan_id:
            plan_query = select(TreatmentPlan).where(TreatmentPlan.id == data.plan_id)
            plan = (await db.execute(plan_query)).scalar_one_or_none()
            if plan:
                plan.total_estimated_cost += data.cost
                
        await db.commit()
        await db.refresh(treatment)
        return treatment
        
    @staticmethod
    async def update_treatment(db: AsyncSession, treatment_id: uuid.UUID, data: TreatmentUpdate):
        query = select(Treatment).where(Treatment.id == treatment_id)
        treatment = (await db.execute(query)).scalar_one_or_none()
        if not treatment:
            raise HTTPException(status_code=404, detail="Treatment not found")
            
        old_cost = treatment.cost
            
        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(treatment, k, v)
            
        if data.status == 'completed' and not treatment.completed_at:
            treatment.completed_at = datetime.utcnow()
            
        if 'cost' in update_data and treatment.plan_id:
            plan_query = select(TreatmentPlan).where(TreatmentPlan.id == treatment.plan_id)
            plan = (await db.execute(plan_query)).scalar_one_or_none()
            if plan:
                plan.total_estimated_cost += (Decimal(str(data.cost)) - old_cost)
                
        await db.commit()
        await db.refresh(treatment)
        return treatment
