# Next Steps

## Exact next task

Milestone 7: consolidate the verified capabilities into accessible product surfaces with clear patient/clinician boundaries and synthetic data only.

## Planned scope

- Build a coherent conversation surface for grounded questions, citations, abstentions, and emergency escalation.
- Add process-local conversation history through a repository interface; define pagination, deletion, and retention before durable storage.
- Add privacy/settings controls for session and local-history visibility.
- Add a clinician-only draft-review surface using labeled synthetic content; drafts cannot be sent, prescribed, or treated as clinical records.
- Keep the existing fixed symptom workflow and make its boundaries easier to understand.
- Do not enable arbitrary uploads until parser isolation, malware controls, storage, retention, and deletion are selected and tested.

## Safety and verification

- Emergency policy remains earlier than retrieval, generation, and workflows.
- Every answer continues to expose citations, uncertainty, safety limitations, and provider/usage facts.
- Enforce role checks server-side with negative patient/clinician tests.
- Run accessibility, pagination/deletion, authorization, injection, empty/error-state, and full browser-flow tests.
- Run all existing regressions, secret/whitespace scans, storage checks, then update recovery files and push.

## Remaining blockers

- Vercel project scope needs corrected authorization before deployment.
- Atlas and hosted inference remain unverified and optional.
- Upload isolation and durable audit/conversation retention are unresolved.
- Clinical, legal, and privacy review remain mandatory before real-world use.
