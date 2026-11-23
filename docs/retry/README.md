# logging_suite.retry

Exponential backoff retry through two capability contracts: `RetryPolicy` (a frozen configuration object) and `RetryExecutor` (wraps or calls a function under a policy). The `@retried` decorator and `RetryClient` were removed in 0.6.0.

## Features

- Exponential backoff with a configurable base delay, multiplier and maximum delay cap
- Optional jitter of plus or minus 10 percent on each delay
- Retry decision by predicate (`should_retry`) or by exception types (`retry_on`)
- Supports both sync and async functions

## Installation

logging_suite.retry ships inside logging-suite; there is no separate distribution:

```
uv add logging-suite
```

## Quick Start

### Wrap once, call many

```python
from logging_suite.retry import RetryExecutor, RetryPolicy

policy = RetryPolicy(
    max_attempts=4, backoff_base_seconds=1.0, backoff_multiplier=2.0,
    backoff_max_seconds=60.0, jitter=True, retry_on=(IOError,)
)


def fetch_item(item_id: int) -> str:
    return f"Item#{item_id}"


fetch_with_retry = RetryExecutor().wrap(fetch_item, policy=policy)
result = fetch_with_retry(123)
```

### Per-call form

```python
from logging_suite.retry import RetryExecutor, RetryPolicy

policy = RetryPolicy(
    max_attempts=3, backoff_base_seconds=0.5, backoff_multiplier=2.0,
    backoff_max_seconds=5.0, jitter=False, should_retry=lambda error: isinstance(error, IOError)
)


def unreliable_operation(name: str) -> str:
    return name.upper()


result = RetryExecutor().call(unreliable_operation, "abc", policy=policy)
```

`call` raises `ValueError` when `policy` is omitted.

## RetryPolicy fields

The first five fields are required; there are no defaults for them.

- max_attempts (int): Total number of attempts, including the first (must be >= 1)
- backoff_base_seconds (float): Delay before the first retry (must be >= 0)
- backoff_multiplier (float): Growth factor per attempt (must be > 0)
- backoff_max_seconds (float): Cap on any single delay (must be >= 0)
- jitter (bool): Multiply each delay by a random factor between 0.9 and 1.1
- should_retry (callable, optional): Predicate function(exception) -> bool. Takes precedence over retry_on
- retry_on (tuple of exception types, default empty): Used when should_retry is None

If neither `should_retry` nor `retry_on` is set, nothing is retried: the first exception is raised unchanged.

## Backoff Strategy

After failed attempt n (0-indexed):

- Exponential: backoff_base_seconds * (backoff_multiplier ** n)
- Capped: min(exponential, backoff_max_seconds)
- Jittered (if enabled): capped * random.uniform(0.9, 1.1)

Example with backoff_base_seconds=1.0, backoff_multiplier=2.0, backoff_max_seconds=60.0, jitter=False:

- Attempt 0: Fails, delay = 1s
- Attempt 1: Fails, delay = 2s
- Attempt 2: Fails, delay = 4s
- Attempt 3: Succeeds, or its exception is raised (max_attempts=4)

## RUN-VERIFIED Example

This example was executed with Python 3.12:

```python
from logging_suite.retry import RetryExecutor, RetryPolicy


class MyService:
    attempt_count = 0

    def fetch_item(self, item_id: int) -> str:
        self.attempt_count += 1
        print(f"[Attempt {self.attempt_count}] Fetching item {item_id}...")

        if self.attempt_count < 3:
            raise IOError(f"Network timeout (attempt {self.attempt_count})")

        return f"Item#{item_id}:data=OK"


policy = RetryPolicy(
    max_attempts=4, backoff_base_seconds=0.1, backoff_multiplier=2.0,
    backoff_max_seconds=0.5, jitter=True, retry_on=(IOError,)
)
service = MyService()
fetch = RetryExecutor().wrap(service.fetch_item, policy=policy)
print(f"Result: {fetch(123)}")
```

Output:

```
[Attempt 1] Fetching item 123...
[Attempt 2] Fetching item 123...
[Attempt 3] Fetching item 123...
Result: Item#123:data=OK
```

Explanation: the wrapped call retried twice after the network failures and succeeded on the third attempt.

## Behavior Details

### Exceptions Handled

- The retry decision is made only by `should_retry` or `retry_on`; with neither set, no exception is retried
- An exception the policy does not accept is raised at once, unchanged
- When the attempts are exhausted the last exception is raised unchanged
- The predicate receives the caught exception as-is and owns any unwrapping of `__cause__` chains

### Async Support

`wrap` detects coroutine functions and waits with asyncio.sleep instead of time.sleep.

```python
import asyncio

from logging_suite.retry import RetryExecutor, RetryPolicy

policy = RetryPolicy(
    max_attempts=3, backoff_base_seconds=0.1, backoff_multiplier=2.0,
    backoff_max_seconds=1.0, jitter=True, retry_on=(ConnectionError,)
)


async def fetch_async(url: str) -> str:
    return f"body of {url}"


fetch_with_retry = RetryExecutor().wrap(fetch_async, policy=policy)
print(asyncio.run(fetch_with_retry("https://example.com")))
```

## See Also

- Architecture and flow trace: docs/retry/architecture/flow-trace.md
- logging-suite: https://github.com/jekhator/logging-suite
