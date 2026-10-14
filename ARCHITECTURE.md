# Architecture

## System boundary

```text
Browser
  -> Next.js App Router UI + Tailwind CSS (Vercel candidate)
      -> same-origin auth Route Handlers (HTTP-only session cookie)
      -> FastAPI application service (portable hosting)
          -> identity service -> Argon2id + opaque revocable sessions + RBAC
          -> Safety policy engine (deterministic)
          -> controlled workflow service -> owner/idempotency/transition gates
          -> content-minimized audit ledger (in-memory baseline)
          -> retrieval service -> deterministic lexical embeddings + evidence citations
          -> generation service -> schema/citation/extractive gates -> mock provider
              -> optional verified hosted provider (not configured)
          -> document service -> bounded approved text/PDF extraction and validation
          -> repository interfaces -> PyMongo Async Atlas / in-memory test adapter
```

## Trust boundaries

- User messages, uploaded files, and retrieved documents are untrusted data.
- The frontend never receives database or provider credentials.
- Retrieved text cannot issue application instructions or select tools.
- LLM responses are untrusted until schema, safety, and citation validation pass.
- Only application-controlled code may authorize database writes or workflow transitions.
- Browser JavaScript never receives the raw session token; Next.js forwards it server-side.

## Core domain modules

- **Identity:** users, roles, sessions, permissions.
- **Conversation:** conversations, messages, structured assistant responses.
- **Knowledge:** sources, versions, licenses, chunks, embeddings, deletion state.
- **Retrieval:** query normalization, candidate search, optional reranking, evidence bundles.
- **Documents:** upload metadata, extraction status, report facts, user-visible explanations.
- **Safety:** emergency rules, prohibited actions, uncertainty and escalation responses.
- **Evaluation:** cases, runs, metrics, versions, and regression thresholds.
- **Audit:** security- and workflow-relevant events without sensitive payloads.

## Response contract

An assistant response will separate:

1. direct answer in plain language;
2. evidence-backed claims;
3. citations to source/version/location;
4. uncertainty and missing information;
5. safety guidance and escalation when applicable.

If evidence is insufficient, the response must abstain from unsupported medical claims.

The Milestone 5 generation path always retrieves first. Its current deterministic mock returns only extractive claims, and application code validates the complete response schema, evidence-ID allow-list, extractive support, instruction markers, timeouts, retries, and usage metadata before release. Streaming is deferred because unvalidated partial output would bypass this release gate. See `docs/research/GROUNDED_ANSWER_CONTRACT.md`.

Milestone 6 places the deterministic emergency policy before retrieval and generation. Emergency matches return an application-owned escalation response with zero provider attempts. Guided workflows use explicit state/action allow-lists, owner checks, idempotency, synthetic bounded inputs, and content-minimized audit events. The provider has no transition or side-effect authority.

## Deployment posture

The Next.js frontend uses server components by default and small client components only where browser state or interactivity is required. Tailwind CSS is the styling system; global CSS is limited to design tokens and document defaults. The frontend can use Vercel. The backend stays portable until file upload, duration, cold-start, model loading, and zero-cost constraints are tested. Large files should eventually use direct object-storage uploads rather than transit through a Vercel Function; no storage provider is selected yet.

Production identity persistence requires MongoDB and fails closed when its URI or the authentication secret is absent. Local tests use an injected in-memory repository. See `DATABASE_SCHEMA.md`, `SECURITY.md`, and `API_DOCUMENTATION.md`.

Knowledge ingestion is registry-driven and offline: reviewed fixtures are checksum-pinned, normalized, paragraph-aware chunked, embedded through an interface, and stored with immutable source-version metadata. The current lexical hashing implementation is a deterministic baseline, not a semantic medical model. Retrieved content remains untrusted. The evidence-search endpoint remains retrieval-only; a separate authenticated endpoint can produce an evaluation-only grounded preview through the zero-cost mock.
