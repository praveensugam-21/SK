"""
Meridian Dental - Database Seed Script
Creates default clinic, users, sample patients, appointments, and invoices.
Idempotent: skips if data already exists.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.clinic import Clinic
from app.models.user import User
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.dental_chart import TeethRecord
from app.models.billing import Invoice, InvoiceItem
from app.models.patient_timeline import PatientTimeline
from app.utils.security import hash_password
import uuid
from datetime import date, time, datetime, timedelta


# Resolve sync database URL
sync_url = os.environ.get('DATABASE_URL_SYNC')
if not sync_url:
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

engine = create_engine(sync_url)
Session = sessionmaker(bind=engine)


def seed_data():
    session = Session()
    try:
        # Check if already seeded
        admin = session.query(User).filter(User.email == 'admin@meridian.dental').first()
        if admin:
            print("✓ Database already seeded. Skipping.")
            return

        print("Seeding database...")

        # ── Clinic ──
        clinic = Clinic(
            id=uuid.uuid4(),
            name=settings.DEFAULT_CLINIC_NAME,
            address=settings.DEFAULT_CLINIC_ADDRESS,
            phone=settings.DEFAULT_CLINIC_PHONE,
            email=settings.DEFAULT_CLINIC_EMAIL,
        )
        session.add(clinic)
        session.flush()
        print(f"  ✓ Clinic: {clinic.name}")

        # ── Users ──
        admin_user = User(
            id=uuid.uuid4(), clinic_id=clinic.id,
            email='admin@meridian.dental',
            password_hash=hash_password('Admin@123'),
            full_name='Admin', role='admin',
        )
        dr_rahul = User(
            id=uuid.uuid4(), clinic_id=clinic.id,
            email='dentist@meridian.dental',
            password_hash=hash_password('Dentist@123'),
            full_name='Dr. Rahul Sharma', role='dentist',
            specialization='General Dentistry',
            license_number='DEN-KA-2020-1234',
        )
        receptionist = User(
            id=uuid.uuid4(), clinic_id=clinic.id,
            email='receptionist@meridian.dental',
            password_hash=hash_password('Reception@123'),
            full_name='Priya Nair', role='receptionist',
        )
        accountant = User(
            id=uuid.uuid4(), clinic_id=clinic.id,
            email='accountant@meridian.dental',
            password_hash=hash_password('Account@123'),
            full_name='Arun Kumar', role='accountant',
        )
        session.add_all([admin_user, dr_rahul, receptionist, accountant])
        session.flush()
        print("  ✓ Users: Admin, Dr. Rahul, Priya (receptionist), Arun (accountant)")

        # ── Patients ──
        patient_data = [
            {"full_name": "Sadesh Kumar", "phone": "9043205927", "email": "santhoshkumar@gmail.com",
             "date_of_birth": date(2005, 5, 17), "gender": "male",
             "allergies": "None", "medical_history": "Diabetic patient",
             "blood_group": "B+"},
            {"full_name": "Anita Desai", "phone": "9876543210", "email": "anita.desai@gmail.com",
             "date_of_birth": date(1990, 3, 15), "gender": "female",
             "allergies": "Penicillin", "blood_group": "O+"},
            {"full_name": "Vikram Singh", "phone": "9988776655", "email": "vikram.singh@gmail.com",
             "date_of_birth": date(1985, 8, 22), "gender": "male",
             "medical_history": "Hypertension", "blood_group": "A+"},
            {"full_name": "Sunita Sharma", "phone": "9123456789", "email": "sunita.sharma@gmail.com",
             "date_of_birth": date(1978, 11, 30), "gender": "female",
             "allergies": "Latex", "blood_group": "AB+"},
            {"full_name": "Rajesh Patel", "phone": "9556677889", "email": "rajesh.patel@gmail.com",
             "date_of_birth": date(1995, 1, 10), "gender": "male",
             "blood_group": "O-"},
        ]

        patients = []
        for i, pd in enumerate(patient_data):
            p = Patient(
                id=uuid.uuid4(), clinic_id=clinic.id,
                patient_id_display=f"P-{i+1:05d}",
                status="active", **pd,
            )
            patients.append(p)
        session.add_all(patients)
        session.flush()
        print(f"  ✓ Patients: {len(patients)} created")

        # Timeline events for patient registration
        for p in patients:
            session.add(PatientTimeline(
                id=uuid.uuid4(), patient_id=p.id,
                event_type="registration", title="Patient Registered",
                description=f"{p.full_name} registered at the clinic",
                created_by=receptionist.id,
            ))

        # ── Appointments ──
        today = date.today()
        appointments = [
            Appointment(
                id=uuid.uuid4(), clinic_id=clinic.id,
                patient_id=patients[0].id, dentist_id=dr_rahul.id,
                date=today, start_time=time(9, 0), end_time=time(9, 30),
                duration_minutes=30, appointment_type="consultation",
                status="confirmed",
            ),
            Appointment(
                id=uuid.uuid4(), clinic_id=clinic.id,
                patient_id=patients[1].id, dentist_id=dr_rahul.id,
                date=today, start_time=time(10, 0), end_time=time(10, 45),
                duration_minutes=45, appointment_type="cleaning",
                status="scheduled",
            ),
            Appointment(
                id=uuid.uuid4(), clinic_id=clinic.id,
                patient_id=patients[2].id, dentist_id=dr_rahul.id,
                date=today, start_time=time(11, 0), end_time=time(12, 0),
                duration_minutes=60, appointment_type="root_canal",
                status="scheduled",
            ),
        ]
        session.add_all(appointments)
        session.flush()
        print(f"  ✓ Appointments: {len(appointments)} for today")

        # ── Dental Chart (sample teeth for first patient) ──
        tooth_data = [
            {"tooth_number": 6, "condition": "cavity"},
            {"tooth_number": 14, "condition": "filled"},
            {"tooth_number": 19, "condition": "crown"},
            {"tooth_number": 30, "condition": "root_canal"},
        ]
        for td in tooth_data:
            session.add(TeethRecord(
                id=uuid.uuid4(), patient_id=patients[0].id,
                tooth_number=td["tooth_number"], condition=td["condition"],
                surfaces={"mesial": False, "distal": False, "occlusal": True, "buccal": False, "lingual": False},
                updated_by=dr_rahul.id,
            ))
        print("  ✓ Dental chart: sample records for first patient")

        # ── Invoice ──
        inv = Invoice(
            id=uuid.uuid4(), clinic_id=clinic.id,
            patient_id=patients[0].id, invoice_number="INV-00001",
            invoice_date=today, due_date=today + timedelta(days=30),
            subtotal=20500, discount_amount=0, tax_amount=0,
            total_amount=20500, amount_paid=0, balance=20500,
            status="pending",
        )
        session.add(inv)
        session.flush()

        items = [
            InvoiceItem(id=uuid.uuid4(), invoice_id=inv.id, description="Cavity Filling", quantity=1, unit_price=500, discount=0, amount=500),
            InvoiceItem(id=uuid.uuid4(), invoice_id=inv.id, description="Crown Placement", quantity=1, unit_price=5000, discount=0, amount=5000),
            InvoiceItem(id=uuid.uuid4(), invoice_id=inv.id, description="Root Canal Treatment", quantity=1, unit_price=15000, discount=0, amount=15000),
        ]
        session.add_all(items)
        print("  ✓ Invoice: INV-00001 (₹20,500)")

        session.commit()
        print("\n✅ Database seeded successfully!")
        print("   Login credentials:")
        print("     Admin:        admin@meridian.dental / Admin@123")
        print("     Dentist:      dentist@meridian.dental / Dentist@123")
        print("     Receptionist: receptionist@meridian.dental / Reception@123")
        print("     Accountant:   accountant@meridian.dental / Account@123")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()
