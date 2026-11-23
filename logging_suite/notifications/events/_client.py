"""NotificationEvent factory and client methods."""

from __future__ import annotations

from datetime import datetime, timezone

from logging_suite.notifications.events import _objects as objs


class NotificationEventClient:
    """Factory and utilities for NotificationEvent."""

    @staticmethod
    def create(
        category: str, severity: str | objs.Severity, title: str,
        body: str, fingerprint: str, metadata: tuple[tuple[str, str], ...] = ()
    ) -> objs.NotificationEvent:
        """
        Create a NotificationEvent with auto-captured correlation context.

        Args:
            category:
                Event category (non-empty).
            severity:
                Severity level (INFO, WARNING, CRITICAL).
            title:
                Event title (non-empty).
            body:
                Event body/description.
            fingerprint:
                Unique fingerprint for deduplication (non-empty).
            metadata:
                Optional tuple of (key, value) pairs.

        Returns:
            Configured NotificationEvent with correlation_id and occurred_at populated.
        """
        from logging_suite.logging import get_correlation_id

        resolved_severity = objs.Severity(severity) if isinstance(severity, str) else severity

        now_utc = datetime.now(timezone.utc).isoformat()

        correlation_id = get_correlation_id()

        return objs.NotificationEvent(
            category=category, severity=resolved_severity, title=title, body=body,
            fingerprint=fingerprint, occurred_at=now_utc, correlation_id=correlation_id, metadata=metadata
        )
