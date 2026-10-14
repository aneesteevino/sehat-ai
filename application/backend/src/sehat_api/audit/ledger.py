"""In-memory audit adapter with a strict metadata allow-list."""

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

ALLOWED_METADATA = frozenset({"workflow_kind", "from_state", "to_state", "safety_level"})


@dataclass(frozen=True, slots=True)
class AuditEvent:
    id: str
    occurred_at: datetime
    actor_user_id: str
    action: str
    target_type: str
    target_id: str
    outcome: str
    request_id: str
    metadata: tuple[tuple[str, str], ...]


class InMemoryAuditLedger:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []
        self._lock = asyncio.Lock()

    async def record(
        self,
        *,
        actor_user_id: str,
        action: str,
        target_type: str,
        target_id: str,
        outcome: str,
        request_id: str,
        metadata: dict[str, str],
    ) -> AuditEvent:
        if not set(metadata) <= ALLOWED_METADATA:
            raise ValueError("audit metadata contains a non-allow-listed key")
        event = AuditEvent(
            id=str(uuid4()),
            occurred_at=datetime.now(UTC),
            actor_user_id=actor_user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            outcome=outcome,
            request_id=request_id,
            metadata=tuple(sorted(metadata.items())),
        )
        async with self._lock:
            self._events.append(event)
        return event

    async def list_events(self) -> list[AuditEvent]:
        async with self._lock:
            return list(self._events)
