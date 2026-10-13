# Project Plan

## Milestone 1 — Foundation

Acceptance criteria: environment facts recorded; architecture and cost baseline documented; secrets and heavy artifacts ignored; recovery files current; first local commit verified.

## Milestone 2 — Runnable shells

Acceptance criteria: FastAPI health/config API and a Next.js TypeScript App Router shell styled with Tailwind CSS run locally; lint, typecheck, unit tests, and production builds pass without cloud credentials.

## Milestone 3 — Identity and persistence

Acceptance criteria: secure password hashing or an approved external identity flow; role checks; Atlas integration tests where available; pagination, indexes, retention fields, and audit events documented.

## Milestone 4 — Knowledge ingestion and retrieval

Acceptance criteria: approved-source registry; safe PDF/text extraction; normalization, chunking, metadata, deduplication, embeddings, retrieval, and citation traceability; deterministic retrieval metrics with a small curated corpus.

## Milestone 5 — LLM answer generation

Acceptance criteria: provider abstraction, schema validation, timeouts/retries, mock tests, grounded-answer contract, citations, abstention, and usage accounting. A real provider is optional until free access is verified.

## Milestone 6 — Controlled workflows

Acceptance criteria: explicit tools and schemas; deterministic red-flag route; prompt-injection defenses; document explanation and symptom questionnaire; audit events; no autonomous diagnosis or prescribing.

## Milestone 7 — Product surfaces

Acceptance criteria: accessible chat, history, uploads, citations, symptom flow, medication information, privacy/settings, and doctor draft-review workspace with synthetic labeled data.

## Milestone 8 — Evaluation and security

Acceptance criteria: versioned evaluation cases; Recall@k, MRR, citation correctness, groundedness, structured validity, safety adherence, latency, and cost; threat model; dependency and upload checks; reproducible report.

## Milestone 9 — Deployment readiness

Acceptance criteria: production configuration reviewed; frontend preview deployed; backend target validated; CORS/auth/database connectivity tested; no secret leakage; rollback path documented.

## Milestone 10 — Portfolio release

Acceptance criteria: full documentation, screenshots/demo, honest benchmarks, limitations, tagged release, and verified public demo where feasible.
