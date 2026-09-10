from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import date
from typing import Optional
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.appointment import Appointment
from app.models.billing import Invoice, Payment
from app.models.patient import Patient

router = APIRouter(prefix='/api/reports', tags=['Reports'])

@router.get('/appointments')
async def get_appointment_reports(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Appointment.status, func.count(Appointment.id)).where(Appointment.clinic_id == current_user.clinic_id)
    if start_date:
        query = query.where(Appointment.date >= start_date)
    if end_date:
        query = query.where(Appointment.date <= end_date)
    query = query.group_by(Appointment.status)
    results = (await db.execute(query)).all()
    return {"breakdown": {status: count for status, count in results}}

@router.get('/revenue')
async def get_revenue_reports(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(func.coalesce(func.sum(Payment.amount), 0)).select_from(Payment).join(Invoice).where(Invoice.clinic_id == current_user.clinic_id)
    if start_date:
        query = query.where(Payment.payment_date >= start_date)
    if end_date:
        query = query.where(Payment.payment_date <= end_date)
    total_revenue = (await db.execute(query)).scalar_one()
    return {"total_revenue": total_revenue}

@router.get('/patients')
async def get_patient_reports(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(func.count(Patient.id)).where(Patient.clinic_id == current_user.clinic_id, Patient.deleted_at.is_(None))
    total_patients = (await db.execute(query)).scalar_one()
    return {"total_patients": total_patients}
