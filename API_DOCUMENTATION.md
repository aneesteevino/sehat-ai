# API Documentation

The FastAPI service exposes versioned identity routes under `/api/v1/auth`. Interactive OpenAPI documentation is available at `/docs` outside production.

| Method | Path | Authentication | Result |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | None | Creates a patient account; returns public user fields. |
| `POST` | `/api/v1/auth/login` | None | Returns an opaque bearer session and public user fields. |
| `GET` | `/api/v1/auth/me` | Bearer token | Returns the authenticated user. |
| `POST` | `/api/v1/auth/logout` | Bearer token | Revokes the current session. |
| `POST` | `/api/v1/knowledge/search` | Bearer token | Accepts JSON `query` and `limit`; returns ranked, versioned evidence and citations, never a generated answer. |
| `POST` | `/api/v1/answers` | Bearer token | Accepts JSON `question`; retrieves first, then returns validated extractive claims or a deterministic abstention. |
| `POST` | `/api/v1/safety/check` | Bearer token | Applies the deterministic red-flag policy and always bypasses AI. |
| `POST` | `/api/v1/workflows` | Bearer token | Starts an owner-scoped controlled workflow with an idempotency key. |
| `POST` | `/api/v1/workflows/{id}/transitions` | Bearer token | Applies an allow-listed, idempotent state transition. |
| `GET` | `/health/live` | None | Process liveness contract. |
| `GET` | `/health/ready` | None | Configuration and database readiness contract. |

The Next.js browser application uses same-origin Route Handlers at `/api/auth/login`, `/api/auth/register`, and `/api/auth/logout`. These handlers keep the backend bearer token in an HTTP-only cookie and do not expose it to client JavaScript.

The browser evidence interface uses same-origin JSON `POST /api/knowledge/search`, which forwards the server-only session to FastAPI and returns a non-cacheable evidence payload. POST keeps potentially sensitive search text out of URLs and routine access logs. Queries are 2–500 characters and limits are 1–20.

The grounded-answer interface uses same-origin JSON `POST /api/answers`. Questions are 2–500 characters. A successful response separates `claims`, `evidence`, `uncertainty`, `safety_notice`, `abstention_reason`, and content-free `usage` metadata. `answered` claims cite only evidence returned in that response; `abstained` responses contain no claims. The active provider is a deterministic zero-cost mock, not a medical model.

Answer status can also be `escalated`. That status contains no claims/evidence, records zero provider attempts, and returns the application-owned emergency response. Browser safety and workflow calls use corresponding same-origin routes under `/api/safety` and `/api/workflows`, with non-cacheable responses.

Errors never include password hashes or tokens. Login failures intentionally return the same message for unknown accounts and incorrect passwords. Request IDs are returned in `X-Request-ID` for server-side correlation.
