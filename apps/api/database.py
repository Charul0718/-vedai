import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic_settings import BaseSettings

logger = logging.getLogger("vedai.database")

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./vedai.db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_vedai_key_for_jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    PDF_OUTPUT_DIR: str = os.getenv("PDF_OUTPUT_DIR", "./static/reports")
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure PDF directory exists
os.makedirs(settings.PDF_OUTPUT_DIR, exist_ok=True)

# Set database engine parameters
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.exception(f"Failed to create database engine: {str(e)}")
    raise e

Base = declarative_base()

def get_db():
    """Dependency Injection helper for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
