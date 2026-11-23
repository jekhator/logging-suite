"""
logging_suite.sensitivity: sensitive-data classification for frozen dataclasses.

Quick start:
    from dataclasses import dataclass, field
    from logging_suite.sensitivity import classify, Sensitivity

    @dataclass(frozen=True, slots=True)
    class Patient:
        name: str
        ssn: str = field(metadata={"sensitivity": Sensitivity.PHI})

    profile = classify(Patient)
    print(profile.has(Sensitivity.PHI))  # True

Key features:
    - Sensitive-data classification taxonomy (PHI, PII, PCI, SECRET)
    - Field metadata key "sensitivity" for tagged fields
    - Frozen dataclass compatible
"""

from logging_suite.sensitivity.common.constants.public_api import PUBLIC_API
from logging_suite.sensitivity.config._version import __version__
from logging_suite.sensitivity.repr._objects import (
    SensitiveDeclarationError,
    SensitiveRepr,
)
from logging_suite.sensitivity.services.classify import (
    Sensitivity,
    SensitivityProfile,
    classify,
)

__all__ = [
    "PUBLIC_API",
    "Sensitivity",
    "SensitiveDeclarationError",
    "SensitiveRepr",
    "SensitivityProfile",
    "__version__",
    "classify",
]
