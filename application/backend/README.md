# Sehat AI backend

FastAPI service foundation for Sehat AI.

## Run locally

From the repository root:

```powershell
.\.venv\Scripts\python -m uvicorn sehat_api.main:app --reload --port 8000
```

The package is installed from `application/backend/src` through the root `pyproject.toml`.

## Endpoints

- `GET /health/live` — process liveness; no external dependency checks.
- `GET /health/ready` — configuration readiness and declared dependency state.

Both endpoints include an `X-Request-ID` response header. A valid incoming request ID is preserved; otherwise the service generates a UUID.
