"""LoggingMixin: class-bound structured logging with auto-injected correlation IDs."""

from __future__ import annotations

import logging
from typing import Any

from logging_suite.logging.context.constants import correlation as const
from logging_suite.logging.context.correlation.correlation_client import _client


class LoggingMixin:
    """Class-bound logger auto-injecting correlation_id + per-class context."""

    __slots__ = ()

    @property
    def _logger(self) -> logging.Logger:
        """Per-class logger named <module>.<ClassName>."""
        return logging.getLogger(self.__class__.__module__).getChild(self.__class__.__name__)

    def _log_extra(self, extra: dict[str, Any]) -> dict[str, Any]:
        """Build the log extra: correlation_id + the caller's explicit kwargs."""
        correlation_id = _client.current_id() or const.UNSET_CORRELATION_ID
        result: dict[str, Any] = {const.CORRELATION_ID_KEY: correlation_id}
        if extra:
            result.update(extra)
        return result

    def log_debug(self, event: str, **extra: Any) -> None:
        """Log at DEBUG with auto-injected correlation + class context."""
        log_extra = self._log_extra(extra)
        self._logger.debug(event, extra=log_extra)

    def log_info(self, event: str, **extra: Any) -> None:
        """Log at INFO with auto-injected correlation + class context."""
        log_extra = self._log_extra(extra)
        self._logger.info(event, extra=log_extra)

    def log_warning(self, event: str, **extra: Any) -> None:
        """Log at WARNING with auto-injected correlation + class context."""
        log_extra = self._log_extra(extra)
        self._logger.warning(event, extra=log_extra)

    def log_error(self, event: str, **extra: Any) -> None:
        """Log at ERROR with auto-injected correlation + class context."""
        log_extra = self._log_extra(extra)
        self._logger.error(event, extra=log_extra)

    def log_exception(self, event: str, **extra: Any) -> None:
        """Log at ERROR with traceback (use inside an except block)."""
        log_extra = self._log_extra(extra)
        self._logger.exception(event, extra=log_extra)
