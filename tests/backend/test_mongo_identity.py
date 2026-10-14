from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from pymongo.errors import DuplicateKeyError
from sehat_api.identity.models import Role, SessionRecord, UserRecord
from sehat_api.repositories.identity import DuplicateEmailError
from sehat_api.repositories.mongo_identity import MongoIdentityRepository


def make_repository() -> MongoIdentityRepository:
    repository = object.__new__(MongoIdentityRepository)
    repository._database = SimpleNamespace(command=AsyncMock())
    repository._users = SimpleNamespace(
        create_index=AsyncMock(),
        insert_one=AsyncMock(),
        find_one=AsyncMock(),
    )
    repository._sessions = SimpleNamespace(
        create_index=AsyncMock(),
        insert_one=AsyncMock(),
        find_one=AsyncMock(),
        update_one=AsyncMock(return_value=SimpleNamespace(modified_count=1)),
    )
    return repository


@pytest.mark.asyncio
async def test_mongo_adapter_installs_unique_lookup_and_ttl_indexes() -> None:
    repository = make_repository()

    await repository.initialize()

    repository._database.command.assert_awaited_once_with("ping")
    user_index_calls = repository._users.create_index.await_args_list
    session_index_calls = repository._sessions.create_index.await_args_list
    assert any(call.args == ("email",) and call.kwargs["unique"] for call in user_index_calls)
    assert any(
        call.args == ("expires_at",) and call.kwargs["expireAfterSeconds"] == 0
        for call in session_index_calls
    )


@pytest.mark.asyncio
async def test_mongo_adapter_round_trips_identity_documents() -> None:
    repository = make_repository()
    now = datetime(2026, 10, 14, tzinfo=UTC)
    user = UserRecord(
        id="user-1",
        email="person@example.com",
        display_name="Person",
        password_hash="$argon2id$test",
        role=Role.PATIENT,
        is_active=True,
        created_at=now,
    )
    session = SessionRecord(
        id="session-1",
        user_id=user.id,
        token_digest="digest",
        created_at=now,
        expires_at=now + timedelta(hours=1),
    )

    await repository.add_user(user)
    await repository.add_session(session)
    user_document = repository._users.insert_one.await_args.args[0]
    session_document = repository._sessions.insert_one.await_args.args[0]

    assert user_document["_id"] == user.id
    assert user_document["role"] == "patient"
    assert "id" not in user_document
    assert repository._user_from_document(user_document) == user
    assert repository._session_from_document(session_document) == session
    assert await repository.revoke_session("digest", now) is True


@pytest.mark.asyncio
async def test_mongo_adapter_translates_duplicate_email_error() -> None:
    repository = make_repository()
    repository._users.insert_one.side_effect = DuplicateKeyError("duplicate")
    user = UserRecord(
        id="user-1",
        email="person@example.com",
        display_name="Person",
        password_hash="$argon2id$test",
        role=Role.PATIENT,
        is_active=True,
        created_at=datetime(2026, 10, 14, tzinfo=UTC),
    )

    with pytest.raises(DuplicateEmailError):
        await repository.add_user(user)
