"""FastAPI adapter error messages."""

from typing import Final

ERR_FASTAPI_NO_CORRELATION_ID: Final[str] = (
    "Correlation ID not set in context; ensure CorrelationIdMiddleware is installed"
)
