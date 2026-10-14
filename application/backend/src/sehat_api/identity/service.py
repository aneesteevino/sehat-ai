"""Password, session, and role policy implementation."""

import hashlib
import hmac
import secrets
from asyncio import to_thread
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from pwdlib import PasswordHash

from sehat_api.identity.models import Role, SessionRecord, UserRecord
from sehat_api.repositories.identity import DuplicateEmailError, IdentityRepository


class InvalidCredentialsError(Exception):
    """Credentials failed without revealing which field was incorrect."""


class InactiveUserError(Exception):
    """The identity exists but is not permitted to sign in."""


class InvalidSessionError(Exception):
    """The bearer token is absent, expired, revoked, or unknown."""


class IdentityService:
    def __init__(
        self,
        repository: IdentityRepository,
        secret: bytes,
        session_ttl: timedelta,
        *,
        clock: Callable[[], datetime] | None = None,
        token_factory: Callable[[], str] | None = None,
    ) -> None:
        self.repository = repository
        self._secret = secret
        self._session_ttl = session_ttl
        self._clock = clock or (lambda: datetime.now(UTC))
        self._token_factory = token_factory or (lambda: secrets.token_urlsafe(32))
        self._passwords = PasswordHash.recommended()
        self._dummy_hash = self._passwords.hash("not-a-real-user-password")

    @staticmethod
    def normalize_email(email: str) -> str:
        return email.strip().casefold()

    def digest_token(self, token: str) -> str:
        return hmac.new(self._secret, token.encode(), hashlib.sha256).hexdigest()

    async def register(self, email: str, display_name: str, password: str) -> UserRecord:
        now = self._clock()
        user = UserRecord(
            id=str(uuid4()),
            email=self.normalize_email(email),
            display_name=display_name.strip(),
            password_hash=await to_thread(self._passwords.hash, password),
            role=Role.PATIENT,
            is_active=True,
            created_at=now,
        )
        await self.repository.add_user(user)
        return user

    async def sign_in(self, email: str, password: str) -> tuple[UserRecord, str, SessionRecord]:
        user = await self.repository.get_user_by_email(self.normalize_email(email))
        password_hash = user.password_hash if user else self._dummy_hash
        password_matches = await to_thread(self._passwords.verify, password, password_hash)
        if user is None or not password_matches:
            raise InvalidCredentialsError
        if not user.is_active:
            raise InactiveUserError

        token = self._token_factory()
        now = self._clock()
        session = SessionRecord(
            id=str(uuid4()),
            user_id=user.id,
            token_digest=self.digest_token(token),
            created_at=now,
            expires_at=now + self._session_ttl,
        )
        await self.repository.add_session(session)
        return user, token, session

    async def authenticate(self, token: str) -> UserRecord:
        session = await self.repository.get_session_by_digest(self.digest_token(token))
        now = self._clock()
        if session is None or session.revoked_at is not None or session.expires_at <= now:
            raise InvalidSessionError
        user = await self.repository.get_user_by_id(session.user_id)
        if user is None or not user.is_active:
            raise InvalidSessionError
        return user

    async def sign_out(self, token: str) -> None:
        await self.repository.revoke_session(self.digest_token(token), self._clock())


__all__ = [
    "DuplicateEmailError",
    "IdentityService",
    "InactiveUserError",
    "InvalidCredentialsError",
    "InvalidSessionError",
]
