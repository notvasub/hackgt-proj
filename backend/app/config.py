from __future__ import annotations

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_env: str = Field(default="local", alias="APP_ENV")
    app_port: int = Field(default=8080, alias="APP_PORT")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")

    # Supabase
    supabase_url: str | None = Field(default=None, alias="SUPABASE_URL")
    supabase_anon_key: str | None = Field(default=None, alias="SUPABASE_ANON_KEY")
    supabase_service_role_key: str | None = Field(default=None, alias="SUPABASE_SERVICE_ROLE_KEY")
    supabase_jwks_url: str | None = Field(default=None, alias="SUPABASE_JWKS_URL")
    supabase_storage_bucket: str = Field(default="claims", alias="SUPABASE_STORAGE_BUCKET")

    # Email
    email_provider: str = Field(default="postmark", alias="EMAIL_PROVIDER")
    postmark_api_token: str | None = Field(default=None, alias="POSTMARK_API_TOKEN")

    # PDF
    pdf_engine: str = Field(default="weasyprint", alias="PDF_ENGINE")

    # AI
    ai_provider: str = Field(default="openai", alias="AI_PROVIDER")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,https://staging.frontend.app,https://frontend.app",
        alias="CORS_ORIGINS",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

