"""
Database configuration and session management using SQLAlchemy.
Supports both PostgreSQL and SQLite.
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# Database URL configuration
# Default to SQLite for development, switch to PostgreSQL if DATABASE_URL env is set
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./snake_game.db"
)

# Adapt postgres:// to postgresql:// for SQLAlchemy 2.0+
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with connection pooling
is_sqlite = "sqlite" in DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    # For SQLite: disable connection pooling and thread checks for async support
    connect_args={"check_same_thread": False} if is_sqlite else {},
    poolclass=StaticPool if is_sqlite else None,
    echo=os.getenv("DEBUG", "false").lower() == "true"
)

# Enable foreign keys for SQLite
if is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """Dependency for FastAPI to inject database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables defined in models."""
    Base.metadata.create_all(bind=engine)
