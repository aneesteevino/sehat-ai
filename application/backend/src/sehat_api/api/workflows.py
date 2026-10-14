"""Authenticated deterministic safety and workflow endpoints."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from sehat_api.api.identity import get_current_user
from sehat_api.audit.ledger import InMemoryAuditLedger
from sehat_api.identity.models import UserRecord
from sehat_api.safety.policy import RedFlagPolicy
from sehat_api.workflows.service import (
    IdempotencyConflictError,
    InvalidTransitionError,
    WorkflowNotFoundError,
    WorkflowRecord,
    WorkflowService,
)

router = APIRouter(prefix="/api/v1", tags=["controlled-workflows"])
IdempotencyKey = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=100,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$",
    ),
]


class SafetyCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=2, max_length=500)


class SafetyCheckResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    level: Literal["continue", "emergency"]
    categories: list[str]
    message: str
    actions: list[str]
    provider_bypassed: bool = True


class WorkflowStartRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["symptom_questionnaire", "document_explanation"]
    idempotency_key: IdempotencyKey


class WorkflowTransitionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["begin", "submit", "complete", "cancel"]
    idempotency_key: IdempotencyKey
    payload: dict[str, object] | None = None


class WorkflowResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    kind: str
    state: str
    summary: list[str]

    @classmethod
    def from_record(cls, record: WorkflowRecord) -> "WorkflowResponse":
        return cls(
            id=record.id,
            kind=record.kind,
            state=record.state,
            summary=list(record.summary),
        )


def get_workflow_service(request: Request) -> WorkflowService:
    return request.app.state.workflow_service


def get_safety_policy(request: Request) -> RedFlagPolicy:
    return request.app.state.safety_policy


def get_audit_ledger(request: Request) -> InMemoryAuditLedger:
    return request.app.state.audit_ledger


@router.post("/safety/check", response_model=SafetyCheckResponse)
async def safety_check(
    payload: SafetyCheckRequest,
    request: Request,
    user: Annotated[UserRecord, Depends(get_current_user)],
    policy: Annotated[RedFlagPolicy, Depends(get_safety_policy)],
    audit: Annotated[InMemoryAuditLedger, Depends(get_audit_ledger)],
) -> SafetyCheckResponse:
    decision = policy.evaluate(payload.text)
    await audit.record(
        actor_user_id=user.id,
        action="safety.checked",
        target_type="safety_check",
        target_id=request.state.request_id,
        outcome=decision.level,
        request_id=request.state.request_id,
        metadata={"safety_level": decision.level},
    )
    return SafetyCheckResponse(
        level=decision.level,
        categories=list(decision.categories),
        message=decision.message,
        actions=list(decision.actions),
    )


@router.post("/workflows", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def start_workflow(
    payload: WorkflowStartRequest,
    request: Request,
    user: Annotated[UserRecord, Depends(get_current_user)],
    service: Annotated[WorkflowService, Depends(get_workflow_service)],
) -> WorkflowResponse:
    try:
        record = await service.start(
            owner_user_id=user.id,
            kind=payload.kind,
            idempotency_key=payload.idempotency_key,
            request_id=request.state.request_id,
        )
    except IdempotencyConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return WorkflowResponse.from_record(record)


@router.post("/workflows/{workflow_id}/transitions", response_model=WorkflowResponse)
async def transition_workflow(
    workflow_id: str,
    payload: WorkflowTransitionRequest,
    request: Request,
    user: Annotated[UserRecord, Depends(get_current_user)],
    service: Annotated[WorkflowService, Depends(get_workflow_service)],
) -> WorkflowResponse:
    try:
        record = await service.transition(
            owner_user_id=user.id,
            workflow_id=workflow_id,
            action=payload.action,
            idempotency_key=payload.idempotency_key,
            request_id=request.state.request_id,
            payload=payload.payload,
        )
    except WorkflowNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workflow not found.") from exc
    except (InvalidTransitionError, IdempotencyConflictError) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return WorkflowResponse.from_record(record)
