"""
botocore outbound adapter constants.

Import alias: `from logging_suite.logging.adapters.constants import botocore as const`
"""

from __future__ import annotations

from typing import Final

__all__ = [
    "BEFORE_SIGN_EVENT",
    "CORRELATION_ID_HEADER",
    "CORRELATION_ID_MAX_LENGTH",
    "ERR_CORRELATION_ID_UNSAFE",
    "UNSAFE_HEADER_CHARS",
]


"""Outbound header name (matches inbound ASGI/WSGI for round-trip consistency)."""

CORRELATION_ID_HEADER: Final[str] = "X-Correlation-ID"


"""Correlation ID validation."""

CORRELATION_ID_MAX_LENGTH: Final[int] = 128


"""Botocore event the injection handler registers against (fires before SigV4 signing)."""

BEFORE_SIGN_EVENT: Final[str] = "before-sign"


"""Unsafe header characters: rejected to prevent CRLF injection / null-byte attacks."""

UNSAFE_HEADER_CHARS: Final[frozenset[str]] = frozenset({"\r", "\n", "\0"})


"""Error messages raised at the API surface (source-side; tests match against these via const.ERR_*)."""

ERR_CORRELATION_ID_UNSAFE: Final[str] = (
    "correlation_id must be non-empty, within length cap, free of unsafe chars"
)
