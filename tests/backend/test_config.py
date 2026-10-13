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
        auth_secret="not-a-real-secret-for-tests",
        _env_file=None,
    )

    assert settings.auth_secret is not None
    assert str(settings.auth_secret) == "**********"
