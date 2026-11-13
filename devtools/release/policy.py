"""The refusal of `major` below 1.0.0, called by the release code and by the label check."""

from __future__ import annotations

from devtools.release.version import Version

ALLOW_MAJOR_VARIABLE = "ALLOW_PRE_1_MAJOR"


def major_allowed(value: str | None) -> bool:
    """Read the owner's repository variable: only the text `true` allows it."""
    return value is not None and value.strip().lower() == "true"


def major_refusal(latest: Version | None, label: str, allowed: bool) -> str | None:
    """Give the reason `major` is refused, or None when it may go ahead."""
    if label != "major" or allowed:
        return None
    if latest is not None and latest.major >= 1:
        return None
    return (
        "major is refused while no version exists or the latest is below v1.0.0, "
        f"unless the repository variable {ALLOW_MAJOR_VARIABLE} is true"
    )
