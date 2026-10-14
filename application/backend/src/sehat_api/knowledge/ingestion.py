"""Approved-registry ingestion with versioning, checksums, and deduplication."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError

from sehat_api.knowledge.embeddings import EmbeddingProvider
from sehat_api.knowledge.extraction import extract_document
from sehat_api.knowledge.models import (
    IngestionResult,
    KnowledgeChunk,
    SourceRegistry,
    SourceVersion,
)
from sehat_api.knowledge.text import content_digest, normalize_text, split_section
from sehat_api.repositories.knowledge import KnowledgeRepository


class RegistryValidationError(ValueError):
    """The registry or an approved fixture did not match its declared metadata."""


class IngestionService:
    def __init__(
        self,
        repository: KnowledgeRepository,
        embeddings: EmbeddingProvider,
        *,
        chunk_characters: int = 350,
    ) -> None:
        if chunk_characters < 100:
            raise ValueError("chunk_characters must be at least 100")
        self._repository = repository
        self._embeddings = embeddings
        self._chunk_characters = chunk_characters

    async def ingest_registry(self, registry_path: Path) -> list[IngestionResult]:
        try:
            payload = json.loads(registry_path.read_text(encoding="utf-8"))
            registry = SourceRegistry.model_validate(payload)
        except (OSError, json.JSONDecodeError, ValidationError) as exc:
            raise RegistryValidationError("Knowledge source registry is invalid.") from exc

        source_ids = [source.id for source in registry.sources]
        if len(source_ids) != len(set(source_ids)):
            raise RegistryValidationError("Knowledge source IDs must be unique.")

        approved_root = registry_path.parent
        results: list[IngestionResult] = []
        for source in registry.sources:
            if source.status != "approved_for_evaluation":
                continue
            sections = extract_document(
                approved_root / source.fixture_path,
                approved_root,
                source.content_type,
            )
            digest = content_digest(sections)
            if digest != source.expected_sha256:
                raise RegistryValidationError(
                    f"Fixture checksum does not match the registry for {source.id}."
                )

            version = SourceVersion(
                id=f"{source.id}:{digest[:16]}",
                source_id=source.id,
                content_sha256=digest,
                source_updated_at=source.source_updated_at,
                retrieved_at=source.retrieved_at,
                ingested_at=datetime.now(UTC),
            )
            pending: list[tuple[str, int | None, int, int]] = []
            for section in sections:
                for content, paragraph_start, paragraph_end in split_section(
                    section,
                    max_chars=self._chunk_characters,
                ):
                    pending.append(
                        (
                            normalize_text(content),
                            section.page_number,
                            paragraph_start,
                            paragraph_end,
                        )
                    )
            vectors = self._embeddings.embed([item[0] for item in pending])
            chunks: list[KnowledgeChunk] = []
            for index, ((content, page, start, end), vector) in enumerate(
                zip(pending, vectors, strict=True)
            ):
                chunk_digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
                chunks.append(
                    KnowledgeChunk(
                        id=f"{version.id}:{index}:{chunk_digest[:12]}",
                        source_id=source.id,
                        source_version_id=version.id,
                        content=content,
                        content_sha256=chunk_digest,
                        chunk_index=index,
                        page_number=page,
                        paragraph_start=start,
                        paragraph_end=end,
                        embedding=vector,
                    )
                )
            created = await self._repository.add_version(source, version, chunks)
            results.append(
                IngestionResult(
                    source_id=source.id,
                    source_version_id=version.id,
                    chunk_count=len(chunks),
                    created=created,
                )
            )
        return results
