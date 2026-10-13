# Sehat AI

Sehat AI is a safety-first healthcare knowledge and assistance platform under incremental development. It is intended to demonstrate production-minded AI engineering: evidence-grounded answers, traceable retrieval, controlled workflows, document assistance, evaluation, and honest operational limits.

> **Not medical advice.** Sehat AI is not a diagnostic system, does not replace a qualified healthcare professional, and is not clinically validated. Emergency guidance must be deterministic and must never be delayed by model generation.

## Current state

Phase 0 (environment validation and repository foundation) is complete locally. No application feature is represented as operational yet. See [PROJECT_STATUS.md](PROJECT_STATUS.md) and [NEXT_STEPS.md](NEXT_STEPS.md).

## Planned architecture

- React + TypeScript frontend, deployable to Vercel.
- Python 3.12 + FastAPI backend with typed schemas and provider abstractions.
- MongoDB Atlas for application data when account access is verified.
- Local CPU embeddings for development; Atlas Vector Search only after capability testing.
- Hosted LLM access behind a provider interface; mock and deterministic fallbacks keep tests free.
- Evidence records and citation validation as first-class domain objects.

The authoritative architecture is documented in [ARCHITECTURE.md](ARCHITECTURE.md).

## Repository layout

```text
application/       Frontend, backend, and shared contracts
ai/                LLM, RAG, agent workflow, embedding, and evaluation code
data/              Source registry and small, approved evaluation fixtures
docs/              Research, API, security, deployment, and architecture notes
tests/              Cross-component and safety tests
scripts/            Reproducible maintenance and validation commands
```

## Development principles

- No real patient data during development.
- No secrets or model weights in Git.
- No paid service, billing activation, or resource upgrade without explicit approval.
- Model outputs cannot independently diagnose, prescribe, or execute sensitive actions.
- Claims must be tied to retrieved evidence; unsupported answers must abstain.
- Tests use mocks by default to avoid usage charges.

## Quick start

Application setup commands will be added in Milestone 2 after dependencies are pinned and installed. The current milestone contains documentation and repository controls only.

## License

No project license has been selected yet. Do not assume reuse rights until the owner chooses one.
