"""Sensitivity classification: taxonomy, the field-to-class profile, and classify()."""

from logging_suite.sensitivity.services.classify.classify_objects import (
    Sensitivity,
    SensitivityProfile,
)

classify = SensitivityProfile.from_dataclass

__all__ = ["Sensitivity", "SensitivityProfile", "classify"]
