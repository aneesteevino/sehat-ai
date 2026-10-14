"""Deterministic hybrid retrieval with traceable evidence citations."""

from sehat_api.knowledge.embeddings import (
    EmbeddingProvider,
    cosine_similarity,
    tokenize,
)
from sehat_api.knowledge.models import Citation, EvidenceMatch, KnowledgeChunk
from sehat_api.repositories.knowledge import KnowledgeRepository


class RetrievalService:
    def __init__(
        self,
        repository: KnowledgeRepository,
        embeddings: EmbeddingProvider,
    ) -> None:
        self._repository = repository
        self._embeddings = embeddings

    async def search(self, query: str, *, limit: int = 5) -> list[EvidenceMatch]:
        cleaned_query = query.strip()
        if not 2 <= len(cleaned_query) <= 500:
            raise ValueError("query must contain between 2 and 500 characters")
        if not 1 <= limit <= 20:
            raise ValueError("limit must be between 1 and 20")

        query_tokens = set(tokenize(cleaned_query))
        query_vector = self._embeddings.embed([cleaned_query])[0]
        chunks = await self._repository.list_chunks()
        scored: list[tuple[float, KnowledgeChunk]] = []
        for chunk in chunks:
            chunk_tokens = set(tokenize(chunk.content))
            coverage = len(query_tokens & chunk_tokens) / max(len(query_tokens), 1)
            if coverage == 0:
                continue
            cosine = max(cosine_similarity(query_vector, chunk.embedding), 0.0)
            score = (0.7 * cosine) + (0.3 * coverage)
            scored.append((score, chunk))

        scored.sort(key=lambda item: (-item[0], item[1].source_id, item[1].chunk_index))
        evidence: list[EvidenceMatch] = []
        for score, chunk in scored[:limit]:
            source = await self._repository.get_source(chunk.source_id)
            version = await self._repository.get_version(chunk.source_version_id)
            if source is None or version is None:
                continue
            page = f"page {chunk.page_number}, " if chunk.page_number is not None else ""
            paragraph_label = (
                f"paragraph {chunk.paragraph_start}"
                if chunk.paragraph_start == chunk.paragraph_end
                else f"paragraphs {chunk.paragraph_start}-{chunk.paragraph_end}"
            )
            evidence.append(
                EvidenceMatch(
                    chunk_id=chunk.id,
                    content=chunk.content,
                    score=round(score, 6),
                    citation=Citation(
                        source_id=source.id,
                        source_version_id=version.id,
                        title=source.title,
                        publisher=source.publisher,
                        canonical_url=str(source.canonical_url),
                        locator=f"{page}{paragraph_label}",
                    ),
                )
            )
        return evidence
