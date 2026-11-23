"""Cloud adapter: inbound correlation-ID extraction from AWS events."""

from logging_suite.logging.adapters.cloud.cloud_client import CloudSetup
from logging_suite.logging.adapters.cloud.cloud_objects import CloudCorrelation

__all__ = ["CloudCorrelation", "CloudSetup"]
