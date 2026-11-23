"""Redaction filter constants. Imported as const."""

from __future__ import annotations

from typing import Final

__all__ = [
    "MASK_TOKEN",
    "DEFAULT_SENSITIVE_PATTERNS",
    "PRIVATE_ATTRIBUTE_PREFIX",
]


"""Redaction masking parameters."""

MASK_TOKEN: Final[str] = "***REDACTED***"
"""Token used to replace sensitive field values."""


"""Default sensitive field name patterns."""

DEFAULT_SENSITIVE_PATTERNS: Final[frozenset[str]] = frozenset(
    {"password", "secret", "api_key", "token", "auth", "credential", "key"}
)


"""LogRecord attributes with this prefix are left untouched."""

PRIVATE_ATTRIBUTE_PREFIX: Final[str] = "_"
