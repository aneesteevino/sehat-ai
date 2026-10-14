# Controlled Workflow Baseline

Last verified: 2026-10-15.

Milestone 6 adds application-owned safety routing and explicit workflow state machines. It is an engineering demonstration, not medical triage or clinical validation.

## Emergency policy

The narrow phrase policy recognizes configured signals for severe breathing difficulty, severe chest pain/pressure, unconsciousness/unresponsiveness, severe or unstoppable bleeding, and selected stroke signs. An emergency match bypasses retrieval and generation, returns no evidence or model claims, and instructs the user to contact local emergency services immediately.

The categories are supported by current public guidance: [CDC stroke signs](https://www.cdc.gov/stroke/signs-symptoms/) and [MedlinePlus medical-emergency warning signs](https://medlineplus.gov/ency/article/001927.htm). The implementation intentionally says “local emergency services” rather than assuming a country or number.

Phrase matching is conservative and incomplete. A non-match is explicitly not medical clearance. Wording variants, misspellings, languages other than English, context, and emergencies outside the configured categories can be missed. Qualified clinical review and broader evaluation are mandatory before real use.

## Workflow authority

- States: `started -> collecting -> review -> completed`, with `cancelled` allowed from active states.
- Transitions are allow-listed in application code; providers cannot select or execute them.
- Mutations require owner scope and an idempotency key. Replaying the same mutation returns the original result; reusing a key for another mutation fails.
- The symptom demonstration stores only fixed enumerated selections and produces no diagnosis or treatment.
- The document explanation path accepts only explicitly synthetic, bounded label/value facts. Arbitrary uploads remain disabled.
- Audit events record actor/target identifiers, decision metadata, outcome, and request ID. Symptom text, selections, document facts, model output, tokens, and credentials are excluded.

All storage is process-local for this milestone. Restarting the API removes workflows and audit events.
