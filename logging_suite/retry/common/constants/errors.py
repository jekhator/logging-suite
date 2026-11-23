"""Error messages for retry operations."""

from typing import Final

ERR_RETRY_MAX_ATTEMPTS: Final[str] = "max_attempts must be >= 1"
ERR_RETRY_BACKOFF_BASE: Final[str] = "backoff_base_seconds must be >= 0"
ERR_RETRY_BACKOFF_MULTIPLIER: Final[str] = "backoff_multiplier must be > 0"
ERR_RETRY_BACKOFF_MAX: Final[str] = "backoff_max_seconds must be >= 0"
ERR_RETRY_POLICY_REQUIRED: Final[str] = "policy is required for call()"
