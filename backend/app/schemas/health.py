from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Health status", example="healthy")
    timestamp: datetime = Field(..., description="Current server time")
    version: str = Field(..., description="API version", example="1.0.0")
