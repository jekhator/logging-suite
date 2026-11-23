"""requests adapter: outbound correlation-ID propagation via CorrelationHTTPAdapter."""

from logging_suite.logging.adapters.requests.requests_client import (
    CorrelationHTTPAdapter,
)
from logging_suite.logging.adapters.requests.requests_objects import (
    RequestsCorrelation,
)

__all__ = ["CorrelationHTTPAdapter", "RequestsCorrelation"]
