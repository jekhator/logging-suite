"""AWS SNS notification backend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from logging_suite.notifications.backends import _objects as objs
from logging_suite.notifications.common.constants import (
    backends as const,
    events as event_const,
)
from logging_suite.notifications.events import _objects as event_objs


@dataclass(frozen=True, slots=True)
class SNSBackend:
    """
    AWS SNS notification backend.

    Requires: boto3>=1.28.0 (installed via [sns] extra).
    """

    sns_client: Any
    default_topic_arn: str

    @property
    def external_egress(self) -> bool:
        """SNS sends data externally to AWS."""
        return True

    def send(self, event: event_objs.NotificationEvent) -> objs.DeliveryResult:
        """Publish notification to SNS topic."""
        topic_arn = self.default_topic_arn
        for key, value in event.metadata:
            if key == event_const.METADATA_KEY_TOPIC_ARN:
                topic_arn = value
                break

        title = event.title
        body = event.body

        message_attributes = {
            const.SNS_ATTRIBUTE_CATEGORY: {**const.SNS_STRING_ATTRIBUTE, const.SNS_STRING_VALUE_KEY: event.category},
            const.SNS_ATTRIBUTE_SEVERITY: {
                **const.SNS_STRING_ATTRIBUTE, const.SNS_STRING_VALUE_KEY: event.severity.value
            },
            const.SNS_ATTRIBUTE_FINGERPRINT: {
                **const.SNS_STRING_ATTRIBUTE, const.SNS_STRING_VALUE_KEY: event.fingerprint
            }
        }

        if event.correlation_id:
            message_attributes[const.SNS_ATTRIBUTE_CORRELATION_ID] = {
                **const.SNS_STRING_ATTRIBUTE, const.SNS_STRING_VALUE_KEY: event.correlation_id
            }

        try:
            response = self.sns_client.publish(
                TopicArn=topic_arn, Subject=title, Message=body, MessageAttributes=message_attributes
            )

            message_id = response.get(const.AWS_MESSAGE_ID_KEY, const.AWS_MESSAGE_ID_UNKNOWN)
            detail = const.DETAIL_MESSAGE_ID_TEMPLATE.format(message_id=message_id)
            return objs.DeliveryResult(
                delivered=True, backend_name=const.BACKEND_NAME_SNS, detail=detail, retryable=False
            )
        except Exception as error:
            error_response = getattr(error, const.AWS_RESPONSE_ATTR, {})
            error_code = error_response.get(const.AWS_ERROR_KEY, {}).get(
                const.AWS_ERROR_CODE_KEY, const.AWS_NO_ERROR_CODE
            )
            is_retryable = error_code in const.AWS_RETRYABLE_ERROR_CODES
            reason = error_code or error.__class__.__name__
            detail = const.DETAIL_SNS_ERROR_TEMPLATE.format(reason=reason)

            return objs.DeliveryResult(
                delivered=False, backend_name=const.BACKEND_NAME_SNS, detail=detail, retryable=is_retryable
            )
