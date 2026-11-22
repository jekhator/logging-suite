"""Backoff and attempt bounds for retry operations. Imported as backoff_const."""

from typing import Final

"""Jitter: each backoff is scaled by a random factor between these two."""

JITTER_LOWER_FACTOR: Final[float] = 0.9
JITTER_UPPER_FACTOR: Final[float] = 1.1


"""Attempt counting: the last attempt index is max_attempts minus this."""

LAST_ATTEMPT_OFFSET: Final[int] = 1


"""Policy bounds."""

MIN_ATTEMPTS: Final[int] = 1
MIN_BACKOFF_SECONDS: Final[int] = 0
MIN_BACKOFF_MULTIPLIER_EXCLUSIVE: Final[int] = 0
