"""Verify version lockstep across both packages and dist."""

from __future__ import annotations

import importlib.metadata


class TestVersionLockstep:
    """Version consistency across packages and installed dist."""

    def test_all_mixin_roots_version_match(self) -> None:
        """All 5 mixin roots must have same version."""
        from logging_suite.latency.config._version import __version__ as latency_version
        from logging_suite.logging.config._version import (
            __version__ as logging_version,
        )
        from logging_suite.notifications.config._version import (
            __version__ as notifications_version,
        )
        from logging_suite.retry.config._version import __version__ as retry_version
        from logging_suite.sensitivity.config._version import (
            __version__ as sensitivity_version,
        )

        versions = {
            "logging_suite.logging": logging_version, "logging_suite.sensitivity": sensitivity_version,
            "logging_suite.retry": retry_version, "logging_suite.notifications": notifications_version,
            "logging_suite.latency": latency_version
        }

        for name, version in versions.items():
            assert version == logging_version, (
                f"{name} version {version} != logging_suite.logging version {logging_version}"
            )

    def test_package_versions_match_dist_version(self) -> None:
        """Package versions must match the installed mixins dist version."""
        from logging_suite.logging.config._version import __version__ as logging_version

        try:
            dist_version = importlib.metadata.version("logging-suite")
        except importlib.metadata.PackageNotFoundError:
            dist_version = None

        if dist_version is not None:
            assert logging_version == dist_version, (
                f"Package version {logging_version} != "
                f"installed dist version {dist_version}"
            )
