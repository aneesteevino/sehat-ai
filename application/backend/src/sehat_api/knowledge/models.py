"""Persistence-neutral knowledge and evidence contracts."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class RegistrySource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{2,63}$")
    title: str = Field(min_length=1, max_length=200)
    publisher: str = Field(min_length=1, max_length=120)
    canonical_url: HttpUrl
    source_updated_at: date
    retrieved_at: date
    license_name: str = Field(min_length=1, max_length=120)
    license_url: HttpUrl
    attribution: str = Field(min_length=1, max_length=300)
    non_endorsement: str = Field(min_length=1, max_length=500)
    fixture_path: str = Field(pattern=r"^[A-Za-z0-9._/-]+$")
    content_type: Literal["text/plain", "application/pdf"]
    expected_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    status: Literal["approved_for_evaluation", "disabled"]


class SourceRegistry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    registry_version: int = Field(ge=1)
    sources: list[RegistrySource]


@dataclass(frozen=True, slots=True)
class ExtractedSection:
    text: str
    page_number: int | None


@dataclass(frozen=True, slots=True)
class SourceVersion:
    id: str
    source_id: str
    content_sha256: str
    source_updated_at: date
    retrieved_at: date
    ingested_at: datetime


@dataclass(frozen=True, slots=True)
class KnowledgeChunk:
    id: str
    source_id: str
    source_version_id: str
    content: str
    content_sha256: str
    chunk_index: int
    page_number: int | None
    paragraph_start: int
    paragraph_end: int
    embedding: tuple[float, ...]
    content_trust: Literal["untrusted"] = "untrusted"


@dataclass(frozen=True, slots=True)
class Citation:
    source_id: str
    source_version_id: str
    title: str
    publisher: str
    canonical_url: str
    locator: str


@dataclass(frozen=True, slots=True)
class EvidenceMatch:
    chunk_id: str
    content: str
    score: float
    citation: Citation
    content_trust: Literal["untrusted"] = "untrusted"


@dataclass(frozen=True, slots=True)
class IngestionResult:
    source_id: str
    source_version_id: str
    chunk_count: int
    created: bool
