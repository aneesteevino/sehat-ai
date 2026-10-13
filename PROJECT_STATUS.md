# Project Status

Last updated: 2026-10-14 (Asia/Karachi)

## Phase

Milestone 2 complete and verified: runnable FastAPI and Next.js foundations. Milestone 3 (identity and persistence) is next.

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

## Partially completed

- The technology choices beyond the application shell remain conditional on database and hosted inference account testing.
- Authentication and persistence architecture is planned but not implemented.

## Not started

- Authentication, database integration, LLM integration, RAG, ingestion, workflows, evaluation, and deployment.
- Clinical/domain review; this is mandatory before any claim of medical readiness.

## Current architecture

See `ARCHITECTURE.md`. In short: Vercel-ready Next.js App Router frontend with Tailwind CSS; modular FastAPI backend; MongoDB Atlas when verified; local development embeddings; provider-neutral LLM adapter; deterministic safety gates around model use.

## Repository state

- Local branch: `main`, tracking `origin/main`.
- Remote: `https://github.com/aneesteevino/sehat-ai.git`.
- Foundation milestone commit: `c538338` (`chore: establish Sehat AI project foundation`).
- Phase 0 findings commit: `bdd5ba6` (`docs: record verified phase zero findings`).
- Milestone 2 implementation commit: `4de580a` (`feat: add Next.js and FastAPI foundations`).

## Test status

- Backend: 7 pytest tests passed; Ruff passed. One upstream FastAPI/Starlette warning notes that `httpx` TestClient support is deprecated in favor of `httpx2`.
- Frontend: 3 Jest tests passed; ESLint passed with zero warnings; TypeScript passed; Next.js production build passed and prerendered `/` statically.
- Runtime smoke: Next.js returned HTTP 200; FastAPI readiness returned HTTP 200 with the typed contract and request ID; configured CORS preflight returned HTTP 200.
- Production npm dependency audit: 0 known vulnerabilities. Development-only audit currently reports 19 moderate and 5 high transitive advisories in current Jest and Next ESLint tooling; npm's proposed fixes are unsafe major downgrades, so these are documented rather than forced.

## Deployment status

Not deployed. Vercel project access is blocked by connector scope authorization. Backend deployment target is intentionally undecided.

## Storage status

- Free on C: after Milestone 2: 98.83 GiB.
- Project budget: no more than 50 GB; near-term target below 2 GB excluding package caches.
- Project footprint including local dependencies/build output: approximately 586.74 MiB (`.venv` 71.65 MiB, `node_modules` 489.34 MiB, `.next` 25.02 MiB).
- No models or datasets have been downloaded.

## Known limitations

- No callable MongoDB Atlas or Hugging Face account connector is exposed in this session.
- Hugging Face free-user hosted inference credits are experimental-scale, not a dependable production budget.
- The selected local embedding and reranking models have not yet been downloaded or benchmarked.
- No healthcare feature is clinically validated.
