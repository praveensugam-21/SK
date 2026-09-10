from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from uuid import UUID

class DashboardStats(BaseModel):
    total_patients: int = 0
    todays_appointments: int = 0
    completed_appointments: int = 0
    pending_appointments: int = 0
    cancelled_appointments: int = 0
    todays_revenue: Decimal = Decimal('0')
    outstanding_amount: Decimal = Decimal('0')
    new_patients_this_month: int = 0

class TodayScheduleItem(BaseModel):
    appointment_id: UUID
    patient_name: str
    time: str
    appointment_type: str
    duration: int
    status: str
