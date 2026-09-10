# SK - Meridian Dental Clinic Management System

A full-stack, enterprise-grade Dental Clinic Management System built with Next.js 14, FastAPI, PostgreSQL, Redis, MinIO, and Docker Compose.

## ?? Features
- **Interactive Dental Chart (Odontogram)**: Universal 32-tooth numbering with real-time condition tracking (Cavity, Filled, Crown, Root Canal, Missing, Healthy).
- **Patient Management**: Full patient profile, medical history, clinical notes, prescriptions, and timeline events.
- **Appointment Scheduling**: Visual calendar, conflict detection, and quick check-in.
- **Billing & Payments**: Dynamic multi-item invoice builder with UPI, Cash, Card, and Bank Transfer payment recording.
- **Role-Based Access Control**: Admin, Dentist, Receptionist, and Accountant workflows.

## ??? Tech Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons, Recharts
- **Backend**: FastAPI, SQLAlchemy Async, Alembic, Pydantic, Python-JOSE
- **Database & Storage**: PostgreSQL 16, Redis 7, MinIO Object Storage
- **Orchestration**: Docker Compose

## ?? Getting Started
```bash
cd meridian-dental
docker compose up -d
```
