# Sensitivity Policies: removed in 0.6.0

> **Status:** removed in 0.6.0. `sensitive`, `SensitiveDecorator`, the `logging_suite.sensitivity.decorators` package and the policy classes (`PhiPolicyAware`, `PiiPolicyAware`, `PciPolicyAware`, `SecretPolicyAware`, `Compliance`) no longer exist and cannot be imported.
> **Replacement:** field metadata, the `SensitiveRepr` adoption mixin, and `classify()`.

## What was removed

The 0.6.0 release removed the decorator and policy surface of `logging_suite.sensitivity` (then `mixin_sensitivity`). See the 0.6.0 "Removed" section of `CHANGELOG.md`. Earlier versions of this page documented per-class policy objects with custom placeholders and detection hints. There is no per-policy placeholder and no name-based detection now: a field is sensitive only when its metadata says so, and the mask is always `***MASKED***`.

The sibling pages `sensitive.md` and `compliance.md` in this directory still describe the pre-0.6.0 decorator surface; read them as history.

## Replacement

Mark fields with metadata and inherit `SensitiveRepr`. The dataclass must pass `repr=False`:

```python
from dataclasses import dataclass, field

from logging_suite.sensitivity import SensitiveRepr, Sensitivity, classify


@dataclass(frozen=True, slots=True, repr=False)
class PatientRecord(SensitiveRepr):
    patient_id: str
    name: str = field(metadata={"sensitivity": Sensitivity.PHI})
    ssn: str = field(metadata={"sensitivity": Sensitivity.PHI})
    email: str = field(metadata={"sensitivity": Sensitivity.PII})


patient = PatientRecord(
    patient_id="P12345",
    name="Jane Doe",
    ssn="123-45-6789",
    email="jane@example.com",
)
print(repr(patient))

profile = classify(PatientRecord)
print(profile.fields_of(Sensitivity.PHI))
print(profile.sensitivity_of("email"))
print(profile.has(Sensitivity.PCI))
```

Output:

```
PatientRecord(patient_id='P12345', name=***MASKED***, ssn=***MASKED***, email=***MASKED***)
('name', 'ssn')
pii
False
```

The taxonomy is the `Sensitivity` enum: `PHI`, `PII`, `PCI`, `SECRET`.
