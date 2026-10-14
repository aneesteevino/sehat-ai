"""Typed application configuration with production safety checks."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AnyHttpUrl, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or a local `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    frontend_origin: AnyHttpUrl = "http://localhost:3000"  # type: ignore[assignment]
    mongodb_uri: SecretStr | None = None
    mongodb_database: str = "sehat_ai"
    auth_secret: SecretStr | None = None
    session_ttl_minutes: int = 60
    knowledge_registry_path: Path = Path("data/source_registry/sources.json")
    generation_minimum_score: float = 0.13
    generation_timeout_seconds: float = 8.0
    generation_max_attempts: int = 2

    @model_validator(mode="after")
    def require_production_secrets(self) -> "Settings":
        """Fail closed if production starts without its minimum signing secret."""

        if self.app_env == "production":
            if self.auth_secret is None:
                raise ValueError("AUTH_SECRET is required when APP_ENV=production")
            if len(self.auth_secret.get_secret_value()) < 32:
                raise ValueError("AUTH_SECRET must contain at least 32 characters in production")
            if self.mongodb_uri is None:
                raise ValueError("MONGODB_URI is required when APP_ENV=production")
        if not 5 <= self.session_ttl_minutes <= 10_080:
            raise ValueError("SESSION_TTL_MINUTES must be between 5 and 10080")
        if not 0 <= self.generation_minimum_score <= 1:
            raise ValueError("GENERATION_MINIMUM_SCORE must be between 0 and 1")
        if not 0.1 <= self.generation_timeout_seconds <= 60:
            raise ValueError("GENERATION_TIMEOUT_SECONDS must be between 0.1 and 60")
        if not 1 <= self.generation_max_attempts <= 3:
            raise ValueError("GENERATION_MAX_ATTEMPTS must be between 1 and 3")
        return self


@lru_cache
def get_settings() -> Settings:
    """Return one immutable-equivalent settings instance per process."""

    return Settings()
