from __future__ import annotations

import pytest

from devtools.release import version
from devtools.release.version import Version


def test_the_latest_is_the_highest_tag_compared_as_numbers() -> None:
    latest = version.latest(["v0.9.0", "v0.10.0", "v0.2.0"])

    assert latest == Version(0, 10, 0)


def test_a_tag_of_another_form_is_ignored() -> None:
    latest = version.latest(["v1.0.0", "v2.0", "2.0.0", "v3.0.0-rc1", "v01.0.0", "latest"])

    assert latest == Version(1, 0, 0)


def test_no_tag_of_the_form_gives_no_version() -> None:
    latest = version.latest(["nightly", "v1"])

    assert latest is None


@pytest.mark.parametrize(
    ("label", "expected"),
    [("major", "v2.0.0"), ("minor", "v1.3.0"), ("patch", "v1.2.4")],
)
def test_a_label_raises_its_part_and_zeroes_the_rest(label: str, expected: str) -> None:
    bumped = version.bump(Version(1, 2, 3), label)

    assert bumped.tag() == expected


@pytest.mark.parametrize(
    ("label", "expected"),
    [("major", "v1.0.0"), ("minor", "v0.1.0"), ("patch", "v0.0.1")],
)
def test_with_no_version_the_count_starts_from_zero(label: str, expected: str) -> None:
    bumped = version.bump(None, label)

    assert bumped.tag() == expected


def test_a_word_that_is_not_a_version_label_is_refused() -> None:
    with pytest.raises(ValueError, match="none"):
        version.bump(Version(1, 0, 0), "none")


def test_one_release_label_among_others_is_picked() -> None:
    label = version.pick_label(["bug", "minor", "dependencies"])

    assert label == "minor"


@pytest.mark.parametrize("labels", [[], ["bug"], ["major", "patch"], ["none", "minor"]])
def test_anything_but_exactly_one_release_label_picks_nothing(labels: list[str]) -> None:
    label = version.pick_label(labels)

    assert label is None
