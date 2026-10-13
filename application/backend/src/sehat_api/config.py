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

    @model_validator(mode="after")
    def require_production_secrets(self) -> "Settings":
        """Fail closed if production starts without its minimum signing secret."""

        if self.app_env == "production" and self.auth_secret is None:
            raise ValueError("AUTH_SECRET is required when APP_ENV=production")
        return self


@lru_cache
def get_settings() -> Settings:
    """Return one immutable-equivalent settings instance per process."""

    return Settings()
