"""FastAPI application factory and health endpoints."""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sehat_api import __version__
from sehat_api.config import Settings, get_settings
from sehat_api.logging import configure_logging
from sehat_api.middleware import RequestIdMiddleware
from sehat_api.models import HealthCheck, HealthResponse

logger = logging.getLogger("sehat_api")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the application with explicit, testable settings."""

    active_settings = settings or get_settings()
    configure_logging(active_settings.log_level)

    api = FastAPI(
        title="Sehat AI API",
        summary="Safety-first healthcare knowledge platform API",
        version=__version__,
        docs_url="/docs" if active_settings.app_env != "production" else None,
        redoc_url=None,
    )
    api.state.settings = active_settings
    api.add_middleware(RequestIdMiddleware)
    api.add_middleware(
        CORSMiddleware,
        allow_origins=[str(active_settings.frontend_origin).rstrip("/")],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["Accept", "Content-Type", "X-Request-ID"],
        expose_headers=["X-Request-ID"],
    )

    @api.exception_handler(Exception)
    async def unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        logger.exception("Unhandled request error", extra={"request_id": request_id})
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "The request could not be completed.",
                    "request_id": request_id,
                }
            },
            headers={"X-Request-ID": request_id},
        )

    @api.get("/health/live", response_model=HealthResponse, tags=["health"])
    async def live() -> HealthResponse:
        return HealthResponse(
            status="ok",
            service="sehat-ai-api",
            version=__version__,
            environment=active_settings.app_env,
            checks={"process": HealthCheck(status="ok", detail="API process is responsive")},
        )

    @api.get("/health/ready", response_model=HealthResponse, tags=["health"])
    async def ready() -> HealthResponse:
        database_status = "ok" if active_settings.mongodb_uri else "not_configured"
        database_detail = (
            "Database configuration is present; connectivity is not checked in Milestone 2"
            if active_settings.mongodb_uri
            else "Database is optional until the persistence milestone"
        )
        return HealthResponse(
            status="ok",
            service="sehat-ai-api",
            version=__version__,
            environment=active_settings.app_env,
            checks={
                "configuration": HealthCheck(status="ok", detail="Runtime settings are valid"),
                "database": HealthCheck(status=database_status, detail=database_detail),
            },
        )

    return api


app = create_app()
