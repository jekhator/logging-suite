"""Built-in notification backends."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from logging_suite.notifications.backends import _objects as objs
from logging_suite.notifications.common.constants import backends as const
from logging_suite.notifications.events import _objects as event_objs
from logging_suite.retry import RetryPolicy


class NullBackend:
    """No-op backend for testing."""

    @property
    def external_egress(self) -> bool:
        """Does not egress data."""
        return False

    def send(self, event: event_objs.NotificationEvent) -> objs.DeliveryResult:
        """Accept but discard the event."""
        return objs.DeliveryResult(
            delivered=False,
            backend_name=const.BACKEND_NAME_NULL,
            detail=const.DETAIL_DISCARDED,
            retryable=False,
        )


@dataclass(slots=True)
class CollectingBackend:
    """Collects all delivered events for testing and introspection."""

    events: list[event_objs.NotificationEvent] = field(default_factory=list)

    @property
    def external_egress(self) -> bool:
        """Does not egress data."""
        return False

    def send(self, event: event_objs.NotificationEvent) -> objs.DeliveryResult:
        """Collect the event."""
        self.events.append(event)
        detail = const.DETAIL_COLLECTED_TEMPLATE.format(fingerprint=event.fingerprint)
        return objs.DeliveryResult(
            delivered=True,
            backend_name=const.BACKEND_NAME_COLLECTING,
            detail=detail,
            retryable=False,
        )


class LoggingBackend:
    """Emits notifications via stdlib logging."""

    def __init__(self, logger_name: str = const.LOGGER_NAME):
        """
        Initialize with a logger.

        Args:
            logger_name:
                Name of the logger to use.
        """
        self.logger = logging.getLogger(logger_name)

    @property
    def external_egress(self) -> bool:
        """Does not egress data."""
        return False

    def send(self, event: event_objs.NotificationEvent) -> objs.DeliveryResult:
        """Emit the event via logging."""
        log_level = const.SEVERITY_LOG_LEVELS.get(event.severity.value, logging.INFO)
        log_message = const.LOG_TITLE_TEMPLATE.format(
            category=event.category, title=event.title
        )
        log_extra = {
            const.LOG_EXTRA_BODY: event.body, const.LOG_EXTRA_FINGERPRINT: event.fingerprint,
            const.LOG_EXTRA_CORRELATION_ID: event.correlation_id
        }

        self.logger.log(log_level, log_message, extra=log_extra)
        detail = const.DETAIL_LOGGED_TEMPLATE.format(severity=event.severity.value)
        return objs.DeliveryResult(
            delivered=True,
            backend_name=const.BACKEND_NAME_LOGGING,
            detail=detail,
            retryable=False,
        )


@dataclass(frozen=True, slots=True)
class RetryingBackend:
    """Wraps a backend with retry logic via logging_suite.retry."""

    inner: objs.NotificationBackend
    policy: RetryPolicy
    dead_letter: objs.NotificationBackend | None = None

    @property
    def external_egress(self) -> bool:
        """Combines egress status of inner and dead_letter backends."""
        if self.dead_letter is not None:
            return self.inner.external_egress or self.dead_letter.external_egress
        return self.inner.external_egress

    def send(self, event: event_objs.NotificationEvent) -> objs.DeliveryResult:
        """Deliver with retry logic, exhaustion → dead_letter fallback."""
        from logging_suite.retry import RetryExecutor

        class RetryableDeliveryError(Exception):
            """Exception to signal a retryable delivery failure."""

            def __init__(self, result: objs.DeliveryResult):
                self.result = result
                super().__init__(result.detail)

        logger = logging.getLogger(const.LOGGER_NAME)
        executor = RetryExecutor()

        def attempt_send() -> objs.DeliveryResult:
            result = self.inner.send(event)
            if result.retryable:
                raise RetryableDeliveryError(result)
            return result

        def should_retry(error: BaseException) -> bool:
            if isinstance(error, RetryableDeliveryError):
                return True
            if self.policy.should_retry is not None:
                return self.policy.should_retry(error)
            if self.policy.retry_on:
                return isinstance(error, self.policy.retry_on)
            return False

        policy_with_predicate = RetryPolicy(
            max_attempts=self.policy.max_attempts,
            backoff_base_seconds=self.policy.backoff_base_seconds,
            backoff_multiplier=self.policy.backoff_multiplier,
            backoff_max_seconds=self.policy.backoff_max_seconds,
            jitter=self.policy.jitter,
            should_retry=should_retry,
        )

        try:
            result = executor.call(attempt_send, policy=policy_with_predicate)
            return result
        except RetryableDeliveryError as error:
            exhaustion_error = error
            if self.dead_letter is not None:
                try:
                    dead_result = self.dead_letter.send(event)
                    backend_name = const.BACKEND_NAME_DEAD_LETTER_TEMPLATE.format(
                        dead_letter_name=self.dead_letter.__class__.__name__
                    )
                    detail = const.DETAIL_DEAD_LETTER_OUTCOME_TEMPLATE.format(
                        prefix=const.DETAIL_EXHAUSTED, outcome=dead_result.detail
                    )
                    return objs.DeliveryResult(
                        delivered=dead_result.delivered,
                        backend_name=backend_name,
                        detail=detail,
                        retryable=False,
                    )
                except Exception as error:
                    logger.warning(
                        const.LOG_DEAD_LETTER_FAILED_EXHAUSTION,
                        exc_info=error,
                    )
                    detail = const.DETAIL_DEAD_LETTER_FAILED_TEMPLATE.format(
                        prefix=const.DETAIL_EXHAUSTED
                    )
                    return objs.DeliveryResult(
                        delivered=False,
                        backend_name=const.BACKEND_NAME_RETRYING,
                        detail=detail,
                        retryable=False,
                    )
            detail = const.DETAIL_REASON_TEMPLATE.format(
                prefix=const.DETAIL_EXHAUSTED, reason=exhaustion_error.result.detail
            )
            return objs.DeliveryResult(
                delivered=False,
                backend_name=const.BACKEND_NAME_RETRYING,
                detail=detail,
                retryable=False,
            )
        except Exception as error:
            outer_error = error
            is_retryable_exception = should_retry(outer_error)
            detail_prefix = (
                const.DETAIL_EXHAUSTED
                if is_retryable_exception
                else const.DETAIL_NON_RETRYABLE
            )

            if self.dead_letter is not None:
                try:
                    dead_result = self.dead_letter.send(event)
                    backend_name = const.BACKEND_NAME_DEAD_LETTER_TEMPLATE.format(
                        dead_letter_name=self.dead_letter.__class__.__name__
                    )
                    detail = const.DETAIL_DEAD_LETTER_OUTCOME_TEMPLATE.format(
                        prefix=detail_prefix, outcome=dead_result.detail
                    )
                    return objs.DeliveryResult(
                        delivered=dead_result.delivered,
                        backend_name=backend_name,
                        detail=detail,
                        retryable=False,
                    )
                except Exception as error:
                    log_message = const.LOG_DEAD_LETTER_FAILED_TEMPLATE.format(
                        prefix=detail_prefix
                    )
                    logger.warning(
                        log_message,
                        exc_info=error,
                    )
                    detail = const.DETAIL_DEAD_LETTER_FAILED_TEMPLATE.format(
                        prefix=detail_prefix
                    )
                    return objs.DeliveryResult(
                        delivered=False,
                        backend_name=const.BACKEND_NAME_RETRYING,
                        detail=detail,
                        retryable=False,
                    )

            detail = const.DETAIL_REASON_TEMPLATE.format(
                prefix=detail_prefix, reason=outer_error.__class__.__name__
            )
            return objs.DeliveryResult(
                delivered=False,
                backend_name=const.BACKEND_NAME_RETRYING,
                detail=detail,
                retryable=False,
            )
