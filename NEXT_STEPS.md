# Next Steps

## Exact next task

Milestone 5: implement grounded answer generation behind a provider interface, using a deterministic mock first and keeping real hosted inference optional.

## Files and components

- `application/backend/src/sehat_api/generation/`: provider protocol, deterministic mock, timeout/retry policy, structured output schema, and usage accounting.
- `application/backend/src/sehat_api/api/`: authenticated answer route that always retrieves evidence before generation.
- `application/frontend/`: answer preview that visibly separates answer, evidence, uncertainty, and safety limitations.
- `tests/`: schema failures, missing evidence, citation integrity, timeout, retry, prompt injection, abstention, and cost accounting.
- Grounded-answer and provider-operation documentation.

## Prerequisites

1. Inspect this status file and `BLOCKERS.md`.
2. Confirm `main` is synchronized with `origin/main`.
3. Recheck C: free space before adding dependencies.
4. Define the answer schema and deterministic abstention rules before selecting a provider.
5. Use a mock provider for all automated tests and measure the complete retrieval-to-answer contract.
6. Inspect current hosted-provider availability only if a real smoke test becomes necessary; do not enable billing.

## Planned commands

Do not add an agent framework or download a local generator. Review and pin any provider SDK only after its necessity, current version, free allowance, and fallback are recorded.

## Expected outcome

- Every generated claim is tied to supplied evidence IDs and validated against the retrieval bundle.
- Missing or inadequate evidence produces a deterministic abstention rather than an unsupported answer.
- Provider output is schema-validated, bounded by timeout/retry policy, and usage is recorded without sensitive content.
- Tests remain deterministic and make no paid or external inference calls.

## Verification

- Run generation schema, grounding, abstention, timeout, citation, and adversarial-boundary tests.
- Run Next.js unit tests, typecheck, ESLint, and the production build.
- Scan tracked files for common secret patterns.
- Record package sizes and updated free disk space.
- Update recovery files, then commit and push the verified milestone.

## Remaining blockers

- Vercel project scope needs reconnection or corrected authorization before deployment work.
- MongoDB Atlas and Hugging Face account inspection require usable connectors or user-provided configuration through secure environment settings.
