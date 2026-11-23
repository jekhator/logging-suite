"""Dispatcher result and related types."""

from __future__ import annotations

from dataclasses import dataclass

from logging_suite.notifications.backends import _objects as backend_objs


@dataclass(frozen=True, slots=True)
class DispatchResult:
    """Outcome of dispatching a single event to all backends."""

    total_backends: int
    results: tuple[backend_objs.DeliveryResult, ...]
    suppressed: bool
