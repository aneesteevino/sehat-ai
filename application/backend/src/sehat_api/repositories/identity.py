"""Identity repository contract and concurrency-safe local adapter."""

import asyncio
from datetime import datetime
from typing import Protocol

from sehat_api.identity.models import SessionRecord, UserRecord


class DuplicateEmailError(Exception):
    """Raised when a normalized email address already exists."""


class IdentityRepository(Protocol):
    async def add_user(self, user: UserRecord) -> None: ...

    async def get_user_by_id(self, user_id: str) -> UserRecord | None: ...

    async def get_user_by_email(self, email: str) -> UserRecord | None: ...

    async def add_session(self, session: SessionRecord) -> None: ...

    async def get_session_by_digest(self, token_digest: str) -> SessionRecord | None: ...

    async def revoke_session(self, token_digest: str, revoked_at: datetime) -> bool: ...


class InMemoryIdentityRepository:
    """Process-local adapter for development and deterministic tests.

    This adapter is deliberately non-durable. Production startup remains gated on
    explicit secrets and will later select the MongoDB adapter.
    """

    def __init__(self) -> None:
        self._users_by_id: dict[str, UserRecord] = {}
        self._user_ids_by_email: dict[str, str] = {}
        self._sessions_by_digest: dict[str, SessionRecord] = {}
        self._lock = asyncio.Lock()

    async def add_user(self, user: UserRecord) -> None:
        async with self._lock:
            if user.email in self._user_ids_by_email:
                raise DuplicateEmailError
            self._users_by_id[user.id] = user
            self._user_ids_by_email[user.email] = user.id

    async def get_user_by_id(self, user_id: str) -> UserRecord | None:
        return self._users_by_id.get(user_id)

    async def get_user_by_email(self, email: str) -> UserRecord | None:
        user_id = self._user_ids_by_email.get(email)
        return self._users_by_id.get(user_id) if user_id else None

    async def add_session(self, session: SessionRecord) -> None:
        async with self._lock:
            self._sessions_by_digest[session.token_digest] = session

    async def get_session_by_digest(self, token_digest: str) -> SessionRecord | None:
        return self._sessions_by_digest.get(token_digest)

    async def revoke_session(self, token_digest: str, revoked_at: datetime) -> bool:
        from dataclasses import replace

        async with self._lock:
            session = self._sessions_by_digest.get(token_digest)
            if session is None or session.revoked_at is not None:
                return False
            self._sessions_by_digest[token_digest] = replace(session, revoked_at=revoked_at)
            return True
