"""Constants for notification events and the dispatcher. Imported as const."""

from typing import Final

"""Validation error messages."""

ERR_NOTIFICATION_EMPTY_CATEGORY: Final[str] = "category must be non-empty"
ERR_NOTIFICATION_EMPTY_TITLE: Final[str] = "title must be non-empty"
ERR_NOTIFICATION_EMPTY_FINGERPRINT: Final[str] = "fingerprint must be non-empty"
ERR_ATTACHMENT_EMPTY_FILENAME: Final[str] = "attachment filename must be non-empty"
ERR_ATTACHMENT_EMPTY_CONTENT_TYPE: Final[str] = "attachment content_type must be non-empty"


"""Egress gate: what an external backend receives in place of sensitive content."""

EGRESS_TITLE_TEMPLATE: Final[str] = "{category}: {severity} notification"
EGRESS_MASKED_BODY: Final[str] = "[content redacted for external delivery]"
EGRESS_METADATA_COUNT_KEY: Final[str] = "sensitive_count_metadata"


"""Metadata keys read by backends."""

METADATA_KEY_TOPIC_ARN: Final[str] = "topic_arn"


"""Suppression tracker."""

SUPPRESSION_TRACKER_ATTR: Final[str] = "_suppression_tracker"
SUPPRESSION_MAX_CAPACITY: Final[int] = 10000


"""Dispatcher log message and failure detail."""

LOG_BACKEND_FAILED_TEMPLATE: Final[str] = "Backend {backend_name} failed to deliver notification"
DETAIL_EXCEPTION_TEMPLATE: Final[str] = "exception: {error_name}"
