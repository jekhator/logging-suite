"""gRPC adapter constants. Imported as const."""

from __future__ import annotations

from typing import Final

__all__ = [
    "CORRELATION_ID_KEY",
    "CORRELATION_ID_MAX_LENGTH",
    "ERR_CORRELATION_ID_UNSAFE",
    "GENERATED_ID_LENGTH",
    "UNSAFE_CHARS",
]


"""Metadata extraction key."""

CORRELATION_ID_KEY: Final[str] = "x-correlation-id"


"""Validation."""

CORRELATION_ID_MAX_LENGTH: Final[int] = 128
GENERATED_ID_LENGTH: Final[int] = 12
UNSAFE_CHARS: Final[frozenset[str]] = frozenset({"\r", "\n", "\0"})


"""Error messages."""

ERR_CORRELATION_ID_UNSAFE: Final[str] = (
    "correlation_id must be non-empty, within length cap, free of unsafe chars"
)
