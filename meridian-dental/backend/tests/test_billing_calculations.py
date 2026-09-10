import pytest
from decimal import Decimal

def test_invoice_calculation():
    # Item 1: Root Canal 1 x 6000 - 500 discount = 5500
    qty1 = 1
    price1 = Decimal('6000.00')
    discount1 = Decimal('500.00')
    item1_amt = (price1 * qty1) - discount1
    
    # Item 2: Crown 2 x 4000 = 8000
    qty2 = 2
    price2 = Decimal('4000.00')
    discount2 = Decimal('0.00')
    item2_amt = (price2 * qty2) - discount2
    
    subtotal = item1_amt + item2_amt
    assert subtotal == Decimal('13500.00')
    
    invoice_discount = Decimal('1000.00')
    tax = Decimal('500.00')
    total = subtotal - invoice_discount + tax
    assert total == Decimal('13000.00')
    
    # Payment 1
    payment1 = Decimal('5000.00')
    balance1 = total - payment1
    assert balance1 == Decimal('8000.00')
    
    # Payment 2 - full settlement
    payment2 = Decimal('8000.00')
    final_balance = balance1 - payment2
    assert final_balance == Decimal('0.00')

def test_payment_status_transitions():
    total_amount = Decimal('10000.00')
    amount_paid = Decimal('0.00')
    
    # Initial status
    status = 'pending' if amount_paid == 0 else 'partially_paid'
    assert status == 'pending'
    
    # Partial payment
    amount_paid += Decimal('4000.00')
    balance = total_amount - amount_paid
    if balance <= 0:
        status = 'paid'
    elif amount_paid > 0:
        status = 'partially_paid'
    assert status == 'partially_paid'
    assert balance == Decimal('6000.00')
    
    # Complete payment
    amount_paid += Decimal('6000.00')
    balance = total_amount - amount_paid
    if balance <= 0:
        status = 'paid'
    elif amount_paid > 0:
        status = 'partially_paid'
    assert status == 'paid'
    assert balance == Decimal('0.00')
