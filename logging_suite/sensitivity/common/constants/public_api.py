"""
Public API export names for logging_suite.sensitivity.

Names exported from logging_suite.sensitivity.__init__: Sensitivity, SensitiveRepr,
SensitiveDeclarationError, SensitivityProfile, classify(). PUBLIC_API itself
is exported and self-included in this frozenset.
"""

from typing import Final

PUBLIC_API: Final[frozenset[str]] = frozenset(
    {
        "Sensitivity", "SensitiveDeclarationError", "SensitiveRepr", "SensitivityProfile", "PUBLIC_API", "__version__",
        "classify"
    }
)
