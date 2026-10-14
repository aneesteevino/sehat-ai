# Session Log

## 2026-10-14 — Phase 0 and repository foundation

### Inspected

- Read the supplied Sehat AI master development brief.
- Listed the initially empty workspace and Git state.
- Checked C: capacity (102.1 GiB free).
- Checked installed runtimes: Node.js 22.13.0, npm 10.9.2, Python 3.12.4, Git 2.45.2.
- Checked relevant environment-variable names only; none were present.
- Verified GitHub, Vercel, Google Drive, and Firecrawl connector responses.
- Confirmed no exact `sehat-ai` repository in the authenticated GitHub owner's repository list.
- Reviewed official service documentation for cost and deployment constraints.

### Files created

- Repository controls: `.gitignore`, `.env.example`.
- Project entry point: `README.md`.
- Recovery files: `PROJECT_STATUS.md`, `NEXT_STEPS.md`, `DECISIONS.md`, `SESSION_LOG.md`, `BLOCKERS.md`.
- Planning documents: `PROJECT_PLAN.md`, `ARCHITECTURE.md`, `TECH_STACK.md`, `API_COSTS.md`.
- Initial directory placeholders under `application/`, `ai/`, `data/`, `docs/`, `tests/`, and `scripts/`.

### External actions

- Read-only inspection only. No cloud project, repository, database, deployment, file, or paid resource was created or modified.

### Failures and recovery

- Vercel project listing under the reported default team returned HTTP 403 due to scope authorization.
- GitHub CLI is not installed; the GitHub connector does not expose repository creation.
- Firecrawl reports -107 remaining credits of a 1,000-credit plan, so it was not used for research.
- No MongoDB Atlas or Hugging Face account tools were exposed.

### Stopping point

Repository foundation verified and committed locally on branch `main` as `c538338`. Workspace content outside `.git` was approximately 26 KB before the commit. Required-file validation, whitespace checks, and a conservative secret-pattern scan passed. Next: begin the runnable frontend/backend foundation.

## 2026-10-14 — Milestone 2 runnable shells

### Repository synchronization

- Verified the user-created public repository `aneesteevino/sehat-ai`, its empty state, `main` default branch, and admin/push permission.
- Added the exact repository as `origin` and pushed commits `c538338` and `bdd5ba6`.

### Architecture update

- Replaced the uncommitted Vite proposal with Next.js 16.4, TypeScript 6.0, App Router, and Tailwind CSS 4 at the user's request.
- Kept the landing page server-rendered and isolated browser readiness checking in one client component.
- Updated architecture, stack, roadmap, decision, environment, and setup documentation.

### Backend implementation

- Added FastAPI application factory, typed Pydantic settings, production secret validation, JSON logging, request ID middleware, constrained CORS, and liveness/readiness contracts.
- Added 7 deterministic configuration and API tests.

### Frontend implementation

- Added accessible responsive landing page, explicit medical safety boundary, API readiness status, Jest tests, ESLint, TypeScript, Tailwind/PostCSS, and Next.js production configuration.

### Verification

- Ruff: passed.
- Pytest: 7 passed; one upstream TestClient deprecation warning recorded.
- Jest: 3 passed.
- ESLint: passed with zero warnings.
- TypeScript: passed.
- Next.js production build: passed; `/` statically prerendered.
- Runtime: page, readiness endpoint, request ID preservation, and CORS preflight returned HTTP 200.
- Production npm audit: 0 vulnerabilities. Development-only audit advisories documented in `PROJECT_STATUS.md` and `TEST_REPORT.md`.

### Storage

- C: free after dependencies/build: 98.83 GiB.
- Project footprint: approximately 586.74 MiB, under the 2 GiB near-term target.

### Stopping point

Milestone 2 is implemented and verified in commit `4de580a`. A generated editable-install `.egg-info` directory was caught during the pre-push review, removed, ignored, and excluded from the amended commit. Next: push the milestone and this recovery checkpoint, then begin Milestone 3 identity and persistence.

## 2026-10-14 — Milestone 3 identity and persistence

### Identity and API

- Added normalized patient registration, Argon2id password hashing, generic credential failures, dummy-hash timing mitigation, active-account checks, and patient/clinician/admin authorization policy.
- Added random opaque sessions whose HMAC digests—not raw bearer values—are persisted, with absolute expiry and explicit logout revocation.
- Added versioned register, login, current-user, and logout endpoints.

### Persistence

- Added repository protocols and a concurrency-safe in-memory adapter for development and deterministic tests.
- Added a conditional official PyMongo Async adapter with unique email/token indexes, user/session lookup indexes, and automatic session TTL cleanup.
- Production now fails closed without both a strong auth secret and MongoDB configuration. Live Atlas access was not available, so no remote database was created or modified.

### Frontend

- Added accessible sign-up and sign-in pages, a server-rendered authenticated workspace, and sign-out flow.
- Added Next.js auth Route Handlers as a backend-for-frontend. Session tokens are server-only HTTP-only cookies; mutation requests enforce same-origin signals, JSON content, and an 8 KiB body ceiling.

### Verification

- Ruff passed; pytest passed 23 tests.
- Jest passed 8 tests; ESLint and TypeScript passed; the Next.js production build passed.
- End-to-end local runtime passed registration, authenticated workspace rendering, logout, and revoked-session rejection.
- Production npm audit reported zero vulnerabilities; conservative tracked-file credential scan found no matches.

### Storage and stopping point

- Project footprint is approximately 611.62 MiB. C: reported 83.01 GiB free; the project remains far below its 50 GB ceiling and no model or dataset was downloaded.
- Milestone 3 was committed as `bfceee4` and pushed to the verified `aneesteevino/sehat-ai` repository. Milestone 4 knowledge ingestion and retrieval is next. Atlas, Vercel project scope, hosted inference, and clinical review blockers remain open.

## 2026-10-14 — Milestone 4 knowledge ingestion and retrieval

### Sources and ingestion

- Added an approved-source registry with two short CDC-derived evaluation summaries, exact update/retrieval dates, attribution, non-endorsement, reuse-policy URLs, and normalized SHA-256 checksums.
- Added bounded strict-UTF-8 and `pypdf` extraction, path containment, Unicode normalization, paragraph-aware chunking, immutable versions, and deduplication.
- Documented that arbitrary PDF uploads remain prohibited; current parsing is only for reviewed local registry fixtures.

### Retrieval and product surface

- Added a provider-neutral embedding protocol and zero-download 256-dimensional signed lexical hashing baseline.
- Added deterministic hybrid ranking and evidence contracts carrying source/version IDs, canonical URL, paragraph/page locator, score, and `content_trust=untrusted`.
- Added authenticated FastAPI and Next.js search routes plus an accessible workspace evidence-search interface. The response explicitly contains no generated answer.

### Evaluation and verification

- Baseline corpus: two sources, five chunks, four queries; Recall@2 1.00 and MRR 1.00.
- Ruff passed; pytest passed 34 tests including PDF boundaries, deduplication, retrieval, API authentication, citations, and retrieved prompt-injection handling.
- Jest passed 10 tests; TypeScript, ESLint, and the Next.js production build passed.
- End-to-end runtime passed registration, authenticated workspace rendering, BFF evidence retrieval, top-source citation, untrusted marker, null generated answer, and no-store response caching.

### Storage and stopping point

- Project footprint is approximately 625.59 MiB; no model weights or large datasets were downloaded. C: reported 58.89 GiB free, with the host-level decrease occurring outside this project.
- Milestone 4 was committed as `2b0dba7` and pushed to the verified `aneesteevino/sehat-ai` repository. Milestone 5 grounded answer generation is next. Atlas, Vercel project scope, hosted inference, arbitrary upload isolation, and clinical review blockers remain open.

## 2026-10-15 — Milestone 5 grounded answer generation

### Generation contract

- Added a provider-neutral FastAPI generation module with a deterministic zero-cost mock, strict structured output, bounded timeout/retry, and process-local content-free usage records.
- Enforced retrieval before generation, rank plus substantive-overlap adequacy, deterministic abstention, evidence-ID allow-listing, extractive claim support, and common direct/indirect instruction-marker rejection.
- Kept authorization, medical safety text, release decisions, and all side-effect authority outside the provider. Partial streaming remains disabled until the complete object can be safely validated.

### Product surface

- Added an authenticated `/api/v1/answers` route and a same-origin Next.js `/api/answers` proxy with bounded JSON handling, server-only session forwarding, and no-store responses.
- Added an accessible workspace preview that visibly separates claims, evidence links, uncertainty, safety limitations, and transparent zero-cost provider metadata.

### Verification

- Ruff passed; pytest passed 47 tests covering schema, missing evidence, forged citations, invented claims, timeout, retry, injection markers, abstention, authentication, and usage accounting.
- Jest passed 12 tests; TypeScript, ESLint, production npm audit, and the Next.js production build passed.
- End-to-end runtime passed registration, login, server-only cookie forwarding, retrieval-to-answer, exact claim/evidence binding, zero mock cost, and no-store caching. Browser verification then caught and corrected a weak sentence-order choice; the final selector prioritizes requested duration evidence and returns only the strongest extractive claim.
- No hosted inference call, model download, paid resource, Atlas operation, or real patient data was used.
- Final footprint was approximately 708.16 MiB with 59.50 GiB free on C: after browser and production-build caches; no model or dataset was downloaded.

### Stopping point

Milestone 5 implementation was committed as `a33a7e7` and pushed to the verified `aneesteevino/sehat-ai` repository. Milestone 6 controlled workflows is next; deployment authorization, live Atlas, hosted inference, arbitrary upload isolation, and clinical review blockers remain open.

## 2026-10-15 — Milestone 6 controlled workflows

- Added deterministic emergency phrase routing before retrieval/generation, with application-owned local-emergency guidance and zero provider attempts.
- Added owner-scoped, idempotent state machines for a fixed symptom questionnaire and synthetic document facts, plus strict transition and input allow-lists.
- Added a content-minimized in-memory audit ledger whose metadata schema excludes health/document/model content.
- Added authenticated FastAPI and Next.js safety/workflow routes and an accessible safety/questionnaire workspace preview.
- Ruff and 59 backend tests passed; 15 frontend tests, TypeScript, ESLint, production build, and production audit passed.
- Browser verification completed emergency routing and the full questionnaire with expected 200/201 logs and no console errors.
- No provider call occurred on emergency routing; no model, paid service, upload, Atlas resource, or real patient data was used.
- Final footprint was approximately 732.74 MiB with 59.47 GiB free on C:.

### Stopping point

Milestone 6 implementation was committed as `604df90` and pushed to the verified `aneesteevino/sehat-ai` repository. Milestone 7 product surfaces is next; deployment authorization, live Atlas, hosted inference, arbitrary upload isolation, and clinical review blockers remain open.
