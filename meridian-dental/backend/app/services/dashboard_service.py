from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.billing import Payment, Invoice
import uuid
from datetime import date, datetime

class DashboardService:
    @staticmethod
    async def get_stats(db: AsyncSession, clinic_id: uuid.UUID):
        today = date.today()
        start_of_month = today.replace(day=1)
        
        # total patients
        tp_query = select(func.count()).select_from(Patient).where(Patient.clinic_id == clinic_id, Patient.deleted_at == None)
        total_patients = (await db.execute(tp_query)).scalar()
        
        # today's appointments
        ta_query = select(func.count()).select_from(Appointment).where(
            Appointment.clinic_id == clinic_id, 
            Appointment.date == today,
            Appointment.status != 'cancelled'
        )
        todays_appointments = (await db.execute(ta_query)).scalar()
        
        # completed appointments
        ca_query = select(func.count()).select_from(Appointment).where(
            Appointment.clinic_id == clinic_id, 
            Appointment.date == today,
            Appointment.status == 'completed'
        )
        completed_appointments = (await db.execute(ca_query)).scalar()
        
        # pending appointments
        pa_query = select(func.count()).select_from(Appointment).where(
            Appointment.clinic_id == clinic_id, 
            Appointment.date == today,
            Appointment.status.in_(['scheduled', 'confirmed', 'pending'])
        )
        pending_appointments = (await db.execute(pa_query)).scalar()
        
        # cancelled appointments
        canc_query = select(func.count()).select_from(Appointment).where(
            Appointment.clinic_id == clinic_id, 
            Appointment.date == today,
            Appointment.status == 'cancelled'
        )
        cancelled_appointments = (await db.execute(canc_query)).scalar()
        
        # today's revenue (sum of payments created today)
        tr_query = select(func.sum(Payment.amount)).where(
            Payment.payment_date == today
        ).join(Invoice, Payment.invoice_id == Invoice.id).where(Invoice.clinic_id == clinic_id)
        todays_revenue = (await db.execute(tr_query)).scalar() or 0
        
        # outstanding amount
        oa_query = select(func.sum(Invoice.balance)).where(
            Invoice.clinic_id == clinic_id,
            Invoice.status != 'paid'
        )
        outstanding_amount = (await db.execute(oa_query)).scalar() or 0
        
        # new patients this month
        np_query = select(func.count()).select_from(Patient).where(
            Patient.clinic_id == clinic_id,
            Patient.deleted_at == None,
            Patient.created_at >= start_of_month
        )
        new_patients = (await db.execute(np_query)).scalar()
        
        return {
            "total_patients": total_patients,
            "todays_appointments": todays_appointments,
            "completed_appointments": completed_appointments,
            "pending_appointments": pending_appointments,
            "cancelled_appointments": cancelled_appointments,
            "todays_revenue": todays_revenue,
            "outstanding_amount": outstanding_amount,
            "new_patients_this_month": new_patients
        }

    @staticmethod
    async def get_today_schedule(db: AsyncSession, clinic_id: uuid.UUID):
        today = date.today()
        query = select(Appointment, Patient.full_name.label("patient_name")).join(
            Patient, Appointment.patient_id == Patient.id
        ).where(
            Appointment.clinic_id == clinic_id,
            Appointment.date == today,
            Appointment.status != 'cancelled'
        ).order_by(Appointment.start_time)
        
        result = await db.execute(query)
        rows = result.all()
        
        schedule = []
        for appt, patient_name in rows:
            schedule.append({
                "appointment_id": appt.id,
                "patient_name": patient_name,
                "time": appt.start_time.strftime("%H:%M"),
                "appointment_type": appt.appointment_type,
                "duration": appt.duration_minutes,
                "status": appt.status
            })
            
        return schedule
