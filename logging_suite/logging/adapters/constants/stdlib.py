"""stdlib logging adapter constants. Imported as const."""

from __future__ import annotations

import logging
from typing import Final

__all__ = [
    "CORRELATION_RECORD_ATTR",
    "UNSET_CORRELATION_ID",
    "DEFAULT_CAPACITY",
    "DEFAULT_FLUSH_LEVEL",
    "DEFAULT_MAX_CORRELATIONS",
    "DEFAULT_TTL_SECONDS",
    "ERR_CAPACITY_POSITIVE",
    "ERR_FLUSH_LEVEL_INVALID",
    "ERR_MAX_CORRELATIONS_POSITIVE",
    "ERR_TARGET_HANDLER_REQUIRED",
    "ERR_TTL_POSITIVE",
    "LOWER_BOUND_EXCLUSIVE",
    "NULL_CORRELATION_ID",
]


"""LogRecord attribute field name."""

CORRELATION_RECORD_ATTR: Final[str] = "correlation_id"


"""Unset correlation ID sentinel (stamped when context is empty)."""

UNSET_CORRELATION_ID: Final[str] = "-"


"""Flush handler: buffer key for records with no correlation_id set."""

NULL_CORRELATION_ID: Final[str] = "-buffered-"


"""Flush handler: error messages."""

ERR_TARGET_HANDLER_REQUIRED: Final[str] = "target_handler must not be None"
ERR_FLUSH_LEVEL_INVALID: Final[str] = "flush_level must be >= logging.WARNING"
ERR_TTL_POSITIVE: Final[str] = "ttl_seconds must be > 0"
ERR_CAPACITY_POSITIVE: Final[str] = "capacity must be > 0"
ERR_MAX_CORRELATIONS_POSITIVE: Final[str] = "max_correlations must be > 0"


"""Flush handler: default configuration and the bound its sizes must exceed."""

DEFAULT_FLUSH_LEVEL: Final[int] = logging.WARNING
DEFAULT_TTL_SECONDS: Final[int] = 300
DEFAULT_CAPACITY: Final[int] = 1000
DEFAULT_MAX_CORRELATIONS: Final[int] = 100
LOWER_BOUND_EXCLUSIVE: Final[int] = 0
