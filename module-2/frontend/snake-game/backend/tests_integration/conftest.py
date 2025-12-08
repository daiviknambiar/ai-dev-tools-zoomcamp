"""
Conftest for pytest: sets up test database fixtures.
Uses SQLite in-memory database for fast, isolated tests.
"""

import pytest
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Import before app imports to set test DB
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from models import Base, User, LeaderboardEntry, Game
from main import app, get_db


@pytest.fixture(scope="function")
def test_db():
    """Create and drop in-memory SQLite database for each test."""
    # Create engine with connection pooling disabled and thread check off
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(test_db):
    """Provide a FastAPI test client with test database."""
    return TestClient(app)
