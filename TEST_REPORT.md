# Test Report

Last run: 2026-10-14 (Asia/Karachi)

## Milestone 2 results

| Check | Result | Evidence |
|---|---|---|
| Backend lint | Pass | Ruff: all checks passed |
| Backend unit/API tests | Pass | 7 passed in 0.72s |
| Frontend component/page tests | Pass | 2 suites, 3 tests |
| Frontend lint | Pass | ESLint, zero warnings |
| Frontend typecheck | Pass | TypeScript `--noEmit` |
| Frontend production build | Pass | Next.js 16.4, `/` statically prerendered |
| Runtime page | Pass | HTTP 200; expected heading present |
| Runtime API | Pass | HTTP 200; typed readiness payload; request ID preserved |
| Runtime CORS | Pass | Preflight HTTP 200 for the temporary smoke-test origin |
| Production npm audit | Pass | 0 production vulnerabilities |

## Known warnings

- FastAPI's re-exported `TestClient` emits an upstream Starlette warning that `httpx` support is deprecated in favor of `httpx2`. The tests pass; migration should be evaluated when FastAPI documents the stable path.
- The full development dependency audit reports 19 moderate and 5 high transitive advisories in current Jest and `eslint-config-next` tooling. `npm audit --omit=dev` reports zero vulnerabilities. npm proposes incompatible/unsafe major downgrades, so no forced audit fix was applied.

## Runtime verification scope

The verified story was: statically rendered Next.js page → hydrated `ApiStatus` client component → FastAPI `GET /health/ready` → typed response and CORS headers. No database or AI service is part of Milestone 2.
