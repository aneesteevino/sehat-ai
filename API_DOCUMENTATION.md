# API Documentation

The FastAPI service exposes versioned identity routes under `/api/v1/auth`. Interactive OpenAPI documentation is available at `/docs` outside production.

| Method | Path | Authentication | Result |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | None | Creates a patient account; returns public user fields. |
| `POST` | `/api/v1/auth/login` | None | Returns an opaque bearer session and public user fields. |
| `GET` | `/api/v1/auth/me` | Bearer token | Returns the authenticated user. |
| `POST` | `/api/v1/auth/logout` | Bearer token | Revokes the current session. |
| `GET` | `/health/live` | None | Process liveness contract. |
| `GET` | `/health/ready` | None | Configuration and database readiness contract. |

The Next.js browser application uses same-origin Route Handlers at `/api/auth/login`, `/api/auth/register`, and `/api/auth/logout`. These handlers keep the backend bearer token in an HTTP-only cookie and do not expose it to client JavaScript.

Errors never include password hashes or tokens. Login failures intentionally return the same message for unknown accounts and incorrect passwords. Request IDs are returned in `X-Request-ID` for server-side correlation.
