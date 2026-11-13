from __future__ import annotations

from typing import Any

import pytest

from devtools.adapters.gh import PullRequest
from devtools.release import run
from fakes.gate_fakes import FakeGh, FakeGit


def _pull(number: int, *labels: str) -> list[PullRequest]:
    return [PullRequest(number, list(labels))]


def _gh(**kwargs: Any) -> FakeGh:
    kwargs.setdefault("releases", {"v0.1.0", "v1.4.2", "v0.3.1"})
    return FakeGh(**kwargs)


def _git(history: list[str], tags: dict[str, str] | None = None) -> FakeGit:
    return FakeGit([], history=history, tags=tags)


def test_commits_after_the_latest_version_are_released_oldest_first() -> None:
    git = _git(["c1", "c2", "c3"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": _pull(2, "patch"), "c3": _pull(3, "minor")})

    made = run.release(git, gh, "HEAD")

    assert [(m.tag, m.commit) for m in made] == [("v0.1.1", "c2"), ("v0.2.0", "c3")]


def test_a_release_is_created_with_the_notes() -> None:
    git = _git(["c1", "c2"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": _pull(2, "patch")})

    run.release(git, gh, "HEAD")

    assert gh.created == [("v0.1.1", "c2", run.NOTES)]


def test_the_notes_hold_a_place_for_the_upgrade_steps() -> None:
    notes = run.NOTES

    assert "## On upgrade" in notes


def test_a_commit_labelled_none_makes_no_version_and_its_changes_ship_in_the_next() -> None:
    git = _git(["c1", "c2", "c3"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": _pull(2, "none"), "c3": _pull(3, "patch")})

    made = run.release(git, gh, "HEAD")

    assert [(m.tag, m.commit) for m in made] == [("v0.1.1", "c3")]


def test_a_commit_with_no_merged_pull_request_gets_no_release() -> None:
    git = _git(["c1", "c2", "c3"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c3": _pull(3, "patch")})

    made = run.release(git, gh, "HEAD")

    assert [m.commit for m in made] == ["c3"]


def test_a_second_run_over_the_same_commits_makes_nothing_twice() -> None:
    git = _git(["c1", "c2"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": _pull(2, "patch")}, releases={"v0.1.0", "v0.1.1"})

    made = run.release(git, gh, "HEAD")

    assert (made, gh.created) == ([], [])


def test_with_no_version_only_the_newest_commit_is_released() -> None:
    git = _git(["c1", "c2", "c3"])
    gh = _gh(merged={"c1": _pull(1, "patch"), "c3": _pull(3, "patch")})

    made = run.release(git, gh, "HEAD")

    assert [(m.tag, m.commit) for m in made] == [("v0.0.1", "c3")]


def test_a_tag_of_another_form_is_not_a_version() -> None:
    git = _git(["c1", "c2"], {"nightly": "c1"})
    gh = _gh(merged={"c2": _pull(2, "minor")}, releases=set())

    made = run.release(git, gh, "HEAD")

    assert [m.tag for m in made] == ["v0.1.0"]


@pytest.mark.parametrize("labels", [[], ["bug"], ["major", "patch"]])
def test_a_pull_request_without_exactly_one_label_stops_the_run_and_is_named(
    labels: list[str],
) -> None:
    git = _git(["c1", "c2"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": _pull(7, *labels)})

    with pytest.raises(run.ReleaseStopError, match="pull request #7"):
        run.release(git, gh, "HEAD")


def test_a_stop_releases_nothing_at_or_after_the_commit() -> None:
    git = _git(["c1", "c2", "c3"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": _pull(2), "c3": _pull(3, "patch")})

    with pytest.raises(run.ReleaseStopError):
        run.release(git, gh, "HEAD")

    assert gh.created == []


def test_a_commit_with_two_merged_pull_requests_stops_the_run() -> None:
    git = _git(["c1", "c2"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": [*_pull(4, "patch"), *_pull(5, "patch")]})

    with pytest.raises(run.ReleaseStopError, match="#4, #5"):
        run.release(git, gh, "HEAD")


def test_major_below_one_is_refused_and_names_the_pull_request() -> None:
    git = _git(["c1", "c2"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": _pull(9, "major")})

    with pytest.raises(run.ReleaseStopError, match="pull request #9: major is refused"):
        run.release(git, gh, "HEAD")


def test_the_owners_variable_lets_major_through() -> None:
    git = _git(["c1", "c2"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c2": _pull(9, "major")}, variables={"ALLOW_PRE_1_MAJOR": "true"})

    made = run.release(git, gh, "HEAD")

    assert [m.tag for m in made] == ["v1.0.0"]


def test_major_after_one_needs_no_variable() -> None:
    git = _git(["c1", "c2"], {"v1.4.2": "c1"})
    gh = _gh(merged={"c2": _pull(9, "major")})

    made = run.release(git, gh, "HEAD")

    assert [m.tag for m in made] == ["v2.0.0"]


def test_the_dry_run_prints_the_version_a_pull_request_would_get() -> None:
    git = _git(["c1"], {"v0.3.1": "c1"})
    gh = _gh(pulls={5: PullRequest(5, ["minor"])})

    line = run.dry_run(git, gh, 5)

    assert line == "pull request #5 would make v0.4.0"


def test_the_dry_run_creates_nothing() -> None:
    git = _git(["c1"], {"v0.3.1": "c1"})
    gh = _gh(pulls={5: PullRequest(5, ["minor"])})

    run.dry_run(git, gh, 5)

    assert gh.created == []


def test_the_dry_run_of_a_none_pull_request_says_it_makes_no_version() -> None:
    git = _git(["c1"])
    gh = _gh(pulls={5: PullRequest(5, ["none"])})

    line = run.dry_run(git, gh, 5)

    assert "makes no version" in line


def test_the_dry_run_prints_the_refusal() -> None:
    git = _git(["c1"])
    gh = _gh(pulls={5: PullRequest(5, ["major"])})

    with pytest.raises(run.ReleaseStopError, match="pull request #5: major is refused"):
        run.dry_run(git, gh, 5)


def test_the_dry_run_names_a_pull_request_with_the_wrong_labels() -> None:
    git = _git(["c1"])
    gh = _gh(pulls={5: PullRequest(5, [])})

    with pytest.raises(run.ReleaseStopError, match="pull request #5 must carry exactly one"):
        run.dry_run(git, gh, 5)


def test_a_latest_tag_with_no_release_gets_its_release_on_its_own_commit() -> None:
    git = _git(["c1", "c2"], {"v0.1.0": "c1", "v0.1.1": "c2"})
    gh = _gh(releases={"v0.1.0"})

    made = run.release(git, gh, "HEAD")

    assert [(m.tag, m.commit) for m in made] == [("v0.1.1", "c2")]


def test_the_recovered_release_is_the_next_versions_base() -> None:
    git = _git(["c1", "c2", "c3"], {"v0.1.0": "c1"})
    gh = _gh(merged={"c3": _pull(3, "patch")}, releases=set())

    made = run.release(git, gh, "HEAD")

    assert [(m.tag, m.commit) for m in made] == [("v0.1.0", "c1"), ("v0.1.1", "c3")]
