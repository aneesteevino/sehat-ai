# Security Baseline

Last updated: 2026-10-14 (Asia/Karachi).

This is an engineering baseline, not a claim of clinical, privacy, or production certification.

## Identity controls implemented

- Passwords are hashed with `pwdlib`'s recommended Argon2id configuration. A dummy hash is verified for unknown accounts to reduce timing-based account discovery.
- Public registration cannot select a privileged role; it always creates a `patient` identity.
- Sessions use 256-bit random opaque tokens. Only an HMAC-SHA-256 digest is stored, enabling revocation without persisting bearer credentials.
- The browser receives the token only as an HTTP-only, `SameSite=Strict` cookie. Production cookies are `Secure`, host-only, and use the `__Host-` prefix.
- Next.js Route Handlers form a backend-for-frontend boundary: client JavaScript never reads the token. Auth mutations reject cross-site browser requests, require JSON, and cap request bodies at 8 KiB.
- FastAPI checks session expiry, revocation, active-user status, and application-owned role policy on every protected request.
- Production startup requires a secret of at least 32 characters and durable MongoDB configuration. Development may use an ephemeral repository and a process-random token-digest key.

## Trust boundaries

- Browser fields, uploads, retrieved content, and model output are untrusted.
- Authorization decisions remain server-side. A browser-supplied role is rejected.
- Database, auth, and AI-provider secrets are server-only and must be supplied through environment secret settings.
- Passwords, raw session tokens, medical text, and document contents must not enter logs or audit metadata.

## Known gaps before public deployment

- Add login and registration rate limits, abuse monitoring, and lockout/backoff policy.
- Add verified-email, password-reset, session-list/revoke-all, and secret-rotation workflows.
- Decide whether MFA or an approved hosted identity provider is required after privacy and threat review.
- Implement audit-event persistence and approve its retention policy.
- Complete live Atlas least-privilege, TLS, network-access, backup, and TTL validation.
- Add dependency scanning and browser/API security tests in CI.
- Obtain qualified healthcare, legal, and privacy review before handling real health data.

## Current threat focus

The current controls address plaintext password exposure, stolen database session replay, basic account enumeration, client-side token access, CSRF-style cross-site mutations, mass assignment of privileged roles, and non-durable production startup. They do not yet make the service suitable for real patient data or internet exposure.

## Knowledge ingestion and retrieval controls

- Only checksum-pinned files from the approved source registry are ingested; runtime network fetching is disabled.
- Text is strict UTF-8 and PDFs are bounded by file size, page count, page-stream size, and extracted-character count. Encrypted and image-only PDFs are rejected.
- Normalization, chunking, embeddings, ranking, and evaluation are deterministic and require no provider call.
- Every evidence item is explicitly marked `untrusted` and carries an immutable source version plus page/paragraph locator.
- The retrieval endpoint returns evidence only and sets `generated_answer` to null. Retrieved instructions have no path to tools or policy.
- Evidence queries use same-origin JSON POST requests so potentially sensitive text does not enter URLs, browser history, or ordinary access logs.
- Arbitrary PDF uploads remain prohibited until parsing is isolated and malware/resource controls are added.
