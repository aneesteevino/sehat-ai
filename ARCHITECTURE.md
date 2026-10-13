# Architecture

## System boundary

```text
Browser
  -> Next.js App Router UI + Tailwind CSS (Vercel candidate)
      -> FastAPI application service (portable hosting)
          -> Auth/RBAC and audit layer
          -> Safety policy engine (deterministic)
          -> LLM provider interface -> mock / verified hosted provider
          -> RAG service -> embeddings -> vector + keyword retrieval
          -> Document service -> isolated extraction and validation
          -> MongoDB repository interface -> Atlas / test adapter
```

## Trust boundaries

- User messages, uploaded files, and retrieved documents are untrusted data.
- The frontend never receives database or provider credentials.
- Retrieved text cannot issue application instructions or select tools.
- LLM responses are untrusted until schema, safety, and citation validation pass.
- Only application-controlled code may authorize database writes or workflow transitions.

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

## Deployment posture

The Next.js frontend uses server components by default and small client components only where browser state or interactivity is required. Tailwind CSS is the styling system; global CSS is limited to design tokens and document defaults. The frontend can use Vercel. The backend stays portable until file upload, duration, cold-start, model loading, and zero-cost constraints are tested. Large files should eventually use direct object-storage uploads rather than transit through a Vercel Function; no storage provider is selected yet.
