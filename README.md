# logging-suite

Formerly mixin-suite (renamed 2026-11-22; imports moved under `logging_suite`). The old `mixin-suite` PyPI project stays installable at its last release.

**Composable Python mixins for production services:** structured logging with automatic correlation-ID propagation, sensitive-data masking, retry logic, and latency measurement.

[![PyPI version](https://img.shields.io/pypi/v/logging-suite.svg)](https://pypi.org/project/logging-suite/)
[![CI](https://github.com/jekhator/logging-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/jekhator/logging-suite/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/logging-suite.svg)](https://pypi.org/project/logging-suite/)

This distribution includes five composable roots:

- **logging_suite.logging**: End-to-end correlation-ID propagation, LoggingMixin, ambient logging, FlushOnWarningHandler
- **logging_suite.sensitivity**: Sensitivity classification and dataclass repr-masking via SensitiveRepr
- **logging_suite.retry**: Exponential backoff retry logic via RetryPolicy/RetryExecutor (capability contracts)
- **logging_suite.latency**: High-precision elapsed-time measurement via LatencyClock
- **logging_suite.notifications**: Event dispatch and suppression across multi-step workflows

All five live under the single import root `logging_suite` and can be used independently or together.

## What They Do

### Logging: Correlation-ID Propagation

Track a single request through a distributed system with automatic correlation-ID injection on every log, HTTP call, database query, and background task.

**Before:**
```python
class OrderService:
    def create_order(self, order_id: int):
        print(f"Creating order {order_id}")  # No correlation tracking
        send_notification(order_id)  # Loses request context
```

**After:**
```python
from logging_suite.logging import LoggingMixin, set_correlation_id

set_correlation_id("req-123")

class OrderService(LoggingMixin):
    def create_order(self, order_id: int):
        self.log_info("order.create", order_id=order_id)
        # Logs with: {"correlation_id": "req-123", "order_id": 123, ...}
        send_notification(order_id)  # Correlation ID propagates automatically
```

### Sensitivity: Prevent Accidental Secret Leaks

Mark sensitive fields in dataclasses via field metadata, and adopt SensitiveRepr to auto-mask in repr output.

**Before:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class APICredentials:
    user_id: int
    api_token: str

creds = APICredentials(user_id=1, api_token="sk-abc123xyz")
logger.info("Creds: %s", creds)  # LEAKED: api_token exposed
```

**After:**
```python
from dataclasses import dataclass, field
from logging_suite.sensitivity import Sensitivity, SensitiveRepr

@dataclass(frozen=True, slots=True, repr=False)
class APICredentials(SensitiveRepr):
    user_id: int
    api_token: str = field(metadata={"sensitivity": Sensitivity.SECRET})

creds = APICredentials(user_id=1, api_token="sk-abc123xyz")
logger.info("Creds: %s", creds)  # SAFE: repr shows "api_token=***MASKED***"
```

### Retry: Exponential Backoff with Predicates

Resilient function execution with configurable backoff and predicate-based retry decisions.

```python
from logging_suite.retry import RetryPolicy, RetryExecutor

policy = RetryPolicy(
    max_attempts=3,
    backoff_base_seconds=0.1,
    backoff_multiplier=2.0,
    backoff_max_seconds=1.0,
    jitter=True,
    should_retry=lambda exc: isinstance(exc, ConnectionError)
)

executor = RetryExecutor()

def flaky_api_call(url):
    # Retries on ConnectionError, exponential backoff
    pass

wrapped_call = executor.wrap(flaky_api_call, policy=policy)
result = wrapped_call("https://api.example.com")
```

### Latency: High-Precision Measurement

Measure elapsed time with perf_counter precision and automatic rounding.

```python
from logging_suite.latency import LatencyClock

clock = LatencyClock.start()
# ... do work ...
measurement = clock.stop()
print(f"Elapsed: {measurement.duration_ms} ms")

# Or context-manager form:
with LatencyClock.measure() as clock:
    # ... do work ...
    pass  # Duration auto-measured on exit
```

## Installation

**Base installation:**
```bash
pip install logging-suite
```

or with uv:
```bash
uv add logging-suite
```

**With optional extras for logging adapters:**

Base package includes `logging_suite.logging` (stdlib adapter only) and `logging_suite.sensitivity` (no dependencies).

Optional extras (logging_suite.logging adapters):
- `[aiohttp]`: aiohttp client instrumentation
- `[botocore]`: AWS SDK instrumentation
- `[celery]`: Celery task propagation
- `[fastapi]`: FastAPI middleware and dependencies
- `[grpc]`: gRPC server instrumentation
- `[httpx]`: HTTPX client instrumentation
- `[requests]`: Requests client instrumentation
- `[urllib3]`: urllib3 client instrumentation
- `[all]`: All adapters

Install with extras:
```bash
uv add "logging-suite[httpx,botocore]"  # Multiple extras
uv add "logging-suite[all]"             # All adapters
```

**Python version:** Requires Python 3.11 or later (3.11 and 3.14 tested).

## Quick Start

### Logging with Correlation IDs

#### 1. Add stdlib adapter to your logging config

```python
import logging
from logging_suite.logging.adapters.stdlib.stdlib_client import CorrelationLogFilter

logging.basicConfig()
logging.getLogger().addFilter(CorrelationLogFilter())
```

#### 2. Install FastAPI adapter and add middleware

For FastAPI applications:

```python
from fastapi import FastAPI
from logging_suite.logging.adapters.fastapi import CorrelationIdMiddleware

app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)
```

Or manually for other frameworks:

```python
from logging_suite.logging import set_correlation_id
from fastapi import Request

@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    set_correlation_id(request.headers.get("x-correlation-id", "auto-gen"))
    return await call_next(request)
```

#### 3. Use LoggingMixin in your classes

```python
from logging_suite.logging import LoggingMixin

class UserService(LoggingMixin):
    def create_user(self, user_name: str):
        self.log_info("user.create", user_name=user_name)
        # Logs include correlation_id automatically
```

### Sensitivity: Masking Sensitive Fields

#### 1. Mark sensitive fields and inherit SensitiveRepr

```python
from dataclasses import dataclass, field
from logging_suite.sensitivity import SensitiveRepr, Sensitivity

@dataclass(frozen=True, slots=True, repr=False)
class User(SensitiveRepr):
    id: int
    api_token: str = field(metadata={"sensitivity": Sensitivity.SECRET})
    email: str = field(metadata={"sensitivity": Sensitivity.PII})
    ssn: str = field(metadata={"sensitivity": Sensitivity.PHI})
    name: str
```

#### 2. Use in your code

```python
user = User(
    id=1,
    api_token="sk-123456",
    email="alice@example.com",
    ssn="123-45-6789",
    name="Alice"
)

# Safe for logging
logger.info("User created: %s", repr(user))
# → "User created: User(id=1, api_token=***MASKED***, email=***MASKED***, ssn=***MASKED***, name='Alice')"

# Introspect sensitivity profile
from logging_suite.sensitivity import classify
profile = classify(user)
# → SensitivityProfile(classes=(
#     ('api_token', Sensitivity.SECRET),
#     ('email', Sensitivity.PII),
#     ('ssn', Sensitivity.PHI),
# ))
```

## Run-Verified Examples

These examples are executed against the 0.5.0 release of this suite.

### Logging Example: Correlation-ID Propagation

```python
import logging
from logging_suite.logging import LoggingMixin, set_correlation_id

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - correlation_id=%(correlation_id)s",
)


class DocumentService(LoggingMixin):
    """Service that processes documents with correlation-ID tracking."""

    def upload(self, doc_name: str, size_bytes: int) -> dict:
        """Upload a document and return metadata."""
        self.log_info("upload.initiated", doc_name=doc_name, size_bytes=size_bytes)
        result = {"id": "doc-123", "doc_name": doc_name, "stored": True}
        self.log_info("upload.complete", doc_id=result["id"])
        return result

    def process(self, doc_id: str) -> str:
        """Process a document and return status."""
        self.log_info("process.started", doc_id=doc_id)
        status = "processed"
        self.log_info("process.finished", doc_id=doc_id, status=status)
        return status


# Execute with correlation context
set_correlation_id("req-2026-07-10-001")
service = DocumentService()
result = service.upload("report.pdf", 1024000)
status = service.process("doc-123")
```

**Output (Python 3.14, suite 0.5.0):**
```
2026-07-10 03:05:20,405 - __main__.DocumentService - INFO - upload.initiated - correlation_id=req-2026-07-10-001
2026-07-10 03:05:20,405 - __main__.DocumentService - INFO - upload.complete - correlation_id=req-2026-07-10-001
2026-07-10 03:05:20,405 - __main__.DocumentService - INFO - process.started - correlation_id=req-2026-07-10-001
2026-07-10 03:05:20,405 - __main__.DocumentService - INFO - process.finished - correlation_id=req-2026-07-10-001
```

### Sensitivity Example: Data Masking

```python
from dataclasses import dataclass, field
from logging_suite.sensitivity import SensitiveRepr, classify, Sensitivity

@dataclass(frozen=True, slots=True, repr=False)
class HealthRecord(SensitiveRepr):
    patient_id: int
    ssn: str = field(metadata={"sensitivity": Sensitivity.PHI})
    diagnosis: str = field(metadata={"sensitivity": Sensitivity.PHI})
    treatment_notes: str = field(metadata={"sensitivity": Sensitivity.PHI})
    attending_physician: str

record = HealthRecord(
    patient_id=42,
    ssn="987-65-4321",
    diagnosis="Type 2 Diabetes",
    treatment_notes="Prescribed Metformin 500mg",
    attending_physician="Dr. Smith"
)

# Safe repr
print(repr(record))

# Introspect profile
profile = classify(record)
print(f"PHI fields: {[f for f, s in profile.classes if s == Sensitivity.PHI]}")
```

**Output (Python 3.14, suite 0.5.0):**
```
HealthRecord(patient_id=42, ssn=***MASKED***, diagnosis=***MASKED***, treatment_notes=***MASKED***, attending_physician='Dr. Smith')

PHI fields: ['ssn', 'diagnosis', 'treatment_notes']
```

## Documentation

- **Logging:** See `docs/logging/` for detailed adapter documentation, architecture, and integration patterns
- **Sensitivity:** See `docs/sensitivity/` for classifier API, masking customization, and examples
- **Historical Changelogs:** See `docs/logging/CHANGELOG-history.md` and `docs/sensitivity/CHANGELOG-history.md`

## Public API

### logging_suite.logging (v0.5.0)

Core classes and functions:
- `LoggingMixin`: Base class providing `log_info()`, `log_debug()`, `log_warning()`, `log_error()`, and `log_exception()` methods
- `set_correlation_id(id)`: Set the correlation ID for the current context
- `get_correlation_id()`: Retrieve the current correlation ID
- `clear_correlation_id()`: Clear the correlation ID from context
- `CorrelationContext`: Data class representing correlation metadata
- `ContextVarClient`: Internal context-variable manager for correlation propagation
- `FlushOnWarningHandler`: Logging handler that flushes on WARNING level or above
- `FlushOnWarningConfig`: Configuration for the flush-on-warning handler
- `AmbientLogger`: Namespace for ambient logging functions (log_info, log_debug, log_warning, log_error)
- `PUBLIC_API`: Frozenset of all public names

### logging_suite.sensitivity (v0.5.0)

Core classes and functions:
- `SensitiveRepr`: Base class for dataclasses that masks sensitive fields in repr output
- `classify(dataclass_or_instance)`: Introspect sensitivity profile of a dataclass
- `Sensitivity`: Enum taxonomy: PHI, PII, PCI, SECRET
- `SensitivityProfile`: Data class containing field-to-sensitivity mappings
- `SensitiveDeclarationError`: Exception raised for invalid sensitivity declarations

### logging_suite.retry (v0.5.0)

Core classes and functions:
- `RetryPolicy`: Configuration object for retry behavior (max_attempts, backoff, jitter, predicates)
- `RetryExecutor`: Client for wrapping functions with retry logic via the `wrap(operation, /, policy)` method

## Imports

All packages maintain their original import roots:

```python
# Logging
from logging_suite.logging import LoggingMixin, set_correlation_id, get_correlation_id

# Sensitivity
from logging_suite.sensitivity import SensitiveRepr, classify, Sensitivity

# Retry
from logging_suite.retry import RetryPolicy, RetryExecutor

# Latency
from logging_suite.latency import LatencyClock

# Notifications
from logging_suite.notifications import Dispatcher, SuppressionPolicy
```

## Contributing

This is a consolidation of independently-maintained packages. Bug reports and feature requests should be filed in this repository or the respective upstream repositories:

- Issues for the suite and all five import roots: https://github.com/jekhator/logging-suite/issues

## License

Licensed under the Apache License 2.0. See `LICENSE` for details.
