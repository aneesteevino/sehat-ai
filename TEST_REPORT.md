# Test Report

Last run: 2026-10-14 (Asia/Karachi)

## Milestone 3 results

| Check | Result | Evidence |
|---|---|---|
| Backend lint | Pass | Ruff: all checks passed |
| Backend unit/API/repository tests | Pass | 23 passed |
| Frontend component/request tests | Pass | 4 suites, 8 tests |
| Frontend lint | Pass | ESLint, zero warnings |
| Frontend typecheck | Pass | TypeScript `--noEmit` |
| Frontend production build | Pass | Next.js 16.4; public/auth pages static; auth handlers and workspace dynamic |
| Runtime registration | Pass | Next.js BFF and FastAPI returned HTTP 201 |
| Runtime protected page | Pass | HTTP 200 with authenticated identity rendered |
| Runtime logout/revocation | Pass | Logout HTTP 200; old token rejected by FastAPI with 401; workspace redirected |
| Cookie boundary | Pass | Production cookie was Secure, HTTP-only, SameSite=Strict, host-prefixed |
| Tracked credential scan | Pass | No selected credential-pattern matches |
| Production npm audit | Pass | 0 production vulnerabilities |

## Known warnings

- FastAPI's re-exported `TestClient` emits an upstream Starlette warning that `httpx` support is deprecated in favor of `httpx2`. The tests pass; migration should be evaluated when FastAPI documents the stable path.
- The full development dependency audit reports 19 moderate and 5 high transitive advisories in current Jest and `eslint-config-next` tooling. `npm audit --omit=dev` reports zero vulnerabilities. npm proposes incompatible/unsafe major downgrades, so no forced audit fix was applied.

## Runtime verification scope

The verified story was: Next.js registration Route Handler → FastAPI identity service → Argon2id account and opaque session in the local repository → production-cookie response → server-rendered protected workspace → logout revocation → rejected token. The MongoDB adapter was unit tested but no live Atlas service was available.
