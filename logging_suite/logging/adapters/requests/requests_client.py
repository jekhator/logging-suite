"""CorrelationHTTPAdapter: requests HTTPAdapter for correlation-ID propagation."""

from __future__ import annotations

from typing import Any

import requests as requests_lib  # type: ignore[import-untyped]
from requests.adapters import HTTPAdapter  # type: ignore[import-untyped]

from logging_suite.logging.adapters.constants import requests as const
from logging_suite.logging.adapters.requests import requests_objects as objs


class CorrelationHTTPAdapter(HTTPAdapter):
    """HTTPAdapter that injects correlation-ID header into outbound requests."""

    def add_headers(self, request: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Inject X-Correlation-ID header from context before send."""
        super().add_headers(request, **kwargs)
        correlation = objs.RequestsCorrelation.from_context()
        if correlation is None:
            return
        name, value = correlation.header_tuple
        request.headers[name] = value

    @classmethod
    def register_on_session(cls, session: requests_lib.Session) -> None:
        """Mount a CorrelationHTTPAdapter on the session for http:// and https://."""
        session.mount(const.MOUNT_PREFIX_HTTP, cls())
        session.mount(const.MOUNT_PREFIX_HTTPS, cls())

    @classmethod
    def correlation_session(cls) -> requests_lib.Session:
        """Return a new requests.Session with correlation-ID injection mounted."""
        session = requests_lib.Session()
        cls.register_on_session(session)
        return session
