# Verified Technology Stack Baseline

Last verified: 2026-10-14.

| Layer | Selection | Status | Rationale / limitation |
|---|---|---|---|
| Frontend | Next.js 16.4 + TypeScript 6.0, App Router | Selected | Server components by default, typed routing, and direct Vercel compatibility. Node.js 22.13 satisfies Next.js requirements. |
| Styling | Tailwind CSS 4.3 | Selected | Responsive, accessible utility styling with a small global design-token layer. |
| Backend | Python 3.12 + FastAPI 0.143 | Selected | Typed API, OpenAPI, identity routes, and portable hosting boundary. |
| Validation | Pydantic 2.14 | Selected | Typed configuration and request/response boundaries. |
| Identity | `pwdlib` Argon2id + opaque revocable sessions | Implemented locally | Raw tokens stay in HTTP-only cookies and are stored only as keyed digests. Production hardening gaps remain documented. |
| Database | PyMongo Async 4.18 + MongoDB Atlas Free candidate | Adapter implemented; live Atlas conditional | Local tests use memory; production requires MongoDB, but this account is not inspectable yet. |
| Unit/integration tests | pytest + Jest/Testing Library | Selected | External providers mocked by default. |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Candidate, metadata verified | Apache-2.0, 384 dimensions, CPU-capable; quality and local footprint still require measurement. |
| Reranker | `cross-encoder/ms-marco-MiniLM-L6-v2` | Optional candidate | Apache-2.0; about 91 MB weights; include only if evaluation improves. |
| Local generator | `Qwen/Qwen2.5-1.5B-Instruct` | Fallback candidate only | Apache-2.0 metadata verified; full/quantized runtime size and this machine's performance are not tested, so do not download yet. |
| Hosted generation | Hugging Face Inference Providers | Conditional | Free users currently receive $0.10/month in credits, subject to change; not production capacity. |
| Frontend hosting | Vercel Hobby | Conditional | Account reports Hobby; project scope currently returns 403. Function payload limit is 4.5 MB. |
| Source control/CI | GitHub public repository + Actions | Repository active; CI not configured | `aneesteevino/sehat-ai` is the verified remote. |

## Deliberately excluded for now

- Large local LLMs, GPU frameworks, and full medical datasets.
- A framework-heavy multi-agent system.
- A second vector database before Atlas capability is tested.
- Paid inference endpoints, paid hosting, or automatic billing.
