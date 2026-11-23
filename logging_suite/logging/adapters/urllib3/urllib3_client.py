"""CorrelationIdPoolManager: urllib3 PoolManager for correlation-ID propagation."""

from __future__ import annotations

from typing import Any

import urllib3

from logging_suite.logging.adapters.constants import urllib3 as const
from logging_suite.logging.adapters.urllib3 import urllib3_objects as objs


class CorrelationIdPoolManager(urllib3.PoolManager):
    """PoolManager that injects correlation-ID header into outbound requests."""

    def urlopen(self, method: str, url: str, **kwargs: Any) -> urllib3.BaseHTTPResponse:  # type: ignore[override]
        """Inject X-Correlation-ID header from context before send."""
        correlation = objs.Urllib3Correlation.from_context()
        if correlation is not None:
            name, value = correlation.header_tuple
            headers = dict(kwargs.get(const.HEADERS_KWARG) or {})
            headers[name] = value
            kwargs[const.HEADERS_KWARG] = headers
        return super().urlopen(method, url, **kwargs)
