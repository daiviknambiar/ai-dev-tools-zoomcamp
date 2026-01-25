from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application
    app_name: str = "NBA Stats & Betting Odds API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # CORS
    cors_origins: list[str] = [
        "http://localhost:8501",  # Streamlit local
        "http://localhost:3000",  # Alternative frontend
        "https://*.streamlit.app",  # Streamlit Cloud
    ]
    
    # External APIs
    balldontlie_api_url: str = "https://api.balldontlie.io/v1"
    balldontlie_api_key: Optional[str] = None
    
    # HTTP Client
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 1
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
