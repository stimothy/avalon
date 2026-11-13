"""The interpreter check: a job on a given Python fails when its interpreter is another."""

from __future__ import annotations


def check(expected: str, version: tuple[int, ...]) -> list[str]:
    """Return one line when the interpreter's `major.minor` is not `expected`."""
    actual = ".".join(str(part) for part in version[:2])
    if actual == expected:
        return []
    return [f"the interpreter reports {actual}, not {expected}"]
