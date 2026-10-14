import pytest
from pydantic import ValidationError
from sehat_api.config import Settings


def test_development_defaults_do_not_require_secrets() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_env == "development"
    assert settings.auth_secret is None


def test_production_requires_auth_secret() -> None:
    with pytest.raises(ValidationError, match="AUTH_SECRET is required"):
        Settings(app_env="production", auth_secret=None, _env_file=None)


def test_production_accepts_secret_without_exposing_it() -> None:
    settings = Settings(
        app_env="production",
        auth_secret="not-a-real-secret-for-tests-32-characters",
        mongodb_uri="mongodb://localhost:27017",
        _env_file=None,
    )

    assert settings.auth_secret is not None
    assert str(settings.auth_secret) == "**********"


def test_production_rejects_short_auth_secret() -> None:
    with pytest.raises(ValidationError, match="at least 32 characters"):
        Settings(app_env="production", auth_secret="too-short", _env_file=None)


def test_production_requires_durable_persistence() -> None:
    with pytest.raises(ValidationError, match="MONGODB_URI"):
        Settings(
            app_env="production",
            auth_secret="not-a-real-secret-for-tests-32-characters",
            _env_file=None,
        )


def test_session_ttl_has_safe_bounds() -> None:
    with pytest.raises(ValidationError, match="SESSION_TTL_MINUTES"):
        Settings(session_ttl_minutes=4, _env_file=None)
