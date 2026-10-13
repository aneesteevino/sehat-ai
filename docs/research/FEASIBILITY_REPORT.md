# Phase 0 Feasibility Report

Date: 2026-10-14 (Asia/Karachi)

## Outcome

Sehat AI is feasible as a zero-additional-spend local MVP and portfolio codebase. A continuously available public AI demo is not yet guaranteed at zero cost because hosted LLM allowance, backend hosting, and connected database access are unverified or constrained.

## Connected environment

| Integration | Verified operations | Current limitation |
|---|---|---|
| Local workspace | Read/write files, execute commands, install dependencies, run tests, use Git | No application dependencies installed yet |
| GitHub | Authenticate; list/search/read repositories; write files and commits to existing authorized repositories | Cannot create a repository through the exposed connector; `gh` CLI is absent |
| Vercel | Authenticate and inspect account plan; connector supports project/deployment operations in principle | Intended team scope returns 403; no Sehat project is accessible |
| Google Drive | Authenticate and use Drive/Docs/Sheets/Slides operations | Not needed for code source of truth |
| Firecrawl | Connector and credit inspection | -107 remaining credits; no crawl initiated |
| Hugging Face | Public documentation and model metadata via the web | No account connector or token is exposed |
| MongoDB Atlas | Public documentation via the web | No account connector or connection URI is exposed |

## AI model and service shortlist

| Service | Model / version | Availability | Free access | Main limitation | Fallback |
|---|---|---|---|---|---|
| Local embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Public model page verified | Apache-2.0 weights; local compute | General-domain English model; healthcare retrieval quality must be measured | Deterministic test embeddings, then compare another compact model |
| Local reranking | `cross-encoder/ms-marco-MiniLM-L6-v2` | Public model page verified | Apache-2.0 weights; local compute | Adds about 91 MB of weights and CPU latency | No reranking unless evaluation demonstrates benefit |
| Local generation candidate | `Qwen/Qwen2.5-1.5B-Instruct` | Public model metadata verified | Apache-2.0; local compute | Runtime/quantized artifact and latency not benchmarked; not medically specialized | Mock provider for tests; verified hosted provider later |
| Hosted generation | Hugging Face Inference Providers, exact routed model TBD | Service/pricing verified; account access not verified | Free users currently get $0.10 monthly credits, subject to change | Experimental allowance only; provider/model routing changes | Local provider or explicit abstaining demo mode |
| Vector/data service | MongoDB Atlas Free cluster | Official support/limits verified; account access not verified | One Free cluster per project in supported regions | Shared limits and unknown account eligibility; indexes must be tested | In-memory test repository and local retrieval fixture |

Exact hosted model selection is intentionally deferred until the account can list available providers and the application has a provider contract plus usage cap.

## Proposed architecture

Use a React/TypeScript frontend on Vercel, a portable FastAPI service, MongoDB Atlas if verified, local development embeddings, and a provider-neutral generator. Keep emergency triage and all authorization deterministic. Treat uploaded and retrieved text as untrusted. Validate structured model output and citations before display.

## Cost and storage

- Additional cash target: USD 0.
- Current local project size at foundation: approximately 26 KB excluding Git metadata.
- Near-term dependency/model target: under 2 GB; hard project ceiling: 50 GB.
- No model, dataset, package tree, or cloud resource was created in Phase 0.
- Use mocks for CI; never use real provider calls in ordinary tests.

## Roadmap

Proceed through runnable shells, identity/persistence, retrieval, generation, controlled workflows, product surfaces, evaluation/security, deployment readiness, and portfolio release. Acceptance criteria are maintained in `PROJECT_PLAN.md`.

## Recovery

Every milestone updates the five root recovery files before commit. On restart, read those files, inspect `git status`, and verify the recorded tests before continuing. A scheduled five-hour heartbeat is technically available in the desktop product but should only be created when an actual limit interruption occurs and a single resume can be scheduled; no recurring credit polling is justified.

## Genuine blockers

Remote repository creation, Vercel team authorization, Atlas account access, Hugging Face account access, a verified zero-cost hosted generator, and eventual clinical review. Details and required interventions are in `BLOCKERS.md`.
