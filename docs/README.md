# logging-suite Documentation

This directory contains comprehensive documentation for the two composable mixins that make up logging-suite:

## logging_suite.logging

**End-to-end correlation-ID propagation across 13 adapters for distributed systems.**

- **[Architecture](logging/architecture/architecture.md)**: System design, correlation context propagation, and integration patterns
- **[Adapters](logging/apps/adapters/)**: Instrumentation for ASGI, WSGI, gRPC, GraphQL, Celery, Botocore, Requests, HTTPX, aiohttp, urllib3, WebSocket, Cloud, and Stdlib
  - [ASGI Adapter](logging/apps/adapters/asgi.md)
  - [WSGI Adapter](logging/apps/adapters/wsgi.md)
  - [gRPC Adapter](logging/apps/adapters/grpc.md)
  - [GraphQL Adapter](logging/apps/adapters/graphql.md)
  - [Celery Adapter](logging/apps/adapters/celery.md)
  - [Botocore Adapter](logging/apps/adapters/botocore.md)
  - [Requests Adapter](logging/apps/adapters/requests.md)
  - [HTTPX Adapter](logging/apps/adapters/httpx.md)
  - [aiohttp Adapter](logging/apps/adapters/aiohttp.md)
  - [urllib3 Adapter](logging/apps/adapters/urllib3.md)
  - [WebSocket Adapter](logging/apps/adapters/websocket.md)
  - [Cloud Adapter](logging/apps/adapters/cloud.md)
  - [Stdlib Adapter](logging/apps/adapters/stdlib.md)
- **[Decorators](logging/apps/decorators/logged.md)**: The @logged decorator was removed in 0.6.0; this page shows the LoggingMixin replacement
- **[Correlation Context](logging/apps/context/correlation.md)**: ContextVar-based correlation ID propagation
- **[LoggingMixin](logging/apps/mixin/mixin.md)**: Base class providing log_info(), log_debug(), and @logged support
- **[Security Audit](logging/apps/security-audit.md)**: CRLF injection prevention, sanitization, and adapter safety
- **[Historical Changelog](logging/CHANGELOG-history.md)**: Release notes for prior versions of logging_suite.logging

## logging_suite.sensitivity

**Decorator-based sensitivity classification and masking for frozen dataclasses.**

- **[Architecture](sensitivity/architecture/architecture.md)**: System design and masking strategy
- **[Sensitive Decorator](sensitivity/apps/decorators/sensitive.md)**: Class-level decorator enabling automatic masking
- **[Compliance Policies](sensitivity/apps/decorators/compliance.md)**: Taxonomy-driven field classification
- **[Classification API](sensitivity/apps/decorators/policies.md)**: The policy classes were removed in 0.6.0; this page shows field metadata, SensitiveRepr and classify()
- **[Classify Service](../logging_suite/sensitivity/services/classify/classify_objects.py)**: Field introspection and sensitivity profile generation (PHI, PII, PCI, SECRET)
- **[Status](sensitivity/STATUS.md)**: Current feature coverage and known limitations
- **[Historical Changelog](sensitivity/CHANGELOG-history.md)**: Release notes for prior versions of logging_suite.sensitivity

## Security & Code Reviews

- [logging_suite.logging audits](logging/audits/): Per-adapter and cross-feature security assessments
- [logging_suite.logging reviews](logging/reviews/): Code review findings and resolution
- [logging_suite.sensitivity audits](sensitivity/audits/): Decorator and classification layer security analysis
- [logging_suite.sensitivity reviews](sensitivity/reviews/): Code review findings and resolution

## Getting Started

- See `README.md` in the repository root for installation and quick-start examples.
- See `CONTRIBUTING.md` for development setup and testing procedures.
- See `SECURITY.md` for vulnerability reporting.
