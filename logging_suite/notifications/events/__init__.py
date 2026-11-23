"""Notification event objects and factory."""

from logging_suite.notifications.events._client import NotificationEventClient
from logging_suite.notifications.events._objects import (
    Attachment,
    NotificationEvent,
    Severity,
)

__all__ = ["Attachment", "NotificationEvent", "NotificationEventClient", "Severity"]
