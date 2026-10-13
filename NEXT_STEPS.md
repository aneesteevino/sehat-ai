# Next Steps

## Exact next task

Milestone 3: design and implement identity and persistence behind repository/service interfaces, without making Atlas a prerequisite for unit tests.

## Files and components

- `application/backend/src/sehat_api/identity/`: password hashing, session/token contracts, roles, and authorization policies.
- `application/backend/src/sehat_api/repositories/`: protocols plus an in-memory test adapter and conditional MongoDB adapter.
- `application/backend/src/sehat_api/api/`: versioned identity routes and consistent error contracts.
- `application/frontend/app/`: sign-in and role-aware shell routes using server-first App Router patterns.
- `tests/`: deterministic identity, authorization, repository, and API tests.
- `DATABASE_SCHEMA.md` and security documentation.

## Prerequisites

1. Inspect this status file and `BLOCKERS.md`.
2. Confirm `main` is synchronized with `origin/main`.
3. Recheck C: free space before adding dependencies.
4. Select a password hashing library and token/session design after current security guidance review.
5. Keep MongoDB behind an interface until Atlas access is available.

## Planned commands

Exact dependency changes must be reviewed and pinned during the milestone. Do not paste tokens, connection strings, or signing secrets into the shell.

## Expected outcome

- Users can be created and authenticated using secure password hashing in the local test adapter.
- Role-based authorization is enforced in application code and covered by negative tests.
- Persistence contracts support an Atlas implementation without coupling domain logic to the driver.
- Production configuration continues to fail closed when required secrets are absent.

## Verification

- Run identity and authorization unit/API tests.
- Run Next.js unit tests, typecheck, ESLint, and the production build.
- Scan tracked files for common secret patterns.
- Record package sizes and updated free disk space.
- Update all five recovery files, then commit the verified milestone.

## Remaining blockers

- Vercel project scope needs reconnection or corrected authorization before deployment work.
- MongoDB Atlas and Hugging Face account inspection require usable connectors or user-provided configuration through secure environment settings.
