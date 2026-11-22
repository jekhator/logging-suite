"""GRPCCorrelation value object for gRPC adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self
from uuid import uuid4

from logging_suite.logging.adapters.constants import grpc as const

Metadata = tuple[tuple[str, str | bytes], ...]


@dataclass(frozen=True, slots=True)
class GRPCCorrelation:
    """Correlation-ID value object resolved from gRPC invocation metadata or generated."""

    correlation_id: str
    extracted: bool

    def __post_init__(self) -> None:
        """Validate correlation_id against safety rules; raise on invariant breach."""
        if not self._is_safe(self.correlation_id):
            raise ValueError(const.ERR_CORRELATION_ID_UNSAFE)

    @classmethod
    def from_metadata(cls, metadata: Metadata) -> Self:
        """Extract correlation_id from gRPC invocation metadata; generate if absent or unsafe."""
        candidate = dict(metadata).get(const.CORRELATION_ID_KEY)
        if isinstance(candidate, str) and cls._is_safe(candidate):
            return cls(correlation_id=candidate, extracted=True)
        generated_id = uuid4().hex[: const.GENERATED_ID_LENGTH]
        return cls(
            correlation_id=generated_id,
            extracted=False,
        )

    @staticmethod
    def _is_safe(value: str) -> bool:
        """Check if correlation_id is safe (non-empty, within length, no CRLF/null)."""
        if not value or len(value) > const.CORRELATION_ID_MAX_LENGTH:
            return False
        return not any(char in const.UNSAFE_CHARS for char in value)
