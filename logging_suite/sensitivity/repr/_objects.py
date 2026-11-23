"""Repr mixin for masking sensitive dataclass fields."""

from __future__ import annotations

from dataclasses import fields, is_dataclass

from logging_suite.sensitivity.common.constants import metadata as const
from logging_suite.sensitivity.services.classify import Sensitivity


class SensitiveDeclarationError(Exception):
    """Raised when SensitiveRepr is adopted without proper repr=False setting."""

    pass


class SensitiveRepr:
    """
    Adoption mixin: masks sensitive fields in dataclass __repr__.

    Inheriting dataclasses MUST use @dataclass(frozen=True, slots=True, repr=False)
    to avoid silent shadowing of the masking __repr__. A __post_init__ guard
    raises SensitiveDeclarationError if repr=False is omitted.

    If an adopting class has its own __post_init__, it must call
    SensitiveRepr.__post_init__(self) to trigger the guard (explicit call required:
    slots dataclass re-creation breaks zero-arg super() on Python 3.11).

    Attributes:
        Inheriting dataclasses may mark fields via
        field(metadata={"sensitivity": Sensitivity.X}).

    Example:
        @dataclass(frozen=True, slots=True, repr=False)
        class Patient(SensitiveRepr):
            name: str
            ssn: str = field(metadata={"sensitivity": Sensitivity.PHI})

        p = Patient(name="Alice", ssn="123-45-6789")
        print(repr(p))
        # Patient(name='Alice', ssn='***MASKED***')
    """

    def __post_init__(self) -> None:
        """
        Guard against silent repr shadowing.

        Raises SensitiveDeclarationError if the adopter's @dataclass
        generated its own __repr__ instead of using SensitiveRepr's.
        """
        if type(self).__repr__ is not SensitiveRepr.__repr__:
            raise SensitiveDeclarationError(const.ERR_SENSITIVE_REPR_NOT_OVERRIDDEN)

    def __repr__(self) -> str:
        """
        Repr with sensitive fields masked.

        Reads field(metadata={"sensitivity": Sensitivity.X}) markers.
        Replaced marked values with ERR_SENSITIVE_MASKED_REPR token.
        Field metadata remains introspectable unchanged.
        """
        if not is_dataclass(self):
            return object.__repr__(self)

        parts = []
        for dataclass_field in fields(self):
            value = getattr(self, dataclass_field.name)
            metadata = dataclass_field.metadata or {}
            sensitivity = metadata.get(const.SENSITIVITY_KEY)

            if sensitivity is not None and isinstance(sensitivity, Sensitivity):
                display_value = const.ERR_SENSITIVE_MASKED_REPR
            else:
                display_value = repr(value)

            part = const.REPR_FIELD_TEMPLATE.format(name=dataclass_field.name, value=display_value)
            parts.append(part)

        class_name = type(self).__name__
        joined_parts = const.REPR_FIELD_SEPARATOR.join(parts)
        return const.REPR_TEMPLATE.format(class_name=class_name, fields=joined_parts)
