import uuid
from sqlalchemy import Column, String, Text, Date, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import TimestampMixin, SoftDeleteMixin, Base

class Invoice(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"))
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    subtotal = Column(Numeric(12, 2), default=0)
    discount_amount = Column(Numeric(12, 2), default=0)
    tax_amount = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), default=0)
    amount_paid = Column(Numeric(12, 2), default=0)
    balance = Column(Numeric(12, 2), default=0)
    status = Column(String(20), default='pending')
    notes = Column(Text, nullable=True)
    
    patient = relationship("Patient", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice")

class InvoiceItem(Base, TimestampMixin):
    __tablename__ = "invoice_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False)
    treatment_id = Column(UUID(as_uuid=True), nullable=True) # Avoiding strict FK to prevent circular dependency for now
    description = Column(String(500), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False)
    discount = Column(Numeric(12, 2), default=0)
    amount = Column(Numeric(12, 2), nullable=False)
    
    invoice = relationship("Invoice", back_populates="items")

class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    transaction_reference = Column(String(200), nullable=True)
    payment_date = Column(Date, nullable=False)
    received_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    notes = Column(Text, nullable=True)
    
    invoice = relationship("Invoice", back_populates="payments")
