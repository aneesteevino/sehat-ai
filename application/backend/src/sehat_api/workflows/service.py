"""Explicit, owner-scoped workflow transitions with idempotent mutations."""

import asyncio
import hashlib
import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from sehat_api.audit.ledger import InMemoryAuditLedger

WorkflowKind = Literal["symptom_questionnaire", "document_explanation"]
WorkflowState = Literal["started", "collecting", "review", "completed", "cancelled"]
WorkflowAction = Literal["begin", "submit", "complete", "cancel"]


class WorkflowNotFoundError(LookupError):
    pass


class InvalidTransitionError(ValueError):
    pass


class IdempotencyConflictError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class WorkflowRecord:
    id: str
    owner_user_id: str
    kind: WorkflowKind
    state: WorkflowState
    summary: tuple[str, ...]
    created_at: datetime
    updated_at: datetime


class WorkflowService:
    _transitions = {
        ("started", "begin"): "collecting",
        ("collecting", "submit"): "review",
        ("review", "complete"): "completed",
        ("started", "cancel"): "cancelled",
        ("collecting", "cancel"): "cancelled",
        ("review", "cancel"): "cancelled",
    }
    _concerns = {"breathing", "chest", "neurological", "fever", "digestive", "other"}
    _durations = {"today", "days", "weeks", "longer"}
    _severities = {"mild", "moderate", "severe"}

    def __init__(self, audit: InMemoryAuditLedger) -> None:
        self._audit = audit
        self._workflows: dict[str, WorkflowRecord] = {}
        self._idempotency: dict[tuple[str, str], tuple[str, WorkflowRecord]] = {}
        self._lock = asyncio.Lock()

    async def start(
        self,
        *,
        owner_user_id: str,
        kind: WorkflowKind,
        idempotency_key: str,
        request_id: str,
    ) -> WorkflowRecord:
        fingerprint = self._fingerprint("start", kind)
        async with self._lock:
            replay = self._replay(owner_user_id, idempotency_key, fingerprint)
            if replay is not None:
                return replay
            now = datetime.now(UTC)
            record = WorkflowRecord(
                id=str(uuid4()),
                owner_user_id=owner_user_id,
                kind=kind,
                state="started",
                summary=(),
                created_at=now,
                updated_at=now,
            )
            self._workflows[record.id] = record
            self._idempotency[(owner_user_id, idempotency_key)] = (fingerprint, record)
        await self._audit.record(
            actor_user_id=owner_user_id,
            action="workflow.started",
            target_type="workflow",
            target_id=record.id,
            outcome="success",
            request_id=request_id,
            metadata={"workflow_kind": kind, "to_state": "started"},
        )
        return record

    async def transition(
        self,
        *,
        owner_user_id: str,
        workflow_id: str,
        action: WorkflowAction,
        idempotency_key: str,
        request_id: str,
        payload: dict[str, object] | None = None,
    ) -> WorkflowRecord:
        data = payload or {}
        fingerprint = self._fingerprint(workflow_id, action, data)
        async with self._lock:
            replay = self._replay(owner_user_id, idempotency_key, fingerprint)
            if replay is not None:
                return replay
            current = self._workflows.get(workflow_id)
            if current is None or current.owner_user_id != owner_user_id:
                raise WorkflowNotFoundError("workflow not found")
            next_state = self._transitions.get((current.state, action))
            if next_state is None:
                raise InvalidTransitionError("transition is not allowed")
            summary = current.summary
            if action == "submit":
                summary = self._validate_submission(current.kind, data)
            updated = replace(
                current,
                state=next_state,  # type: ignore[arg-type]
                summary=summary,
                updated_at=datetime.now(UTC),
            )
            self._workflows[workflow_id] = updated
            self._idempotency[(owner_user_id, idempotency_key)] = (fingerprint, updated)
        await self._audit.record(
            actor_user_id=owner_user_id,
            action=f"workflow.{action}",
            target_type="workflow",
            target_id=workflow_id,
            outcome="success",
            request_id=request_id,
            metadata={
                "workflow_kind": current.kind,
                "from_state": current.state,
                "to_state": next_state,
            },
        )
        return updated

    def _replay(
        self, owner_user_id: str, key: str, fingerprint: str
    ) -> WorkflowRecord | None:
        stored = self._idempotency.get((owner_user_id, key))
        if stored is None:
            return None
        if stored[0] != fingerprint:
            raise IdempotencyConflictError("idempotency key was reused for another mutation")
        return stored[1]

    def _validate_submission(
        self, kind: WorkflowKind, data: dict[str, object]
    ) -> tuple[str, ...]:
        if kind == "symptom_questionnaire":
            concern = data.get("concern")
            duration = data.get("duration")
            severity = data.get("severity")
            if (
                concern not in self._concerns
                or duration not in self._durations
                or severity not in self._severities
                or set(data) != {"concern", "duration", "severity"}
            ):
                raise InvalidTransitionError("questionnaire selections are invalid")
            return (f"concern:{concern}", f"duration:{duration}", f"severity:{severity}")
        if data.get("synthetic") is not True or set(data) != {"synthetic", "facts"}:
            raise InvalidTransitionError("document facts must be explicitly synthetic")
        facts = data.get("facts")
        if not isinstance(facts, list) or not 1 <= len(facts) <= 10:
            raise InvalidTransitionError("one to ten synthetic facts are required")
        summary: list[str] = []
        for fact in facts:
            if not isinstance(fact, dict) or set(fact) != {"label", "value"}:
                raise InvalidTransitionError("synthetic fact shape is invalid")
            label, value = fact.get("label"), fact.get("value")
            if not isinstance(label, str) or not isinstance(value, str):
                raise InvalidTransitionError("synthetic fact values must be text")
            if not 1 <= len(label.strip()) <= 80 or not 1 <= len(value.strip()) <= 200:
                raise InvalidTransitionError("synthetic fact values are out of bounds")
            summary.append(f"{label.strip()}: {value.strip()}")
        return tuple(summary)

    @staticmethod
    def _fingerprint(*parts: object) -> str:
        encoded = json.dumps(parts, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(encoded.encode()).hexdigest()
