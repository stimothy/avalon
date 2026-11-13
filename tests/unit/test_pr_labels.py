from __future__ import annotations

from devtools.adapters.gh import PullRequest
from devtools.gates import pr_labels
from fakes.gate_fakes import FakeGh, FakeGit


def _check(labels: list[str], tags: dict[str, str], variables: dict[str, str]) -> list[str]:
    git = FakeGit([], history=["c1"], tags=tags)
    gh = FakeGh(pulls={5: PullRequest(5, labels)}, variables=variables)

    return pr_labels.check(git, gh, 5)


def test_one_version_label_passes() -> None:
    problems = _check(["minor", "docs"], {}, {})

    assert problems == []


def test_no_version_label_fails_and_names_the_pull_request() -> None:
    problems = _check(["docs"], {}, {})

    assert len(problems) == 1 and "#5" in problems[0] and "docs" in problems[0]


def test_two_version_labels_fail() -> None:
    problems = _check(["minor", "patch"], {}, {})

    assert len(problems) == 1


def test_major_is_refused_with_no_version() -> None:
    problems = _check(["major"], {}, {})

    assert len(problems) == 1 and "ALLOW_PRE_1_MAJOR" in problems[0]


def test_major_is_refused_below_one() -> None:
    problems = _check(["major"], {"v0.4.0": "c1"}, {})

    assert len(problems) == 1


def test_major_passes_when_the_owner_allows_it() -> None:
    problems = _check(["major"], {}, {"ALLOW_PRE_1_MAJOR": "true"})

    assert problems == []


def test_major_passes_from_one_up() -> None:
    problems = _check(["major"], {"v1.0.0": "c1"}, {})

    assert problems == []
