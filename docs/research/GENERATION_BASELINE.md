# Generation Baseline

Last verified: 2026-10-15.

## Configuration

| Item | Baseline |
|---|---|
| Provider | `mock` |
| Model | `deterministic-evidence-v1` |
| External calls | 0 |
| Model downloads | 0 |
| Estimated inference cost | USD 0 |
| Minimum retrieval score | 0.13 plus substantive lexical overlap |
| Timeout | 8 seconds per attempt |
| Maximum attempts | 2 |
| Output mode | Complete structured object; no partial streaming |
| Claim policy | Evidence-ID allow-list plus extractive support |

## Verified behavior

The automated suite covers authenticated access, an answered handwashing case, missing evidence, direct and retrieved instruction markers, malformed provider objects, invented citation IDs, invented claims with valid IDs, transient retry, terminal timeout, deterministic abstention, and content-free usage accounting. The browser component separately tests answered and abstained displays.

The end-to-end runtime case passed this path:

`Next.js sign-in cookie -> POST /api/answers -> FastAPI authentication -> approved retrieval -> mock generation -> schema and grounding validation -> Next.js no-store response -> accessible answer/evidence/uncertainty/safety display`

## Interpretation

This baseline validates software contracts, not medical quality or LLM capability. The mock is extractive and deterministic; it cannot establish whether a hosted model will follow instructions, paraphrase faithfully, resist attacks, meet latency targets, or remain within a free quota. The corpus contains only two short evaluation summaries and five chunks.
