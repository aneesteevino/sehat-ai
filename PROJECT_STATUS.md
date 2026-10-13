# Project Status

Last updated: 2026-10-14 (Asia/Karachi)

## Phase

Phase 0 complete locally: environment inspection, current-service research, architecture baseline, cost controls, recovery files, and repository foundation.

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

## Partially completed

- Git is local-only. The initial commit and remote publication remain pending verification and/or repository creation.
- The technology choices are a baseline; database and hosted inference choices remain conditional on connected-account testing.

## Not started

- Frontend and backend source code.
- Authentication, database integration, LLM integration, RAG, ingestion, workflows, evaluation, and deployment.
- Clinical/domain review; this is mandatory before any claim of medical readiness.

## Current architecture

See `ARCHITECTURE.md`. In short: Vercel-hosted React frontend; modular FastAPI backend; MongoDB Atlas when verified; local development embeddings; provider-neutral LLM adapter; deterministic safety gates around model use.

## Repository state

- Local branch at inspection: `master`, no commits.
- Target default branch: `main`.
- Remote: none configured.
- Foundation milestone commit: `c538338` (`chore: establish Sehat AI project foundation`).

## Test status

- Repository validation passed: required files present, `git diff --check` clean, and no likely committed secret assignments detected outside `.env.example`.
- Application tests: not applicable yet; no application code exists.

## Deployment status

Not deployed. Vercel project access is blocked by connector scope authorization. Backend deployment target is intentionally undecided.

## Storage status

- Free on C: at initial inspection: 102.1 GiB.
- Project budget: no more than 50 GB; near-term target below 2 GB excluding package caches.
- No models, datasets, virtual environments, or package trees have been downloaded.

## Known limitations

- No callable MongoDB Atlas or Hugging Face account connector is exposed in this session.
- Hugging Face free-user hosted inference credits are experimental-scale, not a dependable production budget.
- The selected local embedding and reranking models have not yet been downloaded or benchmarked.
- No healthcare feature is clinically validated.
