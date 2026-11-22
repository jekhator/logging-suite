"""Prove logging_suite.logging never shadows the standard library logging module."""

from __future__ import annotations

import importlib
import logging
import pkgutil
import sysconfig
from pathlib import Path
from typing import Final

import logging_suite
import logging_suite.logging

STDLIB_DIR: Final[Path] = Path(sysconfig.get_paths()["stdlib"]).resolve()
SUITE_PREFIX: Final[str] = "logging_suite."
LOGGING_ATTR: Final[str] = "logging"


class TestStdlibLoggingNotShadowed:
    """Every logging_suite module resolves `import logging` to the standard library."""

    def test_top_level_logging_is_stdlib(self) -> None:
        """The bare name `logging` is the standard library module."""
        stdlib_logging = importlib.import_module("logging")
        assert stdlib_logging is logging  # noqa: S101
        assert stdlib_logging.__name__ == "logging"  # noqa: S101
        assert Path(str(stdlib_logging.__file__)).resolve().is_relative_to(STDLIB_DIR)  # noqa: S101

    def test_suite_subpackage_has_its_own_name(self) -> None:
        """The suite subpackage is addressed only as logging_suite.logging."""
        assert logging_suite.logging.__name__ == "logging_suite.logging"  # noqa: S101
        assert logging_suite.logging is not logging  # noqa: S101

    def test_every_module_binds_stdlib_logging(self) -> None:
        """Any module-level name `logging` in any suite module is the standard library."""
        checked = 0
        for info in pkgutil.walk_packages(logging_suite.__path__, SUITE_PREFIX):
            module = importlib.import_module(info.name)
            bound = module.__dict__.get(LOGGING_ATTR)
            if bound is not None:
                assert bound is logging, f"{info.name} binds a non-stdlib logging"  # noqa: S101
                checked += 1
        assert checked > 0  # noqa: S101
