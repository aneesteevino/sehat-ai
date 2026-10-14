"""Typed contracts shared by generation providers and the application service."""

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from sehat_api.knowledge.models import EvidenceMatch

ClaimText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=700)
]
UncertaintyText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=400)
]
EvidenceId = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=200,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9:._-]*$",
    ),
]


class ProviderClaim(BaseModel):
    """One provider-authored claim and its proposed evidence references."""

    model_config = ConfigDict(extra="forbid")

    text: ClaimText
    evidence_ids: list[EvidenceId] = Field(min_length=1, max_length=3)


class ProviderAnswer(BaseModel):
    """The only provider output shape accepted by the application."""

    model_config = ConfigDict(extra="forbid")

    claims: list[ProviderClaim] = Field(min_length=1, max_length=4)
    uncertainty: UncertaintyText


@dataclass(frozen=True, slots=True)
class ProviderEvidence:
    id: str
    content: str


@dataclass(frozen=True, slots=True)
class ProviderRequest:
    question: str
    evidence: tuple[ProviderEvidence, ...]


class ProviderUsage(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    input_units: int = Field(ge=0)
    output_units: int = Field(ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0)


@dataclass(frozen=True, slots=True)
class ProviderResult:
    payload: object
    usage: ProviderUsage


@dataclass(frozen=True, slots=True)
class GroundedClaim:
    text: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class UsageRecord:
    id: str
    created_at: datetime
    provider: str
    model: str
    input_units: int
    output_units: int
    estimated_cost_usd: float
    attempts: int
    duration_ms: int
    outcome: Literal["answered", "abstained", "failed"]


@dataclass(frozen=True, slots=True)
class GroundedAnswer:
    status: Literal["answered", "abstained"]
    claims: tuple[GroundedClaim, ...]
    evidence: tuple[EvidenceMatch, ...]
    uncertainty: str
    safety_notice: str
    abstention_reason: str | None
    usage: UsageRecord
