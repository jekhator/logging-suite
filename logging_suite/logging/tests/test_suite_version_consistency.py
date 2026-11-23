"""Suite-wide version consistency tests."""

from __future__ import annotations


class TestSuiteVersionConsistency:
    """Verify all mixin roots report consistent versions."""

    def test_all_mixin_roots_report_same_version(self) -> None:
        """All five mixin roots (__version__) report identical version string."""
        import logging_suite.latency
        import logging_suite.logging
        import logging_suite.notifications
        import logging_suite.retry
        import logging_suite.sensitivity

        latency_version = logging_suite.latency.__version__
        logging_version = logging_suite.logging.__version__
        notifications_version = logging_suite.notifications.__version__
        sensitivity_version = logging_suite.sensitivity.__version__
        retry_version = logging_suite.retry.__version__

        assert latency_version == logging_version == notifications_version == sensitivity_version == retry_version
        assert logging_version == "0.7.1"
