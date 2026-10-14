"""FastAPI application factory and health endpoints."""

import logging
import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sehat_api import __version__
from sehat_api.api.identity import router as identity_router
from sehat_api.config import Settings, get_settings
from sehat_api.identity.service import IdentityService
from sehat_api.logging import configure_logging
from sehat_api.middleware import RequestIdMiddleware
from sehat_api.models import HealthCheck, HealthResponse
from sehat_api.repositories.identity import IdentityRepository, InMemoryIdentityRepository
from sehat_api.repositories.mongo_identity import MongoIdentityRepository

logger = logging.getLogger("sehat_api")


def create_app(
    settings: Settings | None = None,
    identity_repository: IdentityRepository | None = None,
) -> FastAPI:
    """Build the application with explicit, testable settings."""

    active_settings = settings or get_settings()
    configure_logging(active_settings.log_level)

    mongo_repository: MongoIdentityRepository | None = None
    if identity_repository is not None:
        active_repository = identity_repository
        repository_kind = "injected"
    elif active_settings.mongodb_uri is not None:
        mongo_repository = MongoIdentityRepository.from_uri(
            active_settings.mongodb_uri.get_secret_value(),
            active_settings.mongodb_database,
        )
        active_repository = mongo_repository
        repository_kind = "mongodb"
    else:
        active_repository = InMemoryIdentityRepository()
        repository_kind = "memory"

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        if mongo_repository is not None:
            await mongo_repository.initialize()
        try:
            yield
        finally:
            if mongo_repository is not None:
                await mongo_repository.close()

    api = FastAPI(
        title="Sehat AI API",
        summary="Safety-first healthcare knowledge platform API",
        version=__version__,
        docs_url="/docs" if active_settings.app_env != "production" else None,
        redoc_url=None,
        lifespan=lifespan,
    )
    api.state.settings = active_settings
    api.state.identity_repository = active_repository
    api.state.repository_kind = repository_kind
    auth_secret = (
        active_settings.auth_secret.get_secret_value().encode()
        if active_settings.auth_secret
        else secrets.token_bytes(32)
    )
    api.state.identity_service = IdentityService(
        active_repository,
        secret=auth_secret,
        session_ttl=timedelta(minutes=active_settings.session_ttl_minutes),
    )
    api.add_middleware(RequestIdMiddleware)
    api.add_middleware(
        CORSMiddleware,
        allow_origins=[str(active_settings.frontend_origin).rstrip("/")],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Accept", "Authorization", "Content-Type", "X-Request-ID"],
        expose_headers=["X-Request-ID"],
    )
    api.include_router(identity_router)

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
    async def ready(response: Response) -> HealthResponse:
        if mongo_repository is None:
            database_status = "not_configured"
            database_detail = "Using the non-durable local identity repository"
            overall_status = "ok"
        else:
            try:
                await mongo_repository.healthcheck()
                database_status = "ok"
                database_detail = "MongoDB connection is responsive"
                overall_status = "ok"
            except Exception:
                logger.exception("MongoDB readiness check failed")
                database_status = "unavailable"
                database_detail = "MongoDB connection is unavailable"
                overall_status = "degraded"
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(
            status=overall_status,
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
