# API and Cost Register

Target: USD 0 additional spend. Last reviewed: 2026-10-14 .

| Service | Model/version or resource | Availability verified | Free access requirement | Limitation | Fallback | Planned cost |
|---|---|---:|---|---|---|---:|
| Hugging Face Inference Providers | Provider-dependent routed models | Documentation only | HF account/token; free users currently receive $0.10 monthly credits | Tiny experimental allowance; model/provider availability changes; extra usage requires purchased credits | Mock provider; later local quantized model | $0 |
| Local embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Public model metadata | Download model weights once | Local CPU/RAM/disk use; medical retrieval quality unproven | Deterministic test embeddings initially | $0 |
| Deterministic retrieval baseline | 256-dimensional lexical feature hashing | Implemented and measured | Python standard library only | Lexical rather than semantic; tiny evaluation corpus | Future semantic model only if metrics improve | $0 |
| Deterministic generation baseline | `mock/deterministic-evidence-v1` | Implemented and tested | Python standard library plus existing validation stack | Extractive software-contract baseline; not an LLM and cannot predict hosted quality | Deterministic abstention | $0 |
| Local reranking | `cross-encoder/ms-marco-MiniLM-L6-v2` | Public model metadata | Download roughly 91 MB weights once | Adds latency and dependencies; English/general-domain training | Skip reranker unless metrics improve | $0 |
| Local generation | `Qwen/Qwen2.5-1.5B-Instruct` | Public model metadata | Download weights/runtime | Not yet benchmarked; even a small LLM may be too slow/large for this laptop or serverless hosting | Hosted free provider when verified; mock in tests | $0 |
| MongoDB Atlas | Free cluster / Vector Search test use | Official docs only | Atlas account and supported region; one Free cluster per project | Shared resources and operational limits; actual account not connected | Repository test adapter; local ephemeral tests | $0 |
| Vercel | Hobby frontend | Account plan verified | Authorized Hobby account/project | Scope currently 403; usage limits; 4.5 MB function request/response payload | Local frontend; alternate backend host later | $0 |
| GitHub Actions | Standard runners in public repo | Official docs and account access | Public GitHub repository | CI is not configured yet | Run the same checks locally until CI is added | $0 |
| Firecrawl | Connected plan | Account balance verified | Credits | Current balance is -107; no crawl should be started | Official web documentation / manual approved source registry | $0 |
| Google Drive | Connected account | Connector profile verified | Connected Google account | Not a code source of truth; privacy/audit considerations | GitHub and local repository | $0 |

## Source references

- Hugging Face Inference Providers pricing: https://huggingface.co/docs/inference-providers/en/pricing
- Hugging Face model pages: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 and https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2
- MongoDB Atlas Free limits: https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/
- MongoDB Vector Search deployment options: https://www.mongodb.com/docs/vector-search/deployment/deployment-options/
- Vercel Hobby and function limits: https://vercel.com/docs/plans/hobby and https://vercel.com/docs/functions/limitations
- GitHub Actions billing: https://docs.github.com/en/actions/concepts/billing-and-usage

No paid resource or billing setting has been enabled.
