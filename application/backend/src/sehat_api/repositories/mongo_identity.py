"""Conditional MongoDB Atlas identity adapter.

The adapter is constructed only when ``MONGODB_URI`` is configured. Unit tests use
the in-memory repository and never require a network connection.
"""

import asyncio
from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any

from pymongo import AsyncMongoClient
from pymongo.errors import DuplicateKeyError

from sehat_api.identity.models import Role, SessionRecord, UserRecord
from sehat_api.repositories.identity import DuplicateEmailError


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


class MongoIdentityRepository:
    """PyMongo Async implementation of the identity repository contract."""

    def __init__(self, client: AsyncMongoClient[dict[str, Any]], database_name: str) -> None:
        self._client = client
        database = client[database_name]
        self._database = database
        self._users = database["users"]
        self._sessions = database["sessions"]

    @classmethod
    def from_uri(cls, uri: str, database_name: str) -> "MongoIdentityRepository":
        client: AsyncMongoClient[dict[str, Any]] = AsyncMongoClient(
            uri,
            tz_aware=True,
            serverSelectionTimeoutMS=5_000,
            connectTimeoutMS=5_000,
        )
        return cls(client, database_name)

    async def initialize(self) -> None:
        """Verify connectivity and install the minimum identity indexes."""

        await self.healthcheck()
        await asyncio.gather(
            self._users.create_index("email", unique=True, name="users_email_unique"),
            self._users.create_index("created_at", name="users_created_at"),
            self._sessions.create_index(
                "token_digest", unique=True, name="sessions_token_digest_unique"
            ),
            self._sessions.create_index("user_id", name="sessions_user_id"),
            self._sessions.create_index(
                "expires_at",
                expireAfterSeconds=0,
                name="sessions_expiry_ttl",
            ),
        )

    async def healthcheck(self) -> None:
        await self._database.command("ping")

    async def close(self) -> None:
        await self._client.close()

    async def add_user(self, user: UserRecord) -> None:
        document = asdict(user)
        document["_id"] = document.pop("id")
        document["role"] = user.role.value
        try:
            await self._users.insert_one(document)
        except DuplicateKeyError as exc:
            raise DuplicateEmailError from exc

    async def get_user_by_id(self, user_id: str) -> UserRecord | None:
        return self._user_from_document(await self._users.find_one({"_id": user_id}))

    async def get_user_by_email(self, email: str) -> UserRecord | None:
        return self._user_from_document(await self._users.find_one({"email": email}))

    async def add_session(self, session: SessionRecord) -> None:
        document = asdict(session)
        document["_id"] = document.pop("id")
        await self._sessions.insert_one(document)

    async def get_session_by_digest(self, token_digest: str) -> SessionRecord | None:
        return self._session_from_document(
            await self._sessions.find_one({"token_digest": token_digest})
        )

    async def revoke_session(self, token_digest: str, revoked_at: datetime) -> bool:
        result = await self._sessions.update_one(
            {"token_digest": token_digest, "revoked_at": None},
            {"$set": {"revoked_at": revoked_at}},
        )
        return result.modified_count == 1

    @staticmethod
    def _user_from_document(document: dict[str, Any] | None) -> UserRecord | None:
        if document is None:
            return None
        return UserRecord(
            id=str(document["_id"]),
            email=document["email"],
            display_name=document["display_name"],
            password_hash=document["password_hash"],
            role=Role(document["role"]),
            is_active=document["is_active"],
            created_at=_utc(document["created_at"]),
        )

    @staticmethod
    def _session_from_document(document: dict[str, Any] | None) -> SessionRecord | None:
        if document is None:
            return None
        return SessionRecord(
            id=str(document["_id"]),
            user_id=document["user_id"],
            token_digest=document["token_digest"],
            created_at=_utc(document["created_at"]),
            expires_at=_utc(document["expires_at"]),
            revoked_at=_utc(document["revoked_at"]) if document["revoked_at"] else None,
        )
