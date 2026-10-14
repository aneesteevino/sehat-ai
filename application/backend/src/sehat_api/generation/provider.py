"""Provider protocol and deterministic, zero-cost implementation."""

import math
import re
from typing import Protocol

from sehat_api.generation.models import (
    ProviderRequest,
    ProviderResult,
    ProviderUsage,
)
from sehat_api.knowledge.embeddings import tokenize


class TransientProviderError(RuntimeError):
    """A provider failure that may succeed on a bounded retry."""


class GenerationProvider(Protocol):
    name: str
    model: str

    async def generate(self, request: ProviderRequest) -> ProviderResult: ...


class MockGenerationProvider:
    """Selects evidence sentences deterministically; it is not a medical model."""

    name = "mock"
    model = "deterministic-evidence-v1"

    async def generate(self, request: ProviderRequest) -> ProviderResult:
        question_tokens = set(tokenize(request.question))
        question_stems = {token[:4] for token in question_tokens if len(token) > 3}
        asks_for_duration = "how long" in request.question.casefold()
        claims: list[dict[str, object]] = []
        for evidence in request.evidence[:1]:
            sentences = [
                sentence.strip()
                for sentence in re.split(r"(?<=[.!?])\s+|\n+", evidence.content)
                if sentence.strip()
            ]
            if not sentences:
                continue
            best = max(
                enumerate(sentences),
                key=lambda item: (
                    bool(
                        asks_for_duration
                        and re.search(
                            r"\b(seconds?|minutes?|hours?|days?|weeks?)\b",
                            item[1],
                            re.IGNORECASE,
                        )
                    ),
                    len(
                        question_stems
                        & {token[:4] for token in tokenize(item[1]) if len(token) > 3}
                    ),
                    -item[0],
                ),
            )[1]
            claims.append({"text": best[:700], "evidence_ids": [evidence.id]})

        payload: dict[str, object] = {
            "claims": claims,
            "uncertainty": (
                "This answer is limited to the small approved evaluation corpus and may not "
                "cover individual circumstances."
            ),
        }
        output_text = " ".join(claim["text"] for claim in claims)
        input_text = request.question + " ".join(item.content for item in request.evidence)
        return ProviderResult(
            payload=payload,
            usage=ProviderUsage(
                input_units=math.ceil(len(input_text) / 4),
                output_units=math.ceil(len(output_text) / 4),
            ),
        )
