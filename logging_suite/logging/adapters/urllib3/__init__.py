"""logging-mixin urllib3 adapter: urllib3_objects (Urllib3Correlation) + urllib3_client (CorrelationIdPoolManager)."""

from logging_suite.logging.adapters.urllib3.urllib3_client import (
    CorrelationIdPoolManager,
)
from logging_suite.logging.adapters.urllib3.urllib3_objects import (
    Urllib3Correlation,
)

__all__ = [
    "CorrelationIdPoolManager",
    "Urllib3Correlation",
]
