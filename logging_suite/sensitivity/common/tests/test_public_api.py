"""Test that PUBLIC_API exports are accurate."""

import logging_suite.sensitivity


class TestPublicAPI:
    """Verify logging_suite.sensitivity.__all__ matches public_api.PUBLIC_API."""

    def test_public_api_completeness(self) -> None:
        """All public_api.PUBLIC_API names are exported."""
        from logging_suite.sensitivity.common.constants import public_api

        for name in public_api.PUBLIC_API:
            assert hasattr(logging_suite.sensitivity, name), f"{name} missing from logging_suite.sensitivity.__all__"

    def test_all_exports_match_public_api(self) -> None:
        """All names in logging_suite.sensitivity.__all__ are in public_api.PUBLIC_API."""
        from logging_suite.sensitivity.common.constants import public_api

        for name in logging_suite.sensitivity.__all__:
            assert name in public_api.PUBLIC_API, f"{name} exported but not in PUBLIC_API"
