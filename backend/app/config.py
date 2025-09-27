"""Application configuration settings."""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/claimmax_ai"
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-vision-preview"
    
    # AWS
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "claimmax-ai-files"
    
    # Application
    environment: str = "development"
    debug: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # File Upload
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "gif", "pdf"]
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("allowed_extensions", pre=True)
    def parse_allowed_extensions(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()