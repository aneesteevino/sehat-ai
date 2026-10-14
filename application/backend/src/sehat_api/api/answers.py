"""Authenticated grounded-answer endpoint."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, Field

from sehat_api.api.identity import get_current_user
from sehat_api.api.knowledge import EvidenceResponse
from sehat_api.generation.models import GroundedAnswer
from sehat_api.generation.service import (
    GenerationService,
    GenerationUnavailableError,
    UnsafeProviderOutputError,
)
from sehat_api.identity.models import UserRecord

router = APIRouter(prefix="/api/v1/answers", tags=["answers"])


class AnswerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=2, max_length=500)


class ClaimResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    evidence_ids: list[str]


class UsageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    input_units: int
    output_units: int
    estimated_cost_usd: float
    attempts: int
    duration_ms: int


class EscalationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    categories: list[str]
    message: str
    actions: list[str]


class AnswerResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["answered", "abstained", "escalated"]
    claims: list[ClaimResponse]
    evidence: list[EvidenceResponse]
    uncertainty: str
    safety_notice: str
    abstention_reason: str | None
    escalation: EscalationResponse | None
    usage: UsageResponse

    @classmethod
    def from_answer(cls, answer: GroundedAnswer) -> "AnswerResponse":
        return cls(
            status=answer.status,
            claims=[
                ClaimResponse(text=claim.text, evidence_ids=list(claim.evidence_ids))
                for claim in answer.claims
            ],
            evidence=[EvidenceResponse.from_match(match) for match in answer.evidence],
            uncertainty=answer.uncertainty,
            safety_notice=answer.safety_notice,
            abstention_reason=answer.abstention_reason,
            escalation=(
                EscalationResponse(
                    categories=list(answer.escalation.categories),
                    message=answer.escalation.message,
                    actions=list(answer.escalation.actions),
                )
                if answer.escalation
                else None
            ),
            usage=UsageResponse(
                provider=answer.usage.provider,
                model=answer.usage.model,
                input_units=answer.usage.input_units,
                output_units=answer.usage.output_units,
                estimated_cost_usd=answer.usage.estimated_cost_usd,
                attempts=answer.usage.attempts,
                duration_ms=answer.usage.duration_ms,
            ),
        )


def get_generation_service(request: Request) -> GenerationService:
    return request.app.state.generation_service


@router.post("", response_model=AnswerResponse)
async def answer(
    _user: Annotated[UserRecord, Depends(get_current_user)],
    service: Annotated[GenerationService, Depends(get_generation_service)],
    payload: AnswerRequest,
) -> AnswerResponse:
    try:
        result = await service.answer(payload.question)
    except UnsafeProviderOutputError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The generated answer did not pass safety validation.",
        ) from exc
    except GenerationUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Answer generation is temporarily unavailable.",
        ) from exc
    return AnswerResponse.from_answer(result)
