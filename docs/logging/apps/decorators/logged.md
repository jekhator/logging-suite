# logging_suite.logging, the removed @logged Decorator

> **Status:** removed in 0.6.0. `logged`, `LoggedClient` and `LoggedContainer` no longer exist and cannot be imported.
> **Replacement:** adopt `LoggingMixin` and call its `log_*` methods directly.
> **Sibling docs:** `docs/logging/apps/mixin/mixin.md`, `docs/logging/apps/context/correlation.md`.

## What was removed

The 0.6.0 release removed the decorator surface of `logging_suite.logging` (then `mixin_logging`) in favor of capability contracts. See the 0.6.0 "Removed" section of `CHANGELOG.md`. Earlier versions of this page documented `@logged(event)`, which emitted `<event>.start` on entry and `<event>.error` on an exception. Nothing in the package emits those events for you any more.

Other pages under `docs/logging/` (architecture, diagrams, security audit) still mention `@logged` as it existed before 0.6.0; read those mentions as history.

## Replacement

Inherit `LoggingMixin` and log the start and the error yourself:

```python
from logging_suite.logging import LoggingMixin


class OrderService(LoggingMixin):
    def process_order(self, order_id: str) -> str:
        self.log_info("process_order.start", order_id=order_id)
        try:
            return self._charge(order_id)
        except Exception as error:
            self.log_error("process_order.error", error_type=type(error).__name__)
            raise

    def _charge(self, order_id: str) -> str:
        return f"charged:{order_id}"
```

Module-level code without a class can use the ambient functions:

```python
from logging_suite.logging import log_error, log_info

log_info("job.start", job="nightly")
log_error("job.error", error_type="TimeoutError")
```

Every record carries the current correlation id; see `docs/logging/apps/context/correlation.md`.
