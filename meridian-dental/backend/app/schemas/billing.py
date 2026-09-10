from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

class InvoiceItemCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    treatment_id: Optional[UUID] = None
    quantity: int = Field(1, ge=1)
    unit_price: Decimal = Field(..., ge=0)
    discount: Decimal = Field(default=Decimal('0'), ge=0)

class InvoiceCreate(BaseModel):
    patient_id: UUID
    due_date: date
    items: List[InvoiceItemCreate] = Field(..., min_length=1)
    discount_amount: Decimal = Field(default=Decimal('0'), ge=0)
    tax_amount: Decimal = Field(default=Decimal('0'), ge=0)
    notes: Optional[str] = None

class InvoiceItemResponse(BaseModel):
    id: UUID
    description: str
    treatment_id: Optional[UUID] = None
    quantity: int
    unit_price: Decimal
    discount: Decimal
    amount: Decimal

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    invoice_id: UUID
    amount: Decimal = Field(..., gt=0)
    payment_method: str = Field(..., min_length=1)
    transaction_reference: Optional[str] = None
    payment_date: Optional[date] = None
    notes: Optional[str] = None

class PaymentResponse(BaseModel):
    id: UUID
    invoice_id: UUID
    amount: Decimal
    payment_method: str
    transaction_reference: Optional[str] = None
    payment_date: date
    received_by_name: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class InvoiceResponse(BaseModel):
    id: UUID
    patient_id: UUID
    patient_name: Optional[str] = None
    invoice_number: str
    invoice_date: date
    due_date: date
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    amount_paid: Decimal
    balance: Decimal
    status: str
    notes: Optional[str] = None
    items: List[InvoiceItemResponse] = []
    payments: List[PaymentResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class InvoiceListResponse(BaseModel):
    id: UUID
    patient_id: UUID
    patient_name: Optional[str] = None
    invoice_number: str
    invoice_date: date
    due_date: date
    total_amount: Decimal
    amount_paid: Decimal
    balance: Decimal
    status: str
    item_summary: Optional[str] = None

    class Config:
        from_attributes = True
