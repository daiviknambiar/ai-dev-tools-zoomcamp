from datetime import datetime
from fastapi import APIRouter, Depends
from app.schemas.health import HealthResponse
from app.config import settings


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current health status of the API.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.app_version,
    )
