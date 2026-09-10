from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, desc
from app.models.billing import Invoice, InvoiceItem, Payment
from app.models.patient_timeline import PatientTimeline
from app.schemas.billing import InvoiceCreate, PaymentCreate
import uuid
import math
from fastapi import HTTPException
from decimal import Decimal

class BillingService:
    @staticmethod
    async def create_invoice(db: AsyncSession, clinic_id: uuid.UUID, data: InvoiceCreate, user_id: uuid.UUID = None):
        # Generate Invoice Number
        count_query = select(func.count()).select_from(Invoice).where(Invoice.clinic_id == clinic_id)
        count = (await db.execute(count_query)).scalar_one()
        invoice_number = f"INV-{count + 1:05d}"
        
        invoice = Invoice(
            id=uuid.uuid4(),
            clinic_id=clinic_id,
            patient_id=data.patient_id,
            invoice_number=invoice_number,
            due_date=data.due_date,
            discount_amount=data.discount_amount,
            tax_amount=data.tax_amount,
            notes=data.notes
        )
        db.add(invoice)
        
        subtotal = Decimal('0')
        for item_data in data.items:
            amount = (Decimal(str(item_data.unit_price)) * item_data.quantity) - Decimal(str(item_data.discount))
            subtotal += amount
            item = InvoiceItem(
                id=uuid.uuid4(),
                invoice_id=invoice.id,
                description=item_data.description,
                treatment_id=item_data.treatment_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                discount=item_data.discount,
                amount=amount
            )
            db.add(item)
            
        invoice.subtotal = subtotal
        invoice.total_amount = subtotal - Decimal(str(data.discount_amount)) + Decimal(str(data.tax_amount))
        invoice.balance = invoice.total_amount
        invoice.status = 'pending'
        
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=data.patient_id,
            event_type="invoice_created",
            title="Invoice Created",
            description=f"Invoice {invoice_number} created for {invoice.total_amount}",
            created_by=user_id
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(invoice)
        return invoice
        
    @staticmethod
    async def get_invoice(db: AsyncSession, invoice_id: uuid.UUID):
        query = select(Invoice).where(Invoice.id == invoice_id).options(selectinload(Invoice.items), selectinload(Invoice.payments))
        invoice = (await db.execute(query)).scalar_one_or_none()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
        
    @staticmethod
    async def record_payment(db: AsyncSession, data: PaymentCreate, user_id: uuid.UUID):
        invoice = await BillingService.get_invoice(db, data.invoice_id)
        
        if data.amount > invoice.balance:
            raise HTTPException(status_code=400, detail="Payment amount exceeds balance")
            
        payment = Payment(
            id=uuid.uuid4(),
            invoice_id=data.invoice_id,
            amount=data.amount,
            payment_method=data.payment_method,
            transaction_reference=data.transaction_reference,
            payment_date=data.payment_date or func.current_date(),
            received_by=user_id,
            notes=data.notes
        )
        db.add(payment)
        
        invoice.amount_paid += Decimal(str(data.amount))
        invoice.balance = invoice.total_amount - invoice.amount_paid
        
        if invoice.balance <= 0:
            invoice.status = 'paid'
        elif invoice.amount_paid > 0:
            invoice.status = 'partially_paid'
            
        event = PatientTimeline(
            id=uuid.uuid4(),
            patient_id=invoice.patient_id,
            event_type="payment_received",
            title="Payment Received",
            description=f"Payment of {data.amount} received for invoice {invoice.invoice_number}",
            created_by=user_id
        )
        db.add(event)
        
        await db.commit()
        return payment
        
    @staticmethod
    async def get_invoices(db: AsyncSession, clinic_id: uuid.UUID, patient_id: uuid.UUID = None, status: str = None, page: int = 1, page_size: int = 20):
        query = select(Invoice).where(Invoice.clinic_id == clinic_id)
        if patient_id:
            query = query.where(Invoice.patient_id == patient_id)
        if status:
            query = query.where(Invoice.status == status)
            
        total_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(total_query)).scalar_one()
        
        query = query.order_by(desc(Invoice.created_at)).offset((page - 1) * page_size).limit(page_size)
        items = (await db.execute(query)).scalars().all()
        
        total_pages = math.ceil(total / page_size) if page_size else 0
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
