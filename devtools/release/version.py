"""Versions, the tags that name them, and the labels that raise them. All pure."""

from __future__ import annotations

import re
from dataclasses import dataclass

VERSION_LABELS = ("major", "minor", "patch")
ALL_LABELS = (*VERSION_LABELS, "none")
_TAG = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int

    def tag(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"


def parse_tag(tag: str) -> Version | None:
    """Read a tag of exactly the form `vMAJOR.MINOR.PATCH`; any other form gives None."""
    found = _TAG.fullmatch(tag)
    if found is None:
        return None
    return Version(int(found.group(1)), int(found.group(2)), int(found.group(3)))


def latest(tags: list[str]) -> Version | None:
    """The highest version among the tags, compared as numbers."""
    versions = [version for version in map(parse_tag, tags) if version is not None]
    return max(versions) if versions else None


def bump(current: Version | None, label: str) -> Version:
    """Raise the part the label names and zero every part after it. No version counts as v0.0.0."""
    base = current or Version(0, 0, 0)
    if label == "major":
        return Version(base.major + 1, 0, 0)
    if label == "minor":
        return Version(base.major, base.minor + 1, 0)
    if label == "patch":
        return Version(base.major, base.minor, base.patch + 1)
    raise ValueError(f"not a version label: {label}")


def pick_label(labels: list[str]) -> str | None:
    """The one release label a pull request carries, or None if it is not exactly one."""
    named = [label for label in labels if label in ALL_LABELS]
    return named[0] if len(named) == 1 else None
