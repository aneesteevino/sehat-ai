"""Persistence-neutral identity records."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class Role(StrEnum):
    PATIENT = "patient"
    CLINICIAN = "clinician"
    ADMIN = "admin"


@dataclass(frozen=True, slots=True)
class UserRecord:
    id: str
    email: str
    display_name: str
    password_hash: str
    role: Role
    is_active: bool
    created_at: datetime


@dataclass(frozen=True, slots=True)
class SessionRecord:
    id: str
    user_id: str
    token_digest: str
    created_at: datetime
    expires_at: datetime
    revoked_at: datetime | None = None
