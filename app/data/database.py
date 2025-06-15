import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from app.config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables first
load_dotenv()

# Get database URL from environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://agrobot:agrobot@localhost:5432/agrobot"
)

# Log the connection URL (without password for security)
from rich import print as rprint

sanitized_url = DATABASE_URL.replace("://", "://***:***@")
rprint(f"[blue]Connecting to database: {sanitized_url}[/blue]")

# Create SQLAlchemy engine with error handling
try:
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db() -> Session:
    """
    Get database session.
    Yields a session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database by creating all tables.
    """
    try:
        # Import all models to ensure they are registered with the Base
        from app.data.models import Robot, Command, TelemetryData, Alert
        from app.data.component.model import Component
        from app.data.action.model import Action, Step

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise
