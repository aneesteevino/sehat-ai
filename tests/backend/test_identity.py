from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException
from sehat_api.api.identity import require_roles
from sehat_api.identity.models import Role, UserRecord
from sehat_api.identity.service import (
    IdentityService,
    InvalidCredentialsError,
    InvalidSessionError,
)
from sehat_api.repositories.identity import DuplicateEmailError, InMemoryIdentityRepository


def make_service(
    repository: InMemoryIdentityRepository,
    now: datetime,
) -> IdentityService:
    return IdentityService(
        repository,
        secret=b"test-secret-that-is-long-enough-32-bytes",
        session_ttl=timedelta(hours=1),
        clock=lambda: now,
        token_factory=lambda: "deterministic-test-token",
    )


@pytest.mark.asyncio
async def test_registration_hashes_password_and_normalizes_email() -> None:
    repository = InMemoryIdentityRepository()
    service = make_service(repository, datetime(2026, 10, 14, tzinfo=UTC))

    user = await service.register(" Person@Example.COM ", "Aneesa", "long-test-password")

    assert user.email == "person@example.com"
    assert user.password_hash != "long-test-password"
    assert user.password_hash.startswith("$argon2id$")
    assert user.role is Role.PATIENT


@pytest.mark.asyncio
async def test_duplicate_normalized_email_is_rejected() -> None:
    repository = InMemoryIdentityRepository()
    service = make_service(repository, datetime(2026, 10, 14, tzinfo=UTC))
    await service.register("person@example.com", "First", "long-test-password")

    with pytest.raises(DuplicateEmailError):
        await service.register("PERSON@example.com", "Second", "another-password")


@pytest.mark.asyncio
async def test_sign_in_authenticate_and_revoke_session() -> None:
    repository = InMemoryIdentityRepository()
    service = make_service(repository, datetime(2026, 10, 14, tzinfo=UTC))
    user = await service.register("person@example.com", "Aneesa", "long-test-password")

    signed_in_user, token, session = await service.sign_in(
        "person@example.com", "long-test-password"
    )

    assert signed_in_user == user
    assert token == "deterministic-test-token"
    assert session.token_digest != token
    assert await service.authenticate(token) == user

    await service.sign_out(token)
    with pytest.raises(InvalidSessionError):
        await service.authenticate(token)


@pytest.mark.asyncio
async def test_bad_password_uses_generic_credentials_failure() -> None:
    repository = InMemoryIdentityRepository()
    service = make_service(repository, datetime(2026, 10, 14, tzinfo=UTC))
    await service.register("person@example.com", "Aneesa", "long-test-password")

    with pytest.raises(InvalidCredentialsError):
        await service.sign_in("person@example.com", "wrong-password")
    with pytest.raises(InvalidCredentialsError):
        await service.sign_in("missing@example.com", "wrong-password")


@pytest.mark.asyncio
async def test_expired_session_is_rejected() -> None:
    repository = InMemoryIdentityRepository()
    initial = datetime(2026, 10, 14, tzinfo=UTC)
    current = initial
    service = IdentityService(
        repository,
        secret=b"test-secret-that-is-long-enough-32-bytes",
        session_ttl=timedelta(minutes=5),
        clock=lambda: current,
        token_factory=lambda: "expiring-token",
    )
    await service.register("person@example.com", "Aneesa", "long-test-password")
    _, token, _ = await service.sign_in("person@example.com", "long-test-password")
    current = initial + timedelta(minutes=6)

    with pytest.raises(InvalidSessionError):
        await service.authenticate(token)


@pytest.mark.asyncio
async def test_role_policy_denies_patient_and_allows_admin() -> None:
    authorize_admin = require_roles(Role.ADMIN)
    patient = UserRecord(
        id="patient-1",
        email="patient@example.com",
        display_name="Patient",
        password_hash="not-used",
        role=Role.PATIENT,
        is_active=True,
        created_at=datetime(2026, 10, 14, tzinfo=UTC),
    )
    admin = UserRecord(
        id="admin-1",
        email="admin@example.com",
        display_name="Admin",
        password_hash="not-used",
        role=Role.ADMIN,
        is_active=True,
        created_at=datetime(2026, 10, 14, tzinfo=UTC),
    )

    with pytest.raises(HTTPException) as denied:
        await authorize_admin(patient)
    assert denied.value.status_code == 403
    assert await authorize_admin(admin) == admin
