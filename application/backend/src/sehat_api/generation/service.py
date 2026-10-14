"""Retrieval-first answer generation with deterministic safety enforcement."""

import asyncio
import re
import time
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import ValidationError

from sehat_api.generation.models import (
    GroundedAnswer,
    GroundedClaim,
    ProviderAnswer,
    ProviderEvidence,
    ProviderRequest,
    ProviderUsage,
    SafetyEscalation,
    UsageRecord,
)
from sehat_api.generation.provider import GenerationProvider, TransientProviderError
from sehat_api.generation.usage import InMemoryUsageLedger
from sehat_api.knowledge.embeddings import tokenize
from sehat_api.knowledge.models import EvidenceMatch
from sehat_api.knowledge.retrieval import RetrievalService
from sehat_api.safety.policy import RedFlagPolicy

SAFETY_NOTICE = (
    "Evaluation preview only. This is not a diagnosis, prescription, emergency service, "
    "or substitute for a qualified healthcare professional."
)
INJECTION_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions?",
        r"(reveal|show|print|repeat)\s+(the\s+)?(system|developer)\s+prompt",
        r"you\s+are\s+now\s+(in\s+)?developer\s+mode",
        r"(call|invoke|run|execute)\s+(the\s+)?[\w-]+\s+tool",
        r"system\s+override",
    )
)
QUERY_STOP_WORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "can",
        "do",
        "for",
        "how",
        "i",
        "in",
        "is",
        "of",
        "should",
        "the",
        "to",
        "what",
        "when",
        "with",
    }
)


class GenerationUnavailableError(RuntimeError):
    """The provider did not produce a result within the bounded policy."""


class UnsafeProviderOutputError(RuntimeError):
    """Provider output failed schema or citation-integrity validation."""


def contains_instruction_like_content(text: str) -> bool:
    """Catch common direct/indirect injection markers as one defense layer."""

    return any(pattern.search(text) for pattern in INJECTION_PATTERNS)


def has_substantive_overlap(question: str, evidence: str) -> bool:
    """Require a non-trivial lexical anchor in addition to the baseline score."""

    question_stems = {
        token[:4]
        for token in tokenize(question)
        if token not in QUERY_STOP_WORDS and len(token) > 3
    }
    evidence_stems = {token[:4] for token in tokenize(evidence) if len(token) > 3}
    return bool(question_stems & evidence_stems)


class GenerationService:
    def __init__(
        self,
        retrieval: RetrievalService,
        provider: GenerationProvider,
        usage_ledger: InMemoryUsageLedger,
        safety_policy: RedFlagPolicy | None = None,
        *,
        minimum_score: float = 0.13,
        timeout_seconds: float = 8.0,
        max_attempts: int = 2,
    ) -> None:
        if not 0 <= minimum_score <= 1:
            raise ValueError("minimum_score must be between 0 and 1")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if not 1 <= max_attempts <= 3:
            raise ValueError("max_attempts must be between 1 and 3")
        self._retrieval = retrieval
        self._provider = provider
        self._usage_ledger = usage_ledger
        self._safety_policy = safety_policy or RedFlagPolicy()
        self._minimum_score = minimum_score
        self._timeout_seconds = timeout_seconds
        self._max_attempts = max_attempts

    async def answer(self, question: str) -> GroundedAnswer:
        started = time.monotonic()
        safety = self._safety_policy.evaluate(question)
        if safety.level == "emergency":
            usage = await self._record(
                ProviderUsage(input_units=0, output_units=0), 0, "escalated", started
            )
            return GroundedAnswer(
                status="escalated",
                claims=(),
                evidence=(),
                uncertainty="This rule-based alert is intentionally conservative.",
                safety_notice=SAFETY_NOTICE,
                abstention_reason=None,
                escalation=SafetyEscalation(
                    categories=safety.categories,
                    message=safety.message,
                    actions=safety.actions,
                ),
                usage=usage,
            )
        evidence = await self._retrieval.search(question, limit=5)
        eligible = tuple(
            match
            for match in evidence
            if match.score >= self._minimum_score
            and has_substantive_overlap(question, match.content)
            and not contains_instruction_like_content(match.content)
        )
        if contains_instruction_like_content(question):
            return await self._abstain("unsafe_input", (), started)
        if not eligible:
            return await self._abstain("insufficient_evidence", (), started)

        request = ProviderRequest(
            question=question.strip(),
            evidence=tuple(
                ProviderEvidence(id=match.chunk_id, content=match.content) for match in eligible
            ),
        )
        attempts = 0
        result = None
        while attempts < self._max_attempts:
            attempts += 1
            try:
                result = await asyncio.wait_for(
                    self._provider.generate(request),
                    timeout=self._timeout_seconds,
                )
                break
            except (TimeoutError, TransientProviderError) as exc:
                if attempts == self._max_attempts:
                    await self._record(
                        ProviderUsage(input_units=0, output_units=0),
                        attempts,
                        "failed",
                        started,
                    )
                    raise GenerationUnavailableError("generation provider unavailable") from exc

        if result is None:  # pragma: no cover - loop invariant
            raise GenerationUnavailableError("generation provider unavailable")

        try:
            output = ProviderAnswer.model_validate(result.payload)
        except ValidationError as exc:
            await self._record(result.usage, attempts, "failed", started)
            raise UnsafeProviderOutputError("provider output schema rejected") from exc

        allowed_ids = {match.chunk_id for match in eligible}
        evidence_by_id = {match.chunk_id: match.content for match in eligible}
        claims: list[GroundedClaim] = []
        for claim in output.claims:
            evidence_ids = tuple(dict.fromkeys(claim.evidence_ids))
            if not evidence_ids or not set(evidence_ids) <= allowed_ids:
                await self._record(result.usage, attempts, "failed", started)
                raise UnsafeProviderOutputError("provider cited evidence outside the bundle")
            normalized_claim = " ".join(claim.text.casefold().split())
            if not any(
                normalized_claim in " ".join(evidence_by_id[evidence_id].casefold().split())
                for evidence_id in evidence_ids
            ):
                await self._record(result.usage, attempts, "failed", started)
                raise UnsafeProviderOutputError(
                    "provider claim was not extractive from its citation"
                )
            if contains_instruction_like_content(claim.text):
                await self._record(result.usage, attempts, "failed", started)
                raise UnsafeProviderOutputError("provider output contained unsafe instructions")
            claims.append(GroundedClaim(text=claim.text, evidence_ids=evidence_ids))

        if contains_instruction_like_content(output.uncertainty):
            await self._record(result.usage, attempts, "failed", started)
            raise UnsafeProviderOutputError("provider uncertainty contained unsafe instructions")

        usage = await self._record(result.usage, attempts, "answered", started)
        return GroundedAnswer(
            status="answered",
            claims=tuple(claims),
            evidence=eligible,
            uncertainty=output.uncertainty,
            safety_notice=SAFETY_NOTICE,
            abstention_reason=None,
            escalation=None,
            usage=usage,
        )

    async def _abstain(
        self,
        reason: str,
        evidence: tuple[EvidenceMatch, ...],
        started: float,
    ) -> GroundedAnswer:
        usage = await self._record(
            ProviderUsage(input_units=0, output_units=0), 0, "abstained", started
        )
        return GroundedAnswer(
            status="abstained",
            claims=(),
            evidence=evidence,
            uncertainty=(
                "The approved evidence is not sufficient to answer this question reliably."
            ),
            safety_notice=SAFETY_NOTICE,
            abstention_reason=reason,
            escalation=None,
            usage=usage,
        )

    async def _record(
        self,
        usage: ProviderUsage,
        attempts: int,
        outcome: Literal["answered", "abstained", "escalated", "failed"],
        started: float,
    ) -> UsageRecord:
        record = UsageRecord(
            id=str(uuid4()),
            created_at=datetime.now(UTC),
            provider=self._provider.name,
            model=self._provider.model,
            input_units=max(usage.input_units, 0),
            output_units=max(usage.output_units, 0),
            estimated_cost_usd=max(usage.estimated_cost_usd, 0),
            attempts=attempts,
            duration_ms=round((time.monotonic() - started) * 1000),
            outcome=outcome,
        )
        await self._usage_ledger.add(record)
        return record
