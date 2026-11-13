from __future__ import annotations

import pytest

from devtools.release import policy
from devtools.release.version import Version


def test_major_is_refused_when_no_version_exists() -> None:
    refusal = policy.major_refusal(None, "major", False)

    assert refusal is not None
    assert policy.ALLOW_MAJOR_VARIABLE in refusal


def test_major_is_refused_below_one() -> None:
    refusal = policy.major_refusal(Version(0, 9, 9), "major", False)

    assert refusal is not None


def test_the_owners_variable_allows_major_below_one() -> None:
    refusal = policy.major_refusal(Version(0, 9, 9), "major", True)

    assert refusal is None


def test_major_goes_ahead_from_one_on() -> None:
    refusal = policy.major_refusal(Version(1, 0, 0), "major", False)

    assert refusal is None


@pytest.mark.parametrize("label", ["minor", "patch"])
def test_the_other_labels_are_never_refused(label: str) -> None:
    refusal = policy.major_refusal(None, label, False)

    assert refusal is None


@pytest.mark.parametrize(("value", "expected"), [("true", True), (" TRUE\n", True), ("yes", False)])
def test_only_the_text_true_allows_major(value: str, expected: bool) -> None:
    allowed = policy.major_allowed(value)

    assert allowed is expected


def test_an_unset_variable_does_not_allow_major() -> None:
    allowed = policy.major_allowed(None)

    assert allowed is False
