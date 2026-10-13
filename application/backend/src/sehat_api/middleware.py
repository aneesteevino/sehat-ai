"""HTTP middleware shared by all API routes."""

import re
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

REQUEST_ID_HEADER = "X-Request-ID"
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
request_id_context: ContextVar[str] = ContextVar("request_id", default="unknown")


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach a bounded, log-safe correlation ID to every request and response."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        supplied = request.headers.get(REQUEST_ID_HEADER, "")
        request_id = supplied if REQUEST_ID_PATTERN.fullmatch(supplied) else str(uuid4())
        token = request_id_context.set(request_id)
        request.state.request_id = request_id
        try:
            response = await call_next(request)
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            request_id_context.reset(token)
