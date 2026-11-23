"""Cross-cutting test constants shared across apps (not exported in PUBLIC_API)."""

from __future__ import annotations

from typing import Final

"""Event base names used in @logged decorator tests."""

EVENT_PROCESS: Final[str] = "process"
EVENT_AUDIT: Final[str] = "audit"
EVENT_VALIDATE: Final[str] = "validate"


"""Expected log-event strings emitted by @logged."""

EVENT_PROCESS_START: Final[str] = "process.start"
EVENT_PROCESS_END: Final[str] = "process.end"
EVENT_PROCESS_ERROR: Final[str] = "process.error"
EVENT_AUDIT_START: Final[str] = "audit.start"
EVENT_AUDIT_END: Final[str] = "audit.end"
EVENT_AUDIT_ERROR: Final[str] = "audit.error"
EVENT_VALIDATE_START: Final[str] = "validate.start"
EVENT_VALIDATE_END: Final[str] = "validate.end"
EVENT_VALIDATE_ERROR: Final[str] = "validate.error"


"""Correlation ID test values."""

CORRELATION_ID_TRACE: Final[str] = "test-trace-123"
CORRELATION_ID_TEST: Final[str] = "test-id"
CORRELATION_ID_CUSTOM: Final[str] = "correlation-456"
CORRELATION_ID_FIRST: Final[str] = "first-id"
CORRELATION_ID_SECOND: Final[str] = "second-id"
CORRELATION_ID_SOMETHING: Final[str] = "something"
CORRELATION_ID_SOME: Final[str] = "some-id"
CORRELATION_ID_ID1: Final[str] = "id-1"
CORRELATION_ID_ID2: Final[str] = "id-2"
CORRELATION_ID_ABC: Final[str] = "abc"
CORRELATION_ID_XYZ: Final[str] = "trace-xyz"
CORRELATION_ID_XYZ_SHORT: Final[str] = "trace-abc"


"""Unset correlation ID sentinel."""

UNSET_CORRELATION_MARKER: Final[str] = "-"


"""Custom exception error code."""

ERROR_CODE_CUSTOM: Final[str] = "ERR_CUSTOM"


"""Log record extra-fields for caller kwargs."""

FIELD_USER_ID: Final[str] = "user_id"
FIELD_ACTION: Final[str] = "action"
FIELD_CUSTOM: Final[str] = "custom"
FIELD_MASKED: Final[str] = "masked"
FIELD_INSTANCE: Final[str] = "instance"
FIELD_EXTRA: Final[str] = "extra"


"""Sample field values."""

USER_ID_42: Final[str] = "user-42"
ACTION_CREATE: Final[str] = "create"
USER_ID_GENERIC: Final[str] = "42"


"""Additional correlation ID test values for adapter/WSGI/ASGI."""

CORRELATION_ID_VALID_ID_123: Final[str] = "valid-id-123"
CORRELATION_ID_HEX: Final[str] = "a1b2c3d4e5f6"
CORRELATION_ID_SHOULD_BE_CLEARED: Final[str] = "should-be-cleared"
CORRELATION_ID_ABC_123: Final[str] = "abc-123"
CORRELATION_ID_PRESET_ID_123: Final[str] = "preset-id-123"
CORRELATION_ID_TEST_ID_456: Final[str] = "test-id-456"


"""HTTP-related test constants."""

HTTP_STATUS_200_OK: Final[str] = "200 OK"
HTTP_HEADER_CONTENT_TYPE: Final[str] = "content-type"
HTTP_MIME_TEXT_PLAIN: Final[str] = "text/plain"
HTTP_EVENT_RESPONSE_START: Final[str] = "http.response.start"
HTTP_EVENT_RESPONSE_BODY: Final[str] = "http.response.body"
HTTP_EVENT_REQUEST: Final[str] = "http.request"


"""Exception match strings for pytest.raises()."""

RAISE_MATCH_BOOM: Final[str] = "boom"
RAISE_MATCH_TEST_ERROR: Final[str] = "test error"
RAISE_MATCH_LOGGED_CONTAINER_EVENT_EMPTY: Final[str] = "LoggedContainer.event must be non-empty"


"""Logger names for testing."""

LOGGER_NAME_TEST: Final[str] = "test"
LOGGER_NAME_CUSTOM: Final[str] = "custom_logger"
LOGGER_NAME_RECORD_COLLECTOR_ATTACHED: Final[str] = "test_record_collector.attached"


"""Log record messages and text."""

RECORD_MSG_HELLO: Final[str] = "hello"
RECORD_MSG_WARNING_TEXT: Final[str] = "warning text"
RECORD_MSG_CAPTURED: Final[str] = "captured message"
RECORD_MSG_PREFIX: Final[str] = "msg-"
RECORD_LINE_NO_42: Final[int] = 42


"""Log level names."""

LOG_LEVEL_WARNING: Final[str] = "WARNING"
LOG_LEVEL_INFO: Final[str] = "INFO"


"""Httpx adapter test constants."""

HTTPX_CORR_ID_SAFE: Final[str] = "safe-id-123"
HTTPX_CORR_ID_TEST: Final[str] = "test-id-456"
HTTPX_CORR_ID_ASYNC: Final[str] = "async-id"
HTTPX_CORR_ID_XYZ: Final[str] = "id-xyz"


"""Error message test constants for @logged decorator tests."""

ERROR_MSG_CUSTOM_WORK_FAILED: Final[str] = "something went wrong"
ERROR_MSG_RUNTIME_NO_CODE: Final[str] = "runtime error without code"
