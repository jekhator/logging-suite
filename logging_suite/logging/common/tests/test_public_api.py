"""Tests for PUBLIC_API: curated set of public export names from logging_suite.logging."""

from __future__ import annotations

import logging_suite.logging
import logging_suite.logging.adapters.asgi
import logging_suite.logging.adapters.botocore
import logging_suite.logging.adapters.celery
import logging_suite.logging.adapters.cloud
import logging_suite.logging.adapters.httpx
import logging_suite.logging.adapters.requests
import logging_suite.logging.adapters.stdlib
import logging_suite.logging.adapters.wsgi
import logging_suite.logging.context.correlation
from logging_suite.logging.common.constants.public_api import PUBLIC_API


class TestPublicApi:
    """Verify PUBLIC_API is in lockstep with __all__ and all names are importable."""

    def test_public_api_matches_all(self) -> None:
        """PUBLIC_API frozenset equals the package __all__ list."""
        assert set(logging_suite.logging.__all__) == PUBLIC_API  # noqa: S101

    def test_all_public_api_names_are_importable(self) -> None:
        """Every name in PUBLIC_API is accessible from logging_suite.logging."""
        for name in PUBLIC_API:
            assert hasattr(logging_suite.logging, name), f"Missing export: {name}"  # noqa: S101
            assert getattr(logging_suite.logging, name) is not None  # noqa: S101


class TestSubPackagePublicApi:
    """Verify sub-package __all__ exports are importable from their packages."""

    def test_asgi_subpackage_all_exportable(self) -> None:
        """Every name in adapters.asgi.__all__ is importable from adapters.asgi."""
        for name in logging_suite.logging.adapters.asgi.__all__:
            assert hasattr(logging_suite.logging.adapters.asgi, name), (
                f"asgi: Missing {name}"
            )  # noqa: S101

    def test_botocore_subpackage_all_exportable(self) -> None:
        """Every name in adapters.botocore.__all__ is importable from adapters.botocore."""
        for name in logging_suite.logging.adapters.botocore.__all__:
            assert hasattr(logging_suite.logging.adapters.botocore, name), (
                f"botocore: Missing {name}"
            )  # noqa: S101

    def test_celery_subpackage_all_exportable(self) -> None:
        """Every name in adapters.celery.__all__ is importable from adapters.celery."""
        for name in logging_suite.logging.adapters.celery.__all__:
            assert hasattr(logging_suite.logging.adapters.celery, name), (
                f"celery: Missing {name}"
            )  # noqa: S101

    def test_cloud_subpackage_all_exportable(self) -> None:
        """Every name in adapters.cloud.__all__ is importable from adapters.cloud."""
        for name in logging_suite.logging.adapters.cloud.__all__:
            assert hasattr(logging_suite.logging.adapters.cloud, name), (
                f"cloud: Missing {name}"
            )  # noqa: S101

    def test_httpx_subpackage_all_exportable(self) -> None:
        """Every name in adapters.httpx.__all__ is importable from adapters.httpx."""
        for name in logging_suite.logging.adapters.httpx.__all__:
            assert hasattr(logging_suite.logging.adapters.httpx, name), (
                f"httpx: Missing {name}"
            )  # noqa: S101

    def test_requests_subpackage_all_exportable(self) -> None:
        """Every name in adapters.requests.__all__ is importable from adapters.requests."""
        for name in logging_suite.logging.adapters.requests.__all__:
            assert hasattr(logging_suite.logging.adapters.requests, name), (
                f"requests: Missing {name}"
            )  # noqa: S101

    def test_stdlib_subpackage_all_exportable(self) -> None:
        """Every name in adapters.stdlib.__all__ is importable from adapters.stdlib."""
        for name in logging_suite.logging.adapters.stdlib.__all__:
            assert hasattr(logging_suite.logging.adapters.stdlib, name), (
                f"stdlib: Missing {name}"
            )  # noqa: S101

    def test_wsgi_subpackage_all_exportable(self) -> None:
        """Every name in adapters.wsgi.__all__ is importable from adapters.wsgi."""
        for name in logging_suite.logging.adapters.wsgi.__all__:
            assert hasattr(logging_suite.logging.adapters.wsgi, name), (
                f"wsgi: Missing {name}"
            )  # noqa: S101

    def test_correlation_subpackage_all_exportable(self) -> None:
        """Every name in context.correlation.__all__ is importable from context.correlation."""
        for name in logging_suite.logging.context.correlation.__all__:
            assert hasattr(logging_suite.logging.context.correlation, name), (
                f"correlation: Missing {name}"
            )  # noqa: S101
