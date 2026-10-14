# Project Status

Last updated: 2026-10-14 (Asia/Karachi)

## Phase

Milestone 4 complete and verified locally: approved-source ingestion, deterministic retrieval, versioned citations, and authenticated evidence search. Milestone 5 (grounded answer generation) is next.

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

## Partially completed

- Live Atlas connectivity and account-specific permissions remain conditional; the adapter is unit tested without a network connection.
- Authentication is an MVP foundation; rate limiting, verified email, recovery, MFA decision, and persistent audit events remain pre-deployment work.
- The retrieval corpus and evaluation set are intentionally tiny; semantic, multilingual, and medical quality remain unproven.

## Not started

- Grounded LLM answer generation, controlled workflows, broader evaluation, and deployment.
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

## Test status

- Backend: 34 pytest tests passed; Ruff passed. One upstream FastAPI/Starlette warning notes that `httpx` TestClient support is deprecated in favor of `httpx2`.
- Frontend: 10 Jest tests passed; ESLint passed with zero warnings; TypeScript passed; Next.js production build passed with the dynamic evidence BFF route.
- Runtime smoke: authenticated workspace and evidence search returned HTTP 200; the handwashing query ranked the expected versioned source first, marked it untrusted, returned a paragraph locator, set `generated_answer` to null, and used `Cache-Control: no-store`.
- Production npm dependency audit: 0 known vulnerabilities. Development-only audit currently reports 19 moderate and 5 high transitive advisories in current Jest and Next ESLint tooling; npm's proposed fixes are unsafe major downgrades, so these are documented rather than forced.

## Deployment status

Not deployed. Vercel project access is blocked by connector scope authorization. Backend deployment target is intentionally undecided.

## Storage status

- Free on C: after Milestone 4 verification: 58.89 GiB. The large host-level decrease occurred outside the project; the project itself grew by about 14 MiB.
- Project budget: no more than 50 GB; near-term target below 2 GB excluding package caches.
- Project footprint including local dependencies/build output: approximately 625.59 MiB (`.venv` 85.67 MiB, `node_modules` 489.34 MiB, with the remainder primarily the production build and source files).
- No models or datasets have been downloaded.

## Known limitations

- No callable MongoDB Atlas or Hugging Face account connector is exposed in this session.
- Hugging Face free-user hosted inference credits are experimental-scale, not a dependable production budget.
- The selected local embedding and reranking models have not yet been downloaded or benchmarked.
- No healthcare feature is clinically validated.
- No live Atlas integration test has run; local identities are intentionally lost when the API restarts without `MONGODB_URI`.
- The PDF parser is limited to reviewed registry fixtures; arbitrary uploads remain prohibited without isolation and malware/resource controls.
