"""Fixtures for redaction filter tests."""

import logging

import pytest

from logging_suite.logging.redaction import RedactionFilter


class TestHandler(logging.Handler):
    """Test handler that captures emitted records."""

    def __init__(self) -> None:
        """Initialize the handler."""
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        """Capture the record."""
        self.records.append(record)


@pytest.fixture
def redaction_logger() -> logging.Logger:
    """
    Create a fresh logger for each test.

    Used by: TestRedactionClient.
    """
    logger = logging.getLogger("test_redaction")
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    return logger


@pytest.fixture
def redaction_handler() -> TestHandler:
    """
    Create a fresh test handler for each test.

    Used by: no test class yet.
    """
    return TestHandler()


@pytest.fixture
def redaction_filter() -> RedactionFilter:
    """
    Create a RedactionFilter with default patterns.

    Used by: TestRedactionFilter.
    """
    return RedactionFilter.with_defaults()
