# Next Steps

## Exact next task

Milestone 2: create the minimal runnable backend and frontend foundations without introducing AI or database coupling.

## Files and components

- `application/backend/`: FastAPI package, settings, structured logging, request IDs, `/health/live`, and `/health/ready`.
- `application/frontend/`: React + TypeScript shell with the product safety notice and API health state.
- `tests/`: backend health/config tests and frontend smoke tests.
- Root dependency and task configuration.

## Prerequisites

1. Inspect this status file and `BLOCKERS.md`.
2. Confirm working tree and current branch.
3. Recheck C: free space before installing dependencies.
4. Use one local Python virtual environment and one Node package tree.

## Planned commands

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
# Install only pinned Milestone 2 dependencies after review.
npm install
```

Exact dependency commands must be finalized in the milestone; do not paste tokens into the shell.

## Expected outcome

- Frontend and backend start locally.
- Health endpoints return typed responses without external services.
- Configuration fails safely when production-only secrets are absent.
- Unit/smoke tests pass with no network calls.

## Verification

- Run backend unit tests.
- Run frontend unit tests, typecheck, lint, and production build.
- Scan tracked files for common secret patterns.
- Record package sizes and updated free disk space.
- Update all five recovery files, then commit the verified milestone.

## Remaining blockers

- Remote GitHub repository creation is not available through the current connector and GitHub CLI is not installed.
- Vercel project scope needs reconnection or corrected authorization before deployment work.
- MongoDB Atlas and Hugging Face account inspection require usable connectors or user-provided configuration through secure environment settings.
