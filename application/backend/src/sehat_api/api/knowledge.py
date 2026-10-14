"""Authenticated, versioned evidence retrieval endpoint."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from sehat_api.api.identity import get_current_user
from sehat_api.identity.models import UserRecord
from sehat_api.knowledge.models import EvidenceMatch
from sehat_api.knowledge.retrieval import RetrievalService

router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge"])


class CitationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    source_version_id: str
    title: str
    publisher: str
    canonical_url: HttpUrl
    locator: str


class EvidenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    content: str
    score: float = Field(ge=0, le=1)
    content_trust: Literal["untrusted"]
    citation: CitationResponse

    @classmethod
    def from_match(cls, match: EvidenceMatch) -> "EvidenceResponse":
        return cls(
            chunk_id=match.chunk_id,
            content=match.content,
            score=match.score,
            content_trust=match.content_trust,
            citation=CitationResponse(
                source_id=match.citation.source_id,
                source_version_id=match.citation.source_version_id,
                title=match.citation.title,
                publisher=match.citation.publisher,
                canonical_url=match.citation.canonical_url,
                locator=match.citation.locator,
            ),
        )


class SearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    evidence: list[EvidenceResponse]
    generated_answer: None = None
    disclaimer: str = "Evidence retrieval only; no medical answer has been generated."


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=2, max_length=500)
    limit: int = Field(default=5, ge=1, le=20)


def get_retrieval_service(request: Request) -> RetrievalService:
    return request.app.state.retrieval_service


@router.post("/search", response_model=SearchResponse)
async def search(
    _user: Annotated[UserRecord, Depends(get_current_user)],
    service: Annotated[RetrievalService, Depends(get_retrieval_service)],
    payload: SearchRequest,
) -> SearchResponse:
    matches = await service.search(payload.query, limit=payload.limit)
    return SearchResponse(
        query=payload.query,
        evidence=[EvidenceResponse.from_match(match) for match in matches],
    )
