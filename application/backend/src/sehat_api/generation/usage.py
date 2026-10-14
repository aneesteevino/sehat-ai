"""Content-free generation usage accounting."""

import asyncio

from sehat_api.generation.models import UsageRecord


class InMemoryUsageLedger:
    def __init__(self) -> None:
        self._records: list[UsageRecord] = []
        self._lock = asyncio.Lock()

    async def add(self, record: UsageRecord) -> None:
        async with self._lock:
            self._records.append(record)

    async def list_records(self) -> list[UsageRecord]:
        async with self._lock:
            return list(self._records)
