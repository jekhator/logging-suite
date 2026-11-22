"""AWS SES notification backend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from logging_suite.notifications.backends import _objects as objs
from logging_suite.notifications.common.constants import backends as const
from logging_suite.notifications.events import _objects as event_objs


@dataclass(frozen=True, slots=True)
class SESBackend:
    """
    AWS SES notification backend with attachment support.

    Requires: boto3>=1.28.0 (installed via [ses] extra).
    """

    ses_client: Any
    to_addresses: tuple[str, ...]
    from_address: str

    @property
    def external_egress(self) -> bool:
        """SES sends data externally to AWS."""
        return True

    def send(self, event: event_objs.NotificationEvent) -> objs.DeliveryResult:
        """Send notification email via SES with attachments."""
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        try:
            message = MIMEMultipart()
            message[const.EMAIL_HEADER_SUBJECT] = event.title
            message[const.EMAIL_HEADER_FROM] = self.from_address
            message[const.EMAIL_HEADER_TO] = const.EMAIL_ADDRESS_SEPARATOR.join(
                self.to_addresses
            )

            message.attach(MIMEText(event.body, const.EMAIL_TEXT_SUBTYPE))

            for attachment in event.attachments:
                part = MIMEBase(
                    const.EMAIL_ATTACHMENT_MAIN_TYPE, const.EMAIL_ATTACHMENT_SUBTYPE
                )
                part.set_payload(attachment.content)
                encoders.encode_base64(part)
                disposition = const.EMAIL_ATTACHMENT_DISPOSITION_TEMPLATE.format(
                    filename=attachment.filename
                )
                part.add_header(const.EMAIL_HEADER_CONTENT_DISPOSITION, disposition)
                message.attach(part)

            raw_data = message.as_string()
            response = self.ses_client.send_raw_email(
                RawMessage={const.SES_RAW_MESSAGE_DATA_KEY: raw_data}
            )

            message_id = response.get(
                const.AWS_MESSAGE_ID_KEY, const.AWS_MESSAGE_ID_UNKNOWN
            )
            detail = const.DETAIL_MESSAGE_ID_TEMPLATE.format(message_id=message_id)
            return objs.DeliveryResult(
                delivered=True,
                backend_name=const.BACKEND_NAME_SES,
                detail=detail,
                retryable=False,
            )
        except Exception as error:
            error_response = getattr(error, const.AWS_RESPONSE_ATTR, {})
            error_code = error_response.get(const.AWS_ERROR_KEY, {}).get(
                const.AWS_ERROR_CODE_KEY, const.AWS_NO_ERROR_CODE
            )
            is_retryable = error_code in const.AWS_RETRYABLE_ERROR_CODES
            reason = error_code or error.__class__.__name__
            detail = const.DETAIL_SES_ERROR_TEMPLATE.format(reason=reason)

            return objs.DeliveryResult(
                delivered=False,
                backend_name=const.BACKEND_NAME_SES,
                detail=detail,
                retryable=is_retryable,
            )
