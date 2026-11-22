"""Stdlib-specific pytest fixtures for adapter tests."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from logging_suite.logging import clear_correlation_id


@pytest.fixture(autouse=True)
def reset_correlation() -> Iterator[None]:
    """
    Clear correlation context before and after each test for isolation.

    Used by: TestCorrelationLogFilterAddCorrelationFilter, TestCorrelationLogFilterFilter,
    TestCorrelationLogFilterRealLoggingIntegration, TestFlushOnWarningConfigValidation,
    TestFlushOnWarningHandlerBuffering, TestFlushOnWarningHandlerCapacity, TestFlushOnWarningHandlerEdgeCases,
    TestFlushOnWarningHandlerNullCorrelation, TestFlushOnWarningHandlerTTL, TestFlushOnWarningHandlerThreadSafety.
    """
    clear_correlation_id()
    yield
    clear_correlation_id()
