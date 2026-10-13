# Architecture Decision Log

## ADR-001: Incremental monorepo

Status: Accepted, 2026-10-14.

Use one repository for frontend, backend, AI modules, tests, and documentation. This reduces synchronization risk and supports atomic, testable milestones.

## ADR-002: Next.js App Router frontend and FastAPI backend

Status: Accepted as baseline, 2026-10-14.

Use Next.js with TypeScript and the App Router for the frontend, Tailwind CSS for styling, and Python 3.12 with FastAPI for the API. Next.js server components are the default; client components are limited to browser-only interactions such as API readiness state. FastAPI matches the project requirement and Python AI ecosystem. The backend must remain portable because Vercel's function payload limit and ephemeral execution are not ideal for document processing or local model loading.

This decision supersedes the earlier Vite proposal before any frontend implementation was committed. Vite is not the application build system.

## ADR-003: Backend deployment remains undecided

Status: Deferred, 2026-10-14.

Vercel is suitable for the frontend. A FastAPI deployment on Vercel may be evaluated for small request/response paths, but the documented 4.5 MB function payload ceiling and serverless lifecycle make it unsuitable to assume for larger document ingestion. Select a backend host only after a zero-cost candidate is tested end to end.

## ADR-004: Provider-neutral LLM boundary

Status: Accepted, 2026-10-14.

All generation uses a typed provider interface with timeouts, structured validation, usage accounting, and a mock provider. No hosted model is hard-coded as mandatory. This prevents a free-tier change from blocking local development.

## ADR-005: Local embeddings for development

Status: Accepted conditionally, 2026-10-14.

Candidate: `sentence-transformers/all-MiniLM-L6-v2` (Apache-2.0). It is small enough for CPU development and produces 384-dimensional embeddings. Download only when the RAG milestone begins, pin the model revision, and measure quality before acceptance.

Candidate reranker: `cross-encoder/ms-marco-MiniLM-L6-v2` (Apache-2.0, roughly 91 MB weights). It is optional and will be added only if evaluation shows measurable retrieval benefit.

## ADR-006: MongoDB Atlas is conditional

Status: Accepted conditionally, 2026-10-14.

Use Atlas as the main application database only after account, Free-cluster, network, and index capabilities are tested. Atlas documentation supports Vector Search testing on Free clusters, but actual account availability is not yet verified. A lightweight in-memory/local test adapter keeps tests independent.

## ADR-007: Deterministic safety controls

Status: Accepted, 2026-10-14.

Emergency red flags, access control, file validation, citation integrity, and prohibited medication actions must be enforced in application code. LLM output cannot override these controls.

## ADR-008: Zero-additional-spend default

Status: Accepted, 2026-10-14.

Do not enable billing or paid compute. Use mocks for automated tests, cache only non-sensitive derived artifacts, and require explicit approval before any action that can create charges.

## ADR-009: Source-of-truth strategy

Status: Accepted, 2026-10-14.

The local Git working tree is the active source of truth; GitHub becomes the durable remote after repository creation. Google Drive may hold exported reports or stakeholder documents later, but never a conflicting source copy.

## ADR-010: Recovery and automatic resumption

Status: Accepted, 2026-10-14.

The repository recovery files are the durable handoff mechanism. The Codex desktop environment supports scheduled thread heartbeats, but no automation is created now: there is no current usage interruption to recover from, usage recovery cannot be safely inferred by a polling task, and the brief explicitly forbids wasteful recurring checks. If a real limit interruption occurs and scheduling remains available, create at most one five-hour follow-up only when it can resume this exact thread without repeatedly consuming usage. Otherwise, resume manually by reading the five recovery files and verifying Git state.
