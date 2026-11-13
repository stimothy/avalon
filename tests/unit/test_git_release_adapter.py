from __future__ import annotations

import pytest

from devtools.adapters.git import GitError, RealGit
from devtools.adapters.process import Completed
from fakes.gate_fakes import FakeProcess


def test_tags_lists_one_per_line() -> None:
    process = FakeProcess(default=Completed(0, "v0.1.0\nnightly\n", ""))

    tags = RealGit(process, "/repo").tags()

    assert tags == ["v0.1.0", "nightly"]


def test_commit_of_asks_for_the_one_commit_the_tag_names() -> None:
    process = FakeProcess(default=Completed(0, "abc\n", ""))

    RealGit(process, "/repo").commit_of("v0.1.0")

    assert process.calls == [["git", "rev-list", "-n", "1", "v0.1.0"]]


def test_commits_after_walks_the_first_parent_line_oldest_first() -> None:
    process = FakeProcess(default=Completed(0, "b\nc\n", ""))

    commits = RealGit(process, "/repo").commits_after("a", "HEAD")

    assert commits == ["b", "c"]
    assert process.calls == [["git", "rev-list", "--reverse", "--first-parent", "a..HEAD"]]


def test_newest_commit_resolves_the_ref() -> None:
    process = FakeProcess(default=Completed(0, "abc\n", ""))

    newest = RealGit(process, "/repo").newest_commit("HEAD")

    assert newest == "abc"


def test_a_failure_of_git_is_raised() -> None:
    process = FakeProcess(default=Completed(128, "", "not a repo\n"))

    with pytest.raises(GitError, match="not a repo"):
        RealGit(process, "/repo").tags()
