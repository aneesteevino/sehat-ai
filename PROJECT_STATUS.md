# Project Status

Last updated: 2026-10-15 (Asia/Karachi)

## Phase

Milestone 5 complete and verified locally: retrieval-first deterministic answer generation, strict grounding validation, abstention, and an authenticated answer preview. Milestone 6 (controlled workflows) is next.

## Completed and verified

- Workspace was empty except for an initialized Git repository with no commits.
- Local execution is available: Node.js 22.13.0, npm 10.9.2, Python 3.12.4, and Git 2.45.2.
- C: had 102.1 GiB free at inspection; the project still enforces a self-imposed 50 GB ceiling.
- No relevant provider environment-variable names were present; values were never inspected or printed.
- GitHub authentication was verified for an account with read/write access to its repositories. No existing repository named exactly `sehat-ai` was found among the authenticated owner's accessible repositories.
- Vercel authentication reports a Hobby account, but the account/team mapping cannot currently list scoped projects (403).
- Google Drive authentication is available; it is not required for source-of-truth code storage.
- Firecrawl is connected but has a negative current credit balance, so no paid/credit-consuming research crawl was started.
- Current official documentation was reviewed for Hugging Face inference pricing, MongoDB Atlas Free and Vector Search, Vercel Hobby/function limits, and GitHub Actions billing.
- Initial architecture, roadmap, cost register, decision log, blockers, and recovery instructions were created.
- GitHub repository `aneesteevino/sehat-ai` was verified, attached as `origin`, and the Phase 0 commits were pushed to `main`.
- FastAPI foundation implemented with typed settings, production secret validation, JSON logging, request IDs, constrained CORS, and liveness/readiness endpoints.
- Next.js 16.4 frontend implemented with TypeScript 6.0, App Router server components, a narrow client readiness component, and Tailwind CSS 4.
- Local unit, lint, type, production-build, and runtime smoke checks passed.
- Backend identity implements Argon2id password hashing, normalized accounts, opaque revocable sessions, patient/clinician/admin roles, negative authorization tests, and versioned auth routes.
- Next.js implements accessible sign-up/sign-in pages, an authenticated server-rendered workspace, and same-origin auth Route Handlers with Secure HTTP-only cookies in production.
- The repository boundary has a concurrency-safe local adapter and a conditional official PyMongo Async adapter. Unique identity indexes and session TTL cleanup are defined.
- Database schema, pagination, retention, audit-event plan, security baseline, and identity API contracts are documented.
- A checksum-pinned source registry contains two evaluation-only CDC-derived summaries with attribution, reuse-policy, version, and non-endorsement metadata.
- Bounded UTF-8 and PDF extraction, Unicode normalization, paragraph-aware chunking, content/version deduplication, and immutable citation locators are implemented.
- A zero-download 256-dimensional lexical hashing provider and hybrid ranker establish a deterministic five-chunk baseline: Recall@2 1.00 and MRR 1.00 across four test queries.
- Authenticated FastAPI and Next.js evidence-search endpoints return versioned, non-cacheable, explicitly untrusted evidence with no generated medical answer.
- A provider-neutral generation service now enforces retrieval adequacy, bounded timeout/retry, strict output schemas, evidence-ID allow-listing, extractive support, common instruction-marker checks, and content-free usage accounting.
- The active `mock/deterministic-evidence-v1` provider makes no external call, downloads no model, costs USD 0, and deterministically selects sentences from eligible evidence.
- Authenticated FastAPI and Next.js answer endpoints return either validated claims with exact citations or deterministic abstention. The accessible UI separates answer, evidence, uncertainty, and application-owned safety limitations.

## Partially completed

- Live Atlas connectivity and account-specific permissions remain conditional; the adapter is unit tested without a network connection.
- Authentication is an MVP foundation; rate limiting, verified email, recovery, MFA decision, and persistent audit events remain pre-deployment work.
- The retrieval corpus and evaluation set are intentionally tiny; semantic, multilingual, and medical quality remain unproven.
- Generation usage records are process-local; no durable operational telemetry exists yet.

## Not started

- Real hosted/local LLM integration, controlled workflows, broader evaluation, and deployment.
- Clinical/domain review; this is mandatory before any claim of medical readiness.

## Current architecture

See `ARCHITECTURE.md`. In short: Vercel-ready Next.js App Router frontend with Tailwind CSS; modular FastAPI backend; MongoDB Atlas when verified; local development embeddings; provider-neutral LLM adapter; deterministic safety gates around model use.

## Repository state

- Local branch: `main`, tracking `origin/main`.
- Remote: `https://github.com/aneesteevino/sehat-ai.git`.
- Foundation milestone commit: `c538338` (`chore: establish Sehat AI project foundation`).
- Phase 0 findings commit: `bdd5ba6` (`docs: record verified phase zero findings`).
- Milestone 2 implementation commit: `4de580a` (`feat: add Next.js and FastAPI foundations`).
- Milestone 2 checkpoint commit: `0426ac3` (`docs: record milestone 2 checkpoint`).
- Milestone 3 implementation commit: `bfceee4` (`feat: add identity and persistence foundation`).
- Milestone 3 checkpoint commit: `9b048a3` (`docs: record milestone 3 checkpoint`).
- Milestone 4 implementation commit: `2b0dba7` (`feat: add grounded evidence retrieval`).
- Milestone 4 checkpoint commit: `726e2ba` (`docs: record milestone 4 checkpoint`).
- Milestone 5 implementation commit: `a33a7e7` (`feat: add grounded answer generation`).

## Test status

- Backend: 47 pytest tests passed; Ruff passed. One upstream FastAPI/Starlette warning notes that `httpx` TestClient support is deprecated in favor of `httpx2`.
- Frontend: 12 Jest tests passed; ESLint passed with zero warnings; TypeScript passed; Next.js production build passed with dynamic evidence and answer BFF routes.
- Runtime smoke: registration and login returned HTTP 201/200; the authenticated answer BFF returned HTTP 200, an extractive answer bound to returned evidence, provider `mock`, cost 0, and `Cache-Control: no-store`.
- Production npm dependency audit: 0 known vulnerabilities. Development-only audit currently reports 19 moderate and 5 high transitive advisories in current Jest and Next ESLint tooling; npm's proposed fixes are unsafe major downgrades, so these are documented rather than forced.

## Deployment status

Not deployed. Vercel project access is blocked by connector scope authorization. Backend deployment target is intentionally undecided.

## Storage status

- Free on C: after final Milestone 5 browser/build verification: 59.50 GiB.
- Project budget: no more than 50 GB; near-term target below 2 GB excluding package caches.
- Project footprint including local dependencies/build output: approximately 708.16 MiB (`.venv` 85.67 MiB, `node_modules` 489.34 MiB, `.next` 131.69 MiB). The temporary development and final production builds increased ignored `.next` cache output; source changes remain small.
- No models or datasets have been downloaded.

## Known limitations

- No callable MongoDB Atlas or Hugging Face account connector is exposed in this session.
- Hugging Face free-user hosted inference credits are experimental-scale, not a dependable production budget.
- The deterministic generation provider is a software-contract mock, not an LLM; it does not establish hosted-model quality, security, latency, or cost.
- The selected local embedding and reranking models have not yet been downloaded or benchmarked.
- No healthcare feature is clinically validated.
- No live Atlas integration test has run; local identities are intentionally lost when the API restarts without `MONGODB_URI`.
- The PDF parser is limited to reviewed registry fixtures; arbitrary uploads remain prohibited without isolation and malware/resource controls.
