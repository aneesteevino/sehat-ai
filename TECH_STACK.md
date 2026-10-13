# Verified Technology Stack Baseline

Last verified: 2026-10-14.

| Layer | Selection | Status | Rationale / limitation |
|---|---|---|---|
| Frontend | React + TypeScript + Vite | Proposed | Small static build; straightforward Vercel deployment. |
| Backend | Python 3.12 + FastAPI | Proposed | Installed Python is 3.12.4; typed API and OpenAPI support. |
| Validation | Pydantic | Proposed | Shared typed boundary for requests, provider output, and tool schemas. |
| Database | MongoDB Atlas Free cluster | Conditional | Free tier and Vector Search testing are documented, but this account is not inspectable yet. |
| Unit/integration tests | pytest + frontend test runner | Proposed | External providers mocked by default. |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Candidate, metadata verified | Apache-2.0, 384 dimensions, CPU-capable; quality and local footprint still require measurement. |
| Reranker | `cross-encoder/ms-marco-MiniLM-L6-v2` | Optional candidate | Apache-2.0; about 91 MB weights; include only if evaluation improves. |
| Local generator | `Qwen/Qwen2.5-1.5B-Instruct` | Fallback candidate only | Apache-2.0 metadata verified; full/quantized runtime size and this machine's performance are not tested, so do not download yet. |
| Hosted generation | Hugging Face Inference Providers | Conditional | Free users currently receive $0.10/month in credits, subject to change; not production capacity. |
| Frontend hosting | Vercel Hobby | Conditional | Account reports Hobby; project scope currently returns 403. Function payload limit is 4.5 MB. |
| Source control/CI | GitHub public repository + Actions | Conditional | Connector can access existing repos; public standard Actions runners are documented as free; remote repo does not exist yet. |

## Deliberately excluded for now

- Large local LLMs, GPU frameworks, and full medical datasets.
- A framework-heavy multi-agent system.
- A second vector database before Atlas capability is tested.
- Paid inference endpoints, paid hosting, or automatic billing.
