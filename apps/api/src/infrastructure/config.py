"""Application configuration."""
import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    # App
    APP_NAME: str = "Holocron Career AI"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "local"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/holocron"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Cognito
    COGNITO_USER_POOL_ID: str = "us-east-1_XXXXXXXXX"
    COGNITO_CLIENT_ID: str = "XXXXXXXXXXXXXXXXXXXXXXXXX"
    COGNITO_REGION: str = "us-east-1"
    
    # Bedrock
    BEDROCK_REGION: str = "us-east-1"
    BEDROCK_HAIKU_MODEL: str = "anthropic.claude-3-5-haiku-20241022-v1:0"
    BEDROCK_SONNET_MODEL: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    # ChromaDB (RAG)
    CHROMA_DB_PATH: str = "chromadb"
    CHROMA_DB_COLLECTION: str = "career_jobs"
    
    # Budget
    DAILY_TOKEN_BUDGET: int = 100000
    COST_LIMIT_USD: float = 10.00
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()