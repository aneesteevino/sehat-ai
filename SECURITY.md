# Security Baseline

Last updated: 2026-10-15 (Asia/Karachi).

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

## Grounded generation controls

- Generation is authenticated, retrieval-first, and limited to the approved offline corpus.
- Rank and substantive-overlap gates abstain before the provider when evidence is inadequate.
- Common direct and indirect instruction markers are rejected in questions, retrieved chunks, claims, and uncertainty text. Pattern matching is explicitly not treated as a complete prompt-injection defense.
- Provider output is an untrusted strict object. Extra fields, missing fields, forged evidence IDs, non-extractive claims, and unsafe output fail closed.
- The current provider has no network, database, filesystem, or tool capability and cannot cause side effects.
- The application, not the provider, owns authorization, the medical safety notice, retry limits, and release decision.
- Output is rendered as escaped plain text; raw HTML and model-authored Markdown are not used.
- Usage records contain operational numbers and identifiers only, never question/evidence/answer content.
- The browser path uses bounded same-origin JSON POSTs and non-cacheable responses.

These controls implement a narrow evaluation baseline. They do not prove resistance to persistent prompt injection or medical groundedness. Broader adversarial evaluation and qualified clinical review remain required.

## Controlled workflow controls

- The emergency policy runs before retrieval and generation; matching requests record zero provider attempts.
- A non-match is not presented as medical clearance. The English phrase list is narrow and incomplete.
- Workflow ownership is server-derived from the authenticated session. Cross-owner access returns not found.
- Only allow-listed state/action pairs can execute. Invalid order and terminal-state mutation fail closed.
- Idempotency prevents accidental duplicate mutations and detects keys reused for different operations.
- Document explanations require explicitly synthetic bounded facts; arbitrary uploads remain disabled.
- Audit metadata has a hard allow-list and excludes health text, selections, document facts, and model content.
