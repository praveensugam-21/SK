import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

# Look for .env in current dir, backend dir, or project root
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
project_root = backend_dir.parent
env_files = [
    str(backend_dir / ".env"),
    str(project_root / ".env"),
    ".env",
]

class Settings(BaseSettings):
    APP_NAME: str = "Meridian Dental API"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    DATABASE_URL: str = "postgresql+asyncpg://meridian:meridian_secret@localhost:5432/meridian_dental"
    DATABASE_URL_SYNC: str = "postgresql://meridian:meridian_secret@localhost:5432/meridian_dental"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    JWT_SECRET_KEY: str = "meridian-secret-key-change-in-production-min-32-chars!!"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    S3_ENDPOINT: str | None = "http://localhost:9000"
    S3_ACCESS_KEY: str | None = "minioadmin"
    S3_SECRET_KEY: str | None = "minioadmin123"
    S3_BUCKET_NAME: str | None = "meridian-dental"
    S3_REGION: str | None = "us-east-1"
    
    DEFAULT_CLINIC_NAME: str = "Meridian Dental"
    DEFAULT_CLINIC_PHONE: str = "+91-9876543210"
    DEFAULT_CLINIC_EMAIL: str = "info@meridian.dental"
    DEFAULT_CLINIC_ADDRESS: str = "123 Dental Street, Chennai, Tamil Nadu 600001"
    
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=tuple(env_files),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

