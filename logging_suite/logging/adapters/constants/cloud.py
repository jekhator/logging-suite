"""Cloud adapter constants. Imported as const."""

from __future__ import annotations

from typing import Final

__all__ = [
    "CORRELATION_ID_HEADER",
    "CORRELATION_ID_KEY",
    "CORRELATION_ID_MAX_LENGTH",
    "ERR_CORRELATION_ID_UNSAFE",
    "EVENT_KEY_DETAIL",
    "EVENT_KEY_HEADERS",
    "EVENT_KEY_MESSAGE_ATTRIBUTES_SQS",
    "EVENT_KEY_MESSAGE_ATTRIBUTES_SNS",
    "EVENT_KEY_RECORDS",
    "EVENT_KEY_SNS",
    "GENERATED_ID_LENGTH",
    "MESSAGE_ATTRIBUTE_STRING_VALUE_KEY_SQS",
    "MESSAGE_ATTRIBUTE_VALUE_KEY_SNS",
    "UNSAFE_HEADER_CHARS",
    "FIRST_RECORD_INDEX",
]


"""Event extraction keys for SNS/SQS messages."""

EVENT_KEY_RECORDS: Final[str] = "Records"
EVENT_KEY_SNS: Final[str] = "Sns"
EVENT_KEY_MESSAGE_ATTRIBUTES_SQS: Final[str] = "messageAttributes"
EVENT_KEY_MESSAGE_ATTRIBUTES_SNS: Final[str] = "MessageAttributes"
EVENT_KEY_HEADERS: Final[str] = "headers"
EVENT_KEY_DETAIL: Final[str] = "detail"


"""SNS and SQS message attribute value keys (AWS uses different casing)."""

MESSAGE_ATTRIBUTE_VALUE_KEY_SNS: Final[str] = "Value"
MESSAGE_ATTRIBUTE_STRING_VALUE_KEY_SQS: Final[str] = "stringValue"


"""Extraction locations."""

CORRELATION_ID_HEADER: Final[str] = "X-Correlation-ID"
CORRELATION_ID_KEY: Final[str] = "correlation_id"


"""Validation."""

CORRELATION_ID_MAX_LENGTH: Final[int] = 128
GENERATED_ID_LENGTH: Final[int] = 12
UNSAFE_HEADER_CHARS: Final[frozenset[str]] = frozenset({"\r", "\n", "\0"})


"""Error messages."""

ERR_CORRELATION_ID_UNSAFE: Final[str] = (
    "correlation_id must be non-empty, within length cap, free of unsafe chars"
)


"""Position of the record read from a batch event."""

FIRST_RECORD_INDEX: Final[int] = 0
