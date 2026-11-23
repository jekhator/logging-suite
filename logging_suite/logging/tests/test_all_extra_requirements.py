"""The all extra lists only real requirements of this project."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

PYPROJECT_PATH = Path(__file__).resolve().parents[3] / "pyproject.toml"
ALL_EXTRA = "all"
BARE_OWN_EXTRA_NAMES = ("ses", "sns")
REQUIRED_ALL_ENTRY = "boto3>=1.28.0"
REQUIREMENT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")
NAME_SEPARATOR_PATTERN = re.compile(r"[-_.]+")


def normalized(requirement: str) -> str:
    """Return the requirement without whitespace, lower-cased."""
    return "".join(requirement.split()).lower()


def distribution_name(requirement: str) -> str:
    """Return the normalized distribution name a requirement string installs."""
    match = REQUIREMENT_NAME_PATTERN.match(requirement.strip())
    assert match is not None, requirement
    return NAME_SEPARATOR_PATTERN.sub("-", match.group(0)).lower()


def read_project(pyproject_path: Path) -> dict[str, object]:
    """Return the [project] table of a pyproject.toml file."""
    with pyproject_path.open("rb") as handle:
        project: dict[str, object] = tomllib.load(handle)["project"]
    return project


def all_extra_entries(pyproject_path: Path) -> list[str]:
    """Return the entries of the all extra, normalized, in file order."""
    extras = read_project(pyproject_path)["optional-dependencies"]
    assert isinstance(extras, dict)
    return [normalized(entry) for entry in extras[ALL_EXTRA]]


def real_requirements(pyproject_path: Path) -> set[str]:
    """Return every requirement of the other extras and of the base install."""
    project = read_project(pyproject_path)
    extras = project["optional-dependencies"]
    assert isinstance(extras, dict)
    dependencies = project.get("dependencies", [])
    assert isinstance(dependencies, list)
    found = {normalized(entry) for entry in dependencies}
    for extra_name, entries in extras.items():
        if extra_name != ALL_EXTRA:
            found.update(normalized(entry) for entry in entries)
    return found


def unknown_all_entries(pyproject_path: Path) -> list[str]:
    """Return the all entries that no other extra and no dependency requires."""
    known = real_requirements(pyproject_path)
    return [entry for entry in all_extra_entries(pyproject_path) if entry not in known]


def write_copy_with_bare_extra_name(directory: Path) -> Path:
    """Write a pyproject.toml copy with the bare name sns put back into all."""
    original = PYPROJECT_PATH.read_text()
    anchor = f'    "{REQUIRED_ALL_ENTRY}",\n'
    assert original.count(anchor) == 1
    copy_path = directory / "pyproject.toml"
    copy_path.write_text(original.replace(anchor, anchor + '    "sns",\n'))
    return copy_path


class TestAllExtraRequirements:
    """Guard the all extra against names that are not this project's requirements."""

    def test_every_all_entry_is_a_real_requirement(self) -> None:
        """Each all entry is required by another extra or by the base install."""
        assert unknown_all_entries(PYPROJECT_PATH) == []

    def test_all_covers_every_other_extra(self) -> None:
        """The all extra installs everything the other extras install."""
        missing = real_requirements(PYPROJECT_PATH) - set(all_extra_entries(PYPROJECT_PATH))
        assert missing == set()

    def test_all_entries_are_deduplicated(self) -> None:
        """No requirement appears twice in the all extra."""
        entries = all_extra_entries(PYPROJECT_PATH)
        assert len(entries) == len(set(entries))

    def test_all_installs_boto3_and_no_bare_extra_name(self) -> None:
        """The ses and sns extras reach all as boto3, never as their own names."""
        entries = all_extra_entries(PYPROJECT_PATH)
        installed = {distribution_name(entry) for entry in entries}
        assert REQUIRED_ALL_ENTRY in entries
        assert installed.isdisjoint(BARE_OWN_EXTRA_NAMES)

    def test_bare_extra_name_is_rejected(self, tmp_path: Path) -> None:
        """Negative control: putting sns back into all is reported."""
        copy_path = write_copy_with_bare_extra_name(tmp_path)
        assert unknown_all_entries(copy_path) == ["sns"]
