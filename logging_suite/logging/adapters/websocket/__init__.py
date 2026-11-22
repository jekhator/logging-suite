"""logging-mixin WebSocket adapter: websocket_objects (WebSocketCorrelation + types) + websocket_client (CorrelationIdMiddleware)."""

from logging_suite.logging.adapters.websocket.websocket_client import (
    CorrelationIdMiddleware,
)
from logging_suite.logging.adapters.websocket.websocket_objects import (
    Headers,
    WebSocketCorrelation,
)

__all__ = [
    "CorrelationIdMiddleware",
    "Headers",
    "WebSocketCorrelation",
]
