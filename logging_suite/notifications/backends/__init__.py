"""Notification backend protocol and built-in implementations."""

from logging_suite.notifications.backends._client import (
    CollectingBackend,
    LoggingBackend,
    NullBackend,
    RetryingBackend,
)
from logging_suite.notifications.backends._objects import (
    DeliveryResult,
    NotificationBackend,
)
from logging_suite.notifications.backends.ses import SESBackend
from logging_suite.notifications.backends.sns import SNSBackend

__all__ = [
    "CollectingBackend",
    "DeliveryResult",
    "LoggingBackend",
    "NotificationBackend",
    "NullBackend",
    "RetryingBackend",
    "SESBackend",
    "SNSBackend",
]
