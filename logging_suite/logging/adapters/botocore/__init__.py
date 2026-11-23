"""
logging-mixin botocore adapter: AWS correlation-ID injection.

Surfaces:
- BotocoreCorrelation: value object for safe correlation-ID extraction
- CorrelationIdInjector: event-hook registration for outbound request injection
"""

from logging_suite.logging.adapters.botocore.botocore_client import CorrelationIdInjector
from logging_suite.logging.adapters.botocore.botocore_objects import BotocoreCorrelation

__all__ = ["BotocoreCorrelation", "CorrelationIdInjector"]
