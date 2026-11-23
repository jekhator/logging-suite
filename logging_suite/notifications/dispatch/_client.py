"""Dispatcher for guarded notification delivery with suppression and egress gating."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from logging_suite.notifications.backends import _objects as backend_objs
from logging_suite.notifications.common.constants import (
    backends as backend_const,
    events as const,
)
from logging_suite.notifications.dispatch import _objects as objs
from logging_suite.notifications.events import _objects as event_objs
from logging_suite.notifications.suppression import _objects as suppression_objs


@dataclass(slots=True)
class Dispatcher:
    """Guarded dispatcher for notification delivery."""

    backends: tuple[backend_objs.NotificationBackend, ...]
    suppression_policy: suppression_objs.SuppressionPolicy | None = None
    _suppression_tracker: suppression_objs.SuppressionTracker | None = field(default=None, init=False)
    _logger: logging.Logger = field(default_factory=lambda: logging.getLogger(backend_const.LOGGER_NAME), init=False)

    def __post_init__(self) -> None:
        """Initialize suppression tracker if policy provided."""
        if self.suppression_policy:
            object.__setattr__(
                self, const.SUPPRESSION_TRACKER_ATTR,
                suppression_objs.SuppressionTracker(window_seconds=self.suppression_policy.window_seconds)
            )

    def notify(self, event: event_objs.NotificationEvent) -> objs.DispatchResult:
        """
        Dispatch event to all backends with suppression and egress gating.

        Args:
            event:
                The notification event to dispatch.

        Returns:
            DispatchResult with per-backend outcomes and suppression status.
        """
        current_time = time.time()

        if self._suppression_tracker and self._suppression_tracker.is_suppressed(
            event.category, event.fingerprint, current_time
        ):
            total_backends = len(self.backends)
            return objs.DispatchResult(total_backends=total_backends, results=(), suppressed=True)

        if self._suppression_tracker:
            self._suppression_tracker.record(event.category, event.fingerprint, current_time)

        results: list[backend_objs.DeliveryResult] = []

        for backend in self.backends:
            egress_event = self._apply_egress_gate(event, backend)
            try:
                result = backend.send(egress_event)
                results.append(result)
            except Exception as error:
                backend_name = backend.__class__.__name__
                log_message = const.LOG_BACKEND_FAILED_TEMPLATE.format(backend_name=backend_name)
                self._logger.warning(log_message, exc_info=error)
                detail = const.DETAIL_EXCEPTION_TEMPLATE.format(error_name=error.__class__.__name__)
                results.append(
                    backend_objs.DeliveryResult(
                        delivered=False, backend_name=backend_name, detail=detail, retryable=True
                    )
                )

        total_backends = len(self.backends)
        delivery_results = tuple(results)
        return objs.DispatchResult(total_backends=total_backends, results=delivery_results, suppressed=False)

    def _apply_egress_gate(
        self, event: event_objs.NotificationEvent, backend: backend_objs.NotificationBackend
    ) -> event_objs.NotificationEvent:
        """
        Gate sensitive content for external_egress backends.

        Args:
            event:
                Original event.
            backend:
                Target backend.

        Returns:
            Original event if backend is not external_egress; sanitized event otherwise.
        """
        if not backend.external_egress:
            return event

        metadata_counts = len(event.metadata)
        masked_body = const.EGRESS_MASKED_BODY
        derived_title = const.EGRESS_TITLE_TEMPLATE.format(category=event.category, severity=event.severity.value)

        safe_attachments = tuple(attachment for attachment in event.attachments if attachment.egress_safe)

        egress_metadata = ((const.EGRESS_METADATA_COUNT_KEY, str(metadata_counts)),)

        return event_objs.NotificationEvent(
            category=event.category, severity=event.severity, title=derived_title,
            body=masked_body, fingerprint=event.fingerprint, occurred_at=event.occurred_at,
            correlation_id=event.correlation_id, metadata=egress_metadata, attachments=safe_attachments
        )
