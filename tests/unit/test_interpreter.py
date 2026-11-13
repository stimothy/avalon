from __future__ import annotations

from devtools.gates import interpreter


def test_the_expected_version_passes() -> None:
    problems = interpreter.check("3.9", (3, 9, 6))

    assert problems == []


def test_another_version_fails_and_names_both() -> None:
    problems = interpreter.check("3.9", (3, 14, 0))

    assert problems == ["the interpreter reports 3.14, not 3.9"]
