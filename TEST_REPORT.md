# Test Report

Last run: 2026-10-15 (Asia/Karachi)

## Milestone 6 results

| Check | Result | Evidence |
|---|---|---|
| Backend lint | Pass | Ruff: all checks passed |
| Backend unit/API/repository/retrieval/generation/workflow tests | Pass | 59 passed |
| Frontend component/request tests | Pass | 7 suites, 15 tests |
| Frontend lint | Pass | ESLint, zero warnings |
| Frontend typecheck | Pass | TypeScript `--noEmit` |
| Frontend production build | Pass | Next.js 16.4; 13 routes including safety and workflow BFF endpoints |
| Retrieval baseline | Pass | 2 sources, 5 chunks, 4 queries; Recall@2 1.00; MRR 1.00 |
| Text/PDF boundaries | Pass | Path, type, NUL, encryption, page/stream/text bounds covered |
| Runtime answer flow | Pass | Registration/login and authenticated answer BFF passed; duration claim bound to evidence, all result sections visible, no browser console errors |
| Generation safety contract | Pass | Retrieval-first, abstention, schema rejection, forged-citation rejection, extractive support, injection markers, timeout/retry |
| Usage/cost contract | Pass | Content-free record; mock provider; USD 0; no external call |
| Emergency precedence | Pass | Configured red flags bypass retrieval/provider and return zero attempts |
| Workflow controls | Pass | Ownership, order, idempotency, synthetic facts, audit allow-list, negative paths |
| Tracked credential scan | Pass | No selected credential-pattern matches |
| Production npm audit | Pass | 0 production vulnerabilities |
| Repository whitespace check | Pass | `git diff --check` |

## Known warnings

- FastAPI's re-exported `TestClient` emits an upstream Starlette warning that `httpx` support is deprecated in favor of `httpx2`. The tests pass; migration should be evaluated when FastAPI documents the stable path.
- The full development dependency audit reports 19 moderate and 5 high transitive advisories in current Jest and `eslint-config-next` tooling. `npm audit --omit=dev` reports zero vulnerabilities. npm proposes incompatible/unsafe major downgrades, so no forced audit fix was applied.

## Runtime verification scope

The Milestone 6 runtime story was: authenticated workspace → emergency phrase → same-origin safety BFF → deterministic policy → application-owned alert with AI bypass; then workflow start → fixed questions → review → completion. Server logs showed expected 200/201 responses and the browser console had no errors. No hosted LLM call, model download, Atlas service, upload, or real patient data was used.
