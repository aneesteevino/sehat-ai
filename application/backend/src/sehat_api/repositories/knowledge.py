"""Knowledge repository contract and deterministic in-memory adapter."""

import asyncio
from typing import Protocol

from sehat_api.knowledge.models import KnowledgeChunk, RegistrySource, SourceVersion


class KnowledgeRepository(Protocol):
    async def add_version(
        self,
        source: RegistrySource,
        version: SourceVersion,
        chunks: list[KnowledgeChunk],
    ) -> bool: ...

    async def list_chunks(self) -> list[KnowledgeChunk]: ...

    async def get_source(self, source_id: str) -> RegistrySource | None: ...

    async def get_version(self, version_id: str) -> SourceVersion | None: ...


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self._sources: dict[str, RegistrySource] = {}
        self._versions: dict[str, SourceVersion] = {}
        self._chunks: dict[str, KnowledgeChunk] = {}
        self._lock = asyncio.Lock()

    async def add_version(
        self,
        source: RegistrySource,
        version: SourceVersion,
        chunks: list[KnowledgeChunk],
    ) -> bool:
        async with self._lock:
            if version.id in self._versions:
                return False
            self._sources[source.id] = source
            self._versions[version.id] = version
            self._chunks.update({chunk.id: chunk for chunk in chunks})
            return True

    async def list_chunks(self) -> list[KnowledgeChunk]:
        return sorted(self._chunks.values(), key=lambda chunk: (chunk.source_id, chunk.chunk_index))

    async def get_source(self, source_id: str) -> RegistrySource | None:
        return self._sources.get(source_id)

    async def get_version(self, version_id: str) -> SourceVersion | None:
        return self._versions.get(version_id)
