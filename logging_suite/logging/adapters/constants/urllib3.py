"""urllib3 adapter constants. Imported as const."""

from __future__ import annotations

from typing import Final

__all__ = [
    "CORRELATION_ID_HEADER",
    "CORRELATION_ID_MAX_LENGTH",
    "ERR_CORRELATION_ID_UNSAFE",
    "UNSAFE_HEADER_CHARS",
    "HEADERS_KWARG",
]


"""Outbound header name (matches httpx/requests/aiohttp for round-trip consistency)."""

CORRELATION_ID_HEADER: Final[str] = "X-Correlation-ID"


"""Correlation ID validation."""

CORRELATION_ID_MAX_LENGTH: Final[int] = 128


"""Unsafe header characters: rejected to prevent CRLF injection/null-byte attacks."""

UNSAFE_HEADER_CHARS: Final[frozenset[str]] = frozenset({"\r", "\n", "\0"})


"""Error messages raised at the API surface (source-side; tests use const.ERR_*)."""

ERR_CORRELATION_ID_UNSAFE: Final[str] = (
    "correlation_id must be non-empty, within length cap, free of unsafe chars"
)


"""urlopen keyword argument that carries the request headers."""

HEADERS_KWARG: Final[str] = "headers"
