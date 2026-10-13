"""API response contracts."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "not_configured", "unavailable"]
    detail: str


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "degraded"]
    service: str
    version: str
    environment: str
    checks: dict[str, HealthCheck]
