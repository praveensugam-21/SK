from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers import auth, patients, dental_chart, appointments, treatments, billing, prescriptions, notes, documents, dashboard, reports, audit_logs, users
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(dental_chart.router)
app.include_router(appointments.router)
app.include_router(treatments.router)
app.include_router(billing.router)
app.include_router(prescriptions.router)
app.include_router(notes.router)
app.include_router(documents.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(audit_logs.router)
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.on_event("startup")
async def startup():
    logger.info(f"{settings.APP_NAME} starting up...")
