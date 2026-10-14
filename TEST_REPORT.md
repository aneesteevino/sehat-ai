# Test Report

Last run: 2026-10-15 (Asia/Karachi)

## Milestone 5 results

| Check | Result | Evidence |
|---|---|---|
| Backend lint | Pass | Ruff: all checks passed |
| Backend unit/API/repository/retrieval/generation tests | Pass | 47 passed |
| Frontend component/request tests | Pass | 6 suites, 12 tests |
| Frontend lint | Pass | ESLint, zero warnings |
| Frontend typecheck | Pass | TypeScript `--noEmit` |
| Frontend production build | Pass | Next.js 16.4; evidence/answer BFF routes and workspace dynamically rendered |
| Retrieval baseline | Pass | 2 sources, 5 chunks, 4 queries; Recall@2 1.00; MRR 1.00 |
| Text/PDF boundaries | Pass | Path, type, NUL, encryption, page/stream/text bounds covered |
| Runtime answer flow | Pass | Registration/login and authenticated answer BFF passed; duration claim bound to evidence, all result sections visible, no browser console errors |
| Generation safety contract | Pass | Retrieval-first, abstention, schema rejection, forged-citation rejection, extractive support, injection markers, timeout/retry |
| Usage/cost contract | Pass | Content-free record; mock provider; USD 0; no external call |
| Tracked credential scan | Pass | No selected credential-pattern matches |
| Production npm audit | Pass | 0 production vulnerabilities |
| Repository whitespace check | Pass | `git diff --check` |

## Known warnings

- FastAPI's re-exported `TestClient` emits an upstream Starlette warning that `httpx` support is deprecated in favor of `httpx2`. The tests pass; migration should be evaluated when FastAPI documents the stable path.
- The full development dependency audit reports 19 moderate and 5 high transitive advisories in current Jest and `eslint-config-next` tooling. `npm audit --omit=dev` reports zero vulnerabilities. npm proposes incompatible/unsafe major downgrades, so no forced audit fix was applied.

## Runtime verification scope

The verified story was: reviewed checksum-pinned fixture → bounded extraction → deterministic retrieval → adequacy and instruction gates → zero-cost mock provider → strict schema/evidence-ID/extractive validation → authenticated FastAPI endpoint → server-only Next.js BFF → accessible answer/evidence/uncertainty/safety display. No hosted LLM call, model download, Atlas service, or real patient data was used.
