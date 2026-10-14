"""Typed application configuration with production safety checks."""

from functools import lru_cache
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
        return self


@lru_cache
def get_settings() -> Settings:
    """Return one immutable-equivalent settings instance per process."""

    return Settings()
