# Test Report

Last run: 2026-10-14 (Asia/Karachi)

## Milestone 4 results

| Check | Result | Evidence |
|---|---|---|
| Backend lint | Pass | Ruff: all checks passed |
| Backend unit/API/repository/retrieval tests | Pass | 34 passed |
| Frontend component/request tests | Pass | 5 suites, 10 tests |
| Frontend lint | Pass | ESLint, zero warnings |
| Frontend typecheck | Pass | TypeScript `--noEmit` |
| Frontend production build | Pass | Next.js 16.4; evidence BFF and workspace dynamically rendered |
| Retrieval baseline | Pass | 2 sources, 5 chunks, 4 queries; Recall@2 1.00; MRR 1.00 |
| Text/PDF boundaries | Pass | Path, type, NUL, encryption, page/stream/text bounds covered |
| Runtime evidence flow | Pass | Authenticated workspace and BFF search HTTP 200; expected source ranked first |
| Evidence safety contract | Pass | Versioned locator, untrusted marker, null answer, no-store response |
| Tracked credential scan | Pass | No selected credential-pattern matches |
| Production npm audit | Pass | 0 production vulnerabilities |

## Known warnings

- FastAPI's re-exported `TestClient` emits an upstream Starlette warning that `httpx` support is deprecated in favor of `httpx2`. The tests pass; migration should be evaluated when FastAPI documents the stable path.
- The full development dependency audit reports 19 moderate and 5 high transitive advisories in current Jest and `eslint-config-next` tooling. `npm audit --omit=dev` reports zero vulnerabilities. npm proposes incompatible/unsafe major downgrades, so no forced audit fix was applied.

## Runtime verification scope

The verified story was: reviewed checksum-pinned fixture → bounded extraction → normalization and paragraph chunks → deterministic lexical vectors → hybrid retrieval → versioned evidence citation → authenticated FastAPI endpoint → server-only Next.js BFF → accessible workspace search. No answer model, provider call, model download, Atlas service, or real patient data was used.
