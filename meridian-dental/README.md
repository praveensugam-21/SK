# Meridian Dental — Clinic Management System

A production-ready dental clinic management system built with Next.js, FastAPI, and PostgreSQL.

## Architecture

```
Frontend (Next.js + TypeScript + Tailwind)
    ↓ HTTPS
Backend API (FastAPI + Python)
    ↓
Service Layer → Repository Layer → PostgreSQL
    ↓
Object Storage (MinIO/S3) for documents
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, React 18, Tailwind CSS |
| Backend | Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Storage | MinIO (S3-compatible) |
| Containers | Docker, Docker Compose |

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Run with Docker

```bash
# Clone and configure
cp .env.example .env

# Start all services
docker-compose up --build

# Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# MinIO Console: http://localhost:9001
```

### Default Login
- **Admin**: admin@meridian.dental / Admin@123
- **Dentist**: dentist@meridian.dental / Dentist@123
- **Receptionist**: receptionist@meridian.dental / Reception@123

### Database Migrations

```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Run migrations
docker-compose exec backend alembic upgrade head

# Seed data
docker-compose exec backend python -m seeds.seed
```

### Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Project Structure

```
meridian-dental/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── routers/      # API route handlers
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access
│   │   └── utils/        # Helpers (security, PDF, storage)
│   ├── alembic/          # Database migrations
│   ├── seeds/            # Development seed data
│   └── tests/            # Backend tests
├── frontend/             # Next.js frontend
│   ├── app/              # App Router pages
│   ├── components/       # React components
│   ├── lib/              # API client, auth, utils
│   ├── hooks/            # Custom hooks
│   └── types/            # TypeScript interfaces
├── docker-compose.yml
└── .env.example
```

## API Documentation

Once running, visit http://localhost:8000/docs for interactive Swagger UI.

## Security

- JWT authentication with httpOnly cookies
- Role-based access control (Admin, Dentist, Receptionist, Accountant)
- bcrypt password hashing
- Rate limiting on auth endpoints
- CORS configuration
- SQL injection protection (SQLAlchemy parameterized queries)
- XSS protection (React auto-escaping + CSP headers)
- File upload validation
- Audit logging for sensitive operations
