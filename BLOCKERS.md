# Blockers

Last updated: 2026-10-14 (Asia/Karachi)

## B-001: GitHub repository creation unavailable

- Status: Blocking remote publication, not local development.
- Evidence: GitHub connector supports repository/file/commit operations for existing repositories but exposes no create-repository action. GitHub CLI is not installed. No exact repository named `sehat-ai` was found for the authenticated owner.
- Needed: Create `sehat-ai` through an authorized GitHub UI/API path, or expose repository creation / install and authenticate GitHub CLI.
- Safety: Do not push to a similarly named third-party repository.

## B-002: Vercel project scope unauthorized

- Status: Blocking deployment inspection and creation.
- Evidence: Account identity and Hobby plan are visible, but listing projects for the reported default team returned HTTP 403 for an unauthorized scope.
- Needed: Reconnect Vercel with the intended account/team scope or provide an authorized project scope.
- Impact: Local builds continue; no deployment may be claimed.

## B-003: MongoDB Atlas connector unavailable

- Status: Blocking account-specific database validation.
- Evidence: No callable MongoDB Atlas tools are exposed in this session, and no `MONGODB_URI` environment-variable name is configured.
- Needed: Connect/expose the Atlas integration or later configure a least-privilege URI through local/Vercel secret settings.
- Impact: Use a test adapter until Atlas can be verified. Do not create or modify databases blindly.

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
