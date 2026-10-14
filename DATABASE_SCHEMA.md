# Database Schema

Last updated: 2026-10-14 (Asia/Karachi).

MongoDB is accessed only through repository interfaces. Local development and unit tests use a process-local adapter; production requires `MONGODB_URI` and refuses to start without it.

## Implemented collections

### `users`

| Field | Type | Notes |
|---|---|---|
| `_id` | string UUID | Application-generated stable identifier. |
| `email` | string | Trimmed and case-folded before storage; unique index. |
| `display_name` | string | Trimmed, 1–80 characters. |
| `password_hash` | string | Argon2id PHC string; plaintext is never stored. |
| `role` | enum | `patient`, `clinician`, or `admin`; public registration always creates `patient`. |
| `is_active` | boolean | Disabled accounts cannot authenticate. |
| `created_at` | UTC datetime | Indexed for future administrative pagination. |

Indexes: unique `email`; ascending `created_at`.

### `sessions`

| Field | Type | Notes |
|---|---|---|
| `_id` | string UUID | Application-generated identifier. |
| `user_id` | string UUID | Indexed reference to `users._id`. |
| `token_digest` | string | HMAC-SHA-256 digest of the opaque bearer token; unique. Raw tokens are never persisted. |
| `created_at` | UTC datetime | Session issue time. |
| `expires_at` | UTC datetime | Absolute expiry; TTL index uses `expireAfterSeconds: 0`. |
| `revoked_at` | UTC datetime or null | Set on logout; checked on every authentication. |

Indexes: unique `token_digest`; `user_id`; TTL `expires_at`. MongoDB TTL cleanup can lag, so application authentication also rejects expired records immediately.

## Planned collections

### `audit_events`

Planned fields: `_id`, `occurred_at`, `actor_user_id`, `action`, `target_type`, `target_id`, `outcome`, `request_id`, and a small allow-listed metadata object. Passwords, tokens, health text, document contents, and provider secrets must never be recorded. Expected indexes are `occurred_at` and `(actor_user_id, occurred_at)`. A deletion TTL will be added only after a written retention policy is approved.

## Pagination and retention rules

- List endpoints will use opaque cursor pagination ordered by `(created_at, _id)`, with a default page size of 25 and a hard maximum of 100. Offset pagination is not planned for growing or sensitive collections.
- Sessions default to a 60-minute absolute lifetime and are both application-expired and TTL-cleaned.
- User records are retained until an explicit account-deletion workflow is implemented; no silent TTL applies.
- Audit retention is undecided and therefore no destructive audit TTL is implemented.
- No real patient data is permitted during development.

## Atlas validation status

The PyMongo Async adapter and indexes are implemented and unit tested without network access. Live Atlas connectivity, permissions, index creation, and TTL behavior remain unverified because no usable Atlas connection is available.
