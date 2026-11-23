"""Notification dispatcher with guarded delivery, suppression, and egress gating."""

from logging_suite.notifications.dispatch._client import Dispatcher
from logging_suite.notifications.dispatch._objects import DispatchResult

__all__ = ["Dispatcher", "DispatchResult"]
