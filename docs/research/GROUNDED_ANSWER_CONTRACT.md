# Grounded Answer Contract

Last verified: 2026-10-15.

## Purpose and scope

Milestone 5 proves the retrieval-to-answer boundary without calling a hosted model, downloading model weights, or claiming medical readiness. The active provider is `mock/deterministic-evidence-v1`. It deterministically selects sentences from approved evidence and has an estimated cost of USD 0.

## Processing order

1. Authenticate the caller.
2. Retrieve up to five chunks from the approved, versioned corpus.
3. Require both the configured rank threshold and a substantive lexical anchor.
4. Exclude retrieved chunks with common instruction-injection markers.
5. Abstain before provider use if no eligible evidence remains.
6. Send only the question and eligible evidence IDs/content through the provider protocol.
7. Apply the bounded timeout/retry policy.
8. Validate the complete provider object against the strict schema.
9. Require every claim to reference only evidence IDs in this request.
10. Require every mock-baseline claim to be extractive from at least one cited chunk.
11. Reject instruction-like claim or uncertainty output.
12. Release the answer only after every check passes.

Partial streaming is intentionally disabled. The complete object must pass schema, evidence-ID, extractive-support, and output checks before user display.

## Response fields

- `status`: `answered` or `abstained`.
- `claims`: plain-text claims with one or more evidence IDs.
- `evidence`: the exact eligible evidence bundle with immutable source/version/locator citations.
- `uncertainty`: limitations specific to the result.
- `safety_notice`: application-owned medical limitation text; the provider cannot replace it.
- `abstention_reason`: `insufficient_evidence` or `unsafe_input` when no answer is released.
- `usage`: provider/model, input/output units, estimated cost, attempts, and elapsed milliseconds.

Usage records contain no question, evidence, claim, email, token, or other content. The current in-memory ledger is operational telemetry only and is not durable.

## Failure behavior

- Missing or inadequate evidence returns HTTP 200 with a deterministic abstention and zero provider attempts.
- Provider timeout or repeated transient failure returns HTTP 503 after at most two attempts by default.
- Invalid schema, forged evidence IDs, non-extractive claims, or unsafe output returns HTTP 502 and no model text.
- All browser answer requests are same-origin JSON POSTs and successful responses are `Cache-Control: no-store`.

## Security limitations

Pattern matching is defense in depth, not proof of prompt-injection resistance. The stronger controls are an approved offline corpus, no tools or side effects, strict schemas, evidence-ID allow-listing, extractive claims, escaped plain-text rendering, and application-owned authorization and safety text. This follows the boundaries in the [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) and [OWASP RAG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html).

Before a real provider is enabled, add provider-specific credentials through secret settings, pin the SDK/model, verify account quota and cost, add deterministic fixtures for its adapter, and define an evidence-entailment policy for paraphrased claims. Do not silently weaken the extractive baseline.
