from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.billing import InvoiceCreate, InvoiceResponse, InvoiceListResponse, PaymentCreate, PaymentResponse
from app.schemas.common import PaginatedResponse
from app.services.billing_service import BillingService

router = APIRouter(tags=['Billing'])

@router.get('/api/invoices', response_model=PaginatedResponse[InvoiceListResponse])
@router.get('/api/billing/invoices', response_model=PaginatedResponse[InvoiceListResponse])
async def list_invoices(
    patient_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await BillingService.get_invoices(db, current_user.clinic_id, patient_id, status, page, page_size)

@router.post('/api/invoices', response_model=InvoiceResponse)
@router.post('/api/billing/invoices', response_model=InvoiceResponse)
async def create_invoice(
    data: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await BillingService.create_invoice(db, current_user.clinic_id, data, current_user.id)

@router.get('/api/invoices/{id}', response_model=InvoiceResponse)
@router.get('/api/billing/invoices/{id}', response_model=InvoiceResponse)
async def get_invoice(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await BillingService.get_invoice(db, id)

@router.post('/api/payments', response_model=PaymentResponse)
async def record_payment(
    data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await BillingService.record_payment(db, data, current_user.id)

@router.post('/api/invoices/{id}/payments', response_model=PaymentResponse)
@router.post('/api/billing/invoices/{id}/payments', response_model=PaymentResponse)
async def record_invoice_payment(
    id: uuid.UUID,
    data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data.invoice_id = id
    return await BillingService.record_payment(db, data, current_user.id)
