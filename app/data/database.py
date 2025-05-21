import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Get database URL from environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://agrobot:agrobot@localhost:5432/agrobot"
)

# Log the connection URL (without password for security)
from rich import print as rprint

sanitized_url = DATABASE_URL.replace(
    ":" + DATABASE_URL.split(":")[-2].split("@")[0] + "@",
    ":***@",
)
rprint(f"[blue]Connecting to database: {sanitized_url}[/blue]")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get a database session.
    Ensures session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database schema"""
    # Don't import modules at the top level to avoid circular imports
    # Import them here when needed
    import importlib

    # Import all model modules to ensure they're registered with SQLAlchemy
    for module in ["robot", "action", "component", "step"]:
        importlib.import_module(f"app.data.{module}.model")

    Base.metadata.create_all(bind=engine)
