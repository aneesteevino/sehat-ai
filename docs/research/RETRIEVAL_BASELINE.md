# Retrieval Baseline

Run date: 2026-10-14 (Asia/Karachi).

## Configuration

- Corpus: two evaluation-only CDC-derived summaries, five paragraph-aware chunks.
- Embedding: 256-dimensional signed lexical feature hashing; no model or weights downloaded.
- Ranking: 70% non-negative cosine similarity plus 30% query-token coverage.
- Dataset: `data/evaluation_datasets/retrieval-v1.json`, four source-identification queries.
- Evaluation cutoff: `k=2`.

## Results

| Metric | Result |
|---|---:|
| Recall@2 | 1.00 |
| Mean reciprocal rank | 1.00 |

The result proves that the pipeline, versioning, ranking, and citation contracts behave deterministically on this tiny corpus. It does not establish semantic, multilingual, medical, or production retrieval quality. The lexical hash baseline will be retained as a zero-cost fallback and regression reference. A local semantic model may be evaluated later only after its revision, license, disk size, latency, and measured improvement are recorded.

## Safety checks

- Evidence responses contain no generated answer.
- Every match includes source ID, version ID, canonical URL, and paragraph/page locator.
- Retrieved prompt-injection text is returned with `content_trust=untrusted` and has no executable/tool field.
- Unknown or low-overlap queries may return no evidence; no fallback medical claim is synthesized.
