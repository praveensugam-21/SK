from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_, desc, func
from app.models.appointment import Appointment
from app.models.patient_timeline import PatientTimeline
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
import uuid
import math
from datetime import datetime, timedelta, time
from fastapi import HTTPException

class AppointmentService:
    @staticmethod
    async def get_appointments(db: AsyncSession, clinic_id: uuid.UUID, date_filter=None, dentist_id=None, patient_id=None, status=None, page: int = 1, page_size: int = 20):
        query = select(Appointment).where(Appointment.clinic_id == clinic_id)
        
        if date_filter:
            query = query.where(Appointment.date == date_filter)
        if dentist_id:
            query = query.where(Appointment.dentist_id == dentist_id)
        if patient_id:
            query = query.where(Appointment.patient_id == patient_id)
        if status:
            query = query.where(Appointment.status == status)
            
        total_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(total_query)
        total = total_result.scalar_one()
        
        query = query.order_by(desc(Appointment.date), desc(Appointment.start_time)).offset((page - 1) * page_size).limit(page_size)
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
    async def create_appointment(db: AsyncSession, clinic_id: uuid.UUID, data: AppointmentCreate, created_by: uuid.UUID = None):
        # Calculate end time
        start_datetime = datetime.combine(data.date, data.start_time)
        end_datetime = start_datetime + timedelta(minutes=data.duration_minutes)
        end_time = end_datetime.time()

        # Check conflicts
        conflict_query = select(Appointment).where(
            Appointment.dentist_id == data.dentist_id,
            Appointment.date == data.date,
            Appointment.status.notin_(['cancelled', 'no_show']),
            Appointment.start_time < end_time,
            Appointment.end_time > data.start_time
        )
        conflict_result = await db.execute(conflict_query)
        if conflict_result.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Appointment conflict detected")

        appointment = Appointment(
            id=uuid.uuid4(),
            clinic_id=clinic_id,
            patient_id=data.patient_id,
            dentist_id=data.dentist_id,
            date=data.date,
            start_time=data.start_time,
            end_time=end_time,
            duration_minutes=data.duration_minutes,
            appointment_type=data.appointment_type,
            notes=data.notes
        )
        db.add(appointment)
        
        # Add timeline event
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=data.patient_id,
            event_type="appointment_scheduled",
            title="Appointment Scheduled",
            description=f"Appointment scheduled for {data.date} at {data.start_time}",
            created_by=created_by
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(appointment)
        return appointment

    @staticmethod
    async def get_appointment(db: AsyncSession, appt_id: uuid.UUID):
        query = select(Appointment).where(Appointment.id == appt_id)
        result = await db.execute(query)
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return appointment

    @staticmethod
    async def update_appointment(db: AsyncSession, appt_id: uuid.UUID, data: AppointmentUpdate, updated_by: uuid.UUID = None):
        appointment = await AppointmentService.get_appointment(db, appt_id)
        
        # Handle time changes
        new_date = data.date if data.date else appointment.date
        new_start_time = data.start_time if data.start_time else appointment.start_time
        new_duration = data.duration_minutes if data.duration_minutes else appointment.duration_minutes
        
        if data.date or data.start_time or data.duration_minutes:
            start_datetime = datetime.combine(new_date, new_start_time)
            end_datetime = start_datetime + timedelta(minutes=new_duration)
            new_end_time = end_datetime.time()
            
            conflict_query = select(Appointment).where(
                Appointment.id != appt_id,
                Appointment.dentist_id == (data.dentist_id if data.dentist_id else appointment.dentist_id),
                Appointment.date == new_date,
                Appointment.status.notin_(['cancelled', 'no_show']),
                Appointment.start_time < new_end_time,
                Appointment.end_time > new_start_time
            )
            conflict_result = await db.execute(conflict_query)
            if conflict_result.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="Appointment conflict detected")
                
            appointment.end_time = new_end_time
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(appointment, key, value)
            
        await db.commit()
        await db.refresh(appointment)
        return appointment

    @staticmethod
    async def cancel_appointment(db: AsyncSession, appt_id: uuid.UUID, reason: str, cancelled_by: uuid.UUID = None):
        appointment = await AppointmentService.get_appointment(db, appt_id)
        appointment.status = 'cancelled'
        appointment.cancellation_reason = reason
        
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=appointment.patient_id,
            event_type="appointment_cancelled",
            title="Appointment Cancelled",
            description=f"Appointment cancelled: {reason}",
            created_by=cancelled_by
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(appointment)
        return appointment

    @staticmethod
    async def check_in(db: AsyncSession, appt_id: uuid.UUID):
        appointment = await AppointmentService.get_appointment(db, appt_id)
        appointment.status = 'checked_in'
        await db.commit()
        await db.refresh(appointment)
        return appointment
