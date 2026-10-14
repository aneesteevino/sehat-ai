# Next Steps

## Exact next task

Milestone 4: implement a small, approved-source knowledge ingestion and retrieval slice without downloading large models or using real patient data.

## Files and components

- `data/`: approved source registry and tiny synthetic/public test fixtures with provenance and license metadata.
- `application/backend/src/sehat_api/knowledge/`: source, version, chunk, deletion, and ingestion contracts.
- `ai/`: deterministic development embedding interface, retrieval service, citation/evidence bundle, and optional local model adapter.
- `application/backend/src/sehat_api/repositories/`: knowledge repository protocol plus memory adapter; Atlas Vector Search stays conditional.
- `tests/`: extraction, normalization, deduplication, retrieval, citation traceability, and prompt-injection boundary tests.
- Retrieval evaluation and data-governance documentation.

## Prerequisites

1. Inspect this status file and `BLOCKERS.md`.
2. Confirm `main` is synchronized with `origin/main`.
3. Recheck C: free space before adding dependencies.
4. Approve a minimal public-domain or appropriately licensed source set and record exact versions.
5. Benchmark a deterministic lightweight embedding path before downloading any candidate model.
6. Keep Atlas Vector Search behind an interface until live Atlas access is available.

## Planned commands

Review and pin any parser or embedding dependency before installation. Do not fetch a full medical dataset or model checkpoint until its license, size, and need are recorded.

## Expected outcome

- A small approved document can be normalized, chunked, deduplicated, embedded through an interface, retrieved, and cited to its exact source/version/location.
- Tests remain deterministic and free of external-provider calls.
- Retrieved text remains data and cannot select tools or override application policy.
- Retrieval quality has a reproducible baseline rather than an anecdotal demo.

## Verification

- Run ingestion, retrieval, citation, and adversarial-boundary tests.
- Run Next.js unit tests, typecheck, ESLint, and the production build.
- Scan tracked files for common secret patterns.
- Record package sizes and updated free disk space.
- Update recovery files, then commit and push the verified milestone.

## Remaining blockers

- Vercel project scope needs reconnection or corrected authorization before deployment work.
- MongoDB Atlas and Hugging Face account inspection require usable connectors or user-provided configuration through secure environment settings.
