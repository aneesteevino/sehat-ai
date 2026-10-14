# Next Steps

## Exact next task

Milestone 6: implement controlled, deterministic healthcare workflows without granting the generation provider tools or autonomous actions.

## Files and components

- `application/backend/src/sehat_api/safety/`: deterministic red-flag classification, application-owned escalation responses, and tested policy ordering before retrieval/generation.
- `application/backend/src/sehat_api/workflows/`: typed symptom-questionnaire and document-explanation state machines with explicit allowed transitions.
- `application/backend/src/sehat_api/audit/`: content-minimized security/workflow event contract and in-memory test adapter.
- `application/backend/src/sehat_api/api/`: authenticated workflow endpoints with role checks and bounded inputs.
- `application/frontend/`: accessible guided workflow surfaces that remain visibly distinct from diagnosis or prescribing.
- `tests/`: red-flag precedence, state-transition rejection, authorization, injection, replay/idempotency, audit minimization, and safe failure tests.

## Prerequisites

1. Read the recovery files and confirm `main` is synchronized with `origin/main`.
2. Recheck disk space; do not add a model, agent framework, or paid dependency.
3. Define red-flag categories and application-owned output text before implementing any workflow.
4. Keep emergency routing deterministic and earlier than retrieval or generation.
5. Use synthetic, explicitly labeled workflow fixtures only; do not use real patient data.
6. Do not enable document uploads; arbitrary-file isolation remains unresolved.

## Expected outcome

- Red-flag inputs bypass generation and return a stable escalation contract.
- Workflow steps and transitions are allow-listed in application code; model text cannot select tools or authorize state changes.
- Symptom collection remains a questionnaire, not diagnosis, and document explanation remains limited to synthetic structured facts.
- Security/workflow audit events contain identifiers and decisions, not symptom text, document contents, or model output.
- Automated tests are deterministic and make no paid or external calls.

## Verification

- Run safety precedence, transition, role, audit-minimization, injection, and negative-path tests.
- Run the existing retrieval/generation regression suites.
- Run Next.js unit tests, typecheck, ESLint, production build, and the complete local runtime path.
- Scan tracked files for common secret patterns; record storage and free disk space.
- Update recovery files, then commit and push the verified milestone.

## Remaining blockers

- Vercel project scope needs reconnection or corrected authorization before deployment work.
- MongoDB Atlas and Hugging Face account inspection require usable connectors or user-provided configuration through secure environment settings.
- Clinical, legal, and privacy review remain mandatory before any real-world health use.
