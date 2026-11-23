"""logging_suite.notifications: Cross-cutting notification dispatch abstraction."""

from logging_suite.notifications.backends import (
    CollectingBackend,
    DeliveryResult,
    LoggingBackend,
    NotificationBackend,
    NullBackend,
    RetryingBackend,
    SESBackend,
    SNSBackend,
)
from logging_suite.notifications.config._version import __version__
from logging_suite.notifications.dispatch import Dispatcher, DispatchResult
from logging_suite.notifications.events import (
    Attachment,
    NotificationEvent,
    NotificationEventClient,
    Severity,
)
from logging_suite.notifications.suppression import (
    SuppressionPolicy,
    SuppressionTracker,
)

__all__ = [
    "Attachment", "CollectingBackend", "DeliveryResult", "Dispatcher", "DispatchResult", "LoggingBackend",
    "NotificationBackend", "NotificationEvent", "NotificationEventClient", "NullBackend", "RetryingBackend",
    "SESBackend", "SNSBackend", "Severity", "SuppressionPolicy", "SuppressionTracker", "__version__"
]
