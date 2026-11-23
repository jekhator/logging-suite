"""Constants for the notification backends. Imported as const."""

import logging
from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

"""Logger name shared by the backends and the dispatcher."""

LOGGER_NAME: Final[str] = "logging_suite.notifications"


"""Backend names reported on delivery results."""

BACKEND_NAME_NULL: Final[str] = "NullBackend"
BACKEND_NAME_COLLECTING: Final[str] = "CollectingBackend"
BACKEND_NAME_LOGGING: Final[str] = "LoggingBackend"
BACKEND_NAME_RETRYING: Final[str] = "RetryingBackend"
BACKEND_NAME_DEAD_LETTER_TEMPLATE: Final[str] = (
    "RetryingBackend(dead_letter={dead_letter_name})"
)
BACKEND_NAME_SES: Final[str] = "SESBackend"
BACKEND_NAME_SNS: Final[str] = "SNSBackend"


"""Delivery detail text."""

DETAIL_DISCARDED: Final[str] = "discarded"
DETAIL_COLLECTED_TEMPLATE: Final[str] = "collected event {fingerprint}"
DETAIL_LOGGED_TEMPLATE: Final[str] = "logged {severity}"
DETAIL_EXHAUSTED: Final[str] = "exhausted retries"
DETAIL_NON_RETRYABLE: Final[str] = "non-retryable exception"
DETAIL_DEAD_LETTER_OUTCOME_TEMPLATE: Final[str] = (
    "{prefix}, dead_letter outcome: {outcome}"
)
DETAIL_DEAD_LETTER_FAILED_TEMPLATE: Final[str] = "{prefix} and dead_letter failed"
DETAIL_REASON_TEMPLATE: Final[str] = "{prefix}: {reason}"
DETAIL_MESSAGE_ID_TEMPLATE: Final[str] = "message_id: {message_id}"
DETAIL_SES_ERROR_TEMPLATE: Final[str] = "ses_error: {reason}"
DETAIL_SNS_ERROR_TEMPLATE: Final[str] = "sns_error: {reason}"


"""Log messages and log record extra keys."""

LOG_TITLE_TEMPLATE: Final[str] = "[{category}] {title}"
LOG_DEAD_LETTER_FAILED_EXHAUSTION: Final[str] = (
    "Dead-letter backend failed during exhaustion fallback"
)
LOG_DEAD_LETTER_FAILED_TEMPLATE: Final[str] = "Dead-letter backend failed ({prefix})"
LOG_EXTRA_BODY: Final[str] = "body"
LOG_EXTRA_FINGERPRINT: Final[str] = "fingerprint"
LOG_EXTRA_CORRELATION_ID: Final[str] = "correlation_id"


"""Severity names mapped to standard logging levels."""

SEVERITY_LOG_LEVELS: Final[Mapping[str, int]] = MappingProxyType(
    {"INFO": logging.INFO, "WARNING": logging.WARNING, "CRITICAL": logging.CRITICAL}
)


"""AWS client responses and error codes."""

AWS_RESPONSE_ATTR: Final[str] = "response"
AWS_ERROR_KEY: Final[str] = "Error"
AWS_ERROR_CODE_KEY: Final[str] = "Code"
AWS_NO_ERROR_CODE: Final[str] = ""
AWS_MESSAGE_ID_KEY: Final[str] = "MessageId"
AWS_MESSAGE_ID_UNKNOWN: Final[str] = "unknown"
AWS_RETRYABLE_ERROR_CODES: Final[frozenset[str]] = frozenset(
    {
        "Throttling",
        "ThrottledException",
        "TooManyRequestsException",
        "ServiceUnavailable",
        "InternalError",
    }
)


"""SES raw email."""

EMAIL_HEADER_SUBJECT: Final[str] = "Subject"
EMAIL_HEADER_FROM: Final[str] = "From"
EMAIL_HEADER_TO: Final[str] = "To"
EMAIL_HEADER_CONTENT_DISPOSITION: Final[str] = "Content-Disposition"
EMAIL_ADDRESS_SEPARATOR: Final[str] = ", "
EMAIL_TEXT_SUBTYPE: Final[str] = "plain"
EMAIL_ATTACHMENT_MAIN_TYPE: Final[str] = "application"
EMAIL_ATTACHMENT_SUBTYPE: Final[str] = "octet-stream"
EMAIL_ATTACHMENT_DISPOSITION_TEMPLATE: Final[str] = "attachment; filename= {filename}"
SES_RAW_MESSAGE_DATA_KEY: Final[str] = "Data"


"""SNS message attributes."""

SNS_ATTRIBUTE_CATEGORY: Final[str] = "category"
SNS_ATTRIBUTE_SEVERITY: Final[str] = "severity"
SNS_ATTRIBUTE_FINGERPRINT: Final[str] = "fingerprint"
SNS_ATTRIBUTE_CORRELATION_ID: Final[str] = "correlation_id"
SNS_STRING_VALUE_KEY: Final[str] = "StringValue"
SNS_STRING_ATTRIBUTE: Final[Mapping[str, str]] = MappingProxyType(
    {"DataType": "String"}
)
