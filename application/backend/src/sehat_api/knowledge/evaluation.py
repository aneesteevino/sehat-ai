"""Small deterministic Recall@k and reciprocal-rank evaluation."""

import json
from dataclasses import dataclass
from pathlib import Path

from sehat_api.knowledge.retrieval import RetrievalService


@dataclass(frozen=True, slots=True)
class RetrievalMetrics:
    case_count: int
    recall_at_k: float
    mean_reciprocal_rank: float


async def evaluate_retrieval(
    service: RetrievalService,
    dataset_path: Path,
    *,
    k: int = 3,
) -> RetrievalMetrics:
    payload = json.loads(dataset_path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    hits = 0
    reciprocal_rank = 0.0
    for case in cases:
        matches = await service.search(case["query"], limit=k)
        source_ids = [match.citation.source_id for match in matches]
        expected = case["expected_source_id"]
        if expected in source_ids:
            hits += 1
            reciprocal_rank += 1 / (source_ids.index(expected) + 1)
    count = len(cases)
    return RetrievalMetrics(
        case_count=count,
        recall_at_k=hits / count if count else 0.0,
        mean_reciprocal_rank=reciprocal_rank / count if count else 0.0,
    )
