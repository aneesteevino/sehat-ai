# Blockers

Last updated: 2026-10-14 (Asia/Karachi)

## B-001: GitHub repository creation unavailable

- Status: Resolved 2026-10-14.
- Resolution: The user created `https://github.com/aneesteevino/sehat-ai.git`. Repository identity, empty state, default branch, and admin/push permission were verified before it was attached as `origin` and `main` was pushed.

## B-002: Vercel project scope unauthorized

- Status: Blocking deployment inspection and creation.
- Evidence: Account identity and Hobby plan are visible, but listing projects for the reported default team returned HTTP 403 for an unauthorized scope.
- Needed: Reconnect Vercel with the intended account/team scope or provide an authorized project scope.
- Impact: Local builds continue; no deployment may be claimed.

## B-003: MongoDB Atlas connector unavailable

- Status: Blocking account-specific database validation.
- Evidence: No callable MongoDB Atlas tools are exposed in this session, and no `MONGODB_URI` environment-variable name is configured.
- Needed: Connect/expose the Atlas integration or later configure a least-privilege URI through local/Vercel secret settings.
- Impact: The conditional PyMongo adapter and indexes are implemented, but only the in-memory adapter is verified. Do not claim live durability or create/modify Atlas resources blindly.

## B-004: Hugging Face account connector unavailable

- Status: Blocking account/quota-specific inference validation.
- Evidence: No callable Hugging Face tools or `HF_TOKEN` environment-variable name is exposed.
- Needed: Connect/expose the Hugging Face integration or later configure a token through secure settings.
- Impact: Use mock generation and postpone model/API integration. Public model metadata remains researchable.

## B-005: Hosted zero-cost production LLM is not established

- Status: Architectural blocker for a public AI-generation demo, not for core development.
- Evidence: Hugging Face free users currently receive only small monthly experimental inference credits; availability and specific routed models can change.
- Needed: Verify an account-specific free provider/model at integration time, or approve a local/self-hosted deployment design after resource testing.

## B-006: Clinical review absent

- Status: Blocking any clinical-safety or diagnostic-readiness claim.
- Needed: Qualified healthcare and legal/privacy review of content, triage rules, disclosures, and evaluation data before real-world use.
