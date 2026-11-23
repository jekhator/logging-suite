"""Metadata constants for sensitivity classification. Imported as const."""

from __future__ import annotations

from typing import Final

"""Field metadata keys."""

SENSITIVITY_KEY: Final[str] = "sensitivity"


"""Masked repr: the mask token, the repr layout and the adoption error."""

ERR_SENSITIVE_MASKED_REPR: Final[str] = "***MASKED***"
ERR_SENSITIVE_REPR_NOT_OVERRIDDEN: Final[str] = (
    "SensitiveRepr adopter must use @dataclass(..., repr=False) "
    "to avoid silent repr shadowing. "
    "If the adopter has __post_init__, call SensitiveRepr.__post_init__(self) "
    "(explicit call required: slots dataclass re-creation breaks zero-arg super on 3.11)."
)
REPR_FIELD_TEMPLATE: Final[str] = "{name}={value}"
REPR_FIELD_SEPARATOR: Final[str] = ", "
REPR_TEMPLATE: Final[str] = "{class_name}({fields})"
