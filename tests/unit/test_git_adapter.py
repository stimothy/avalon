from __future__ import annotations

import pytest

from devtools.adapters.git import GitError, RealGit
from devtools.adapters.process import Completed
from fakes.gate_fakes import FakeProcess


def test_tracked_files_splits_the_nul_separated_list() -> None:
    process = FakeProcess(default=Completed(0, "a.md\0dir/b.md\0", ""))

    files = RealGit(process, "/repo").tracked_files()

    assert files == ["a.md", "dir/b.md"]


def test_changed_files_diffs_against_the_merge_base() -> None:
    process = FakeProcess(default=Completed(0, "a.md\0", ""))

    files = RealGit(process, "/repo").changed_files("origin/master")

    assert files == ["a.md"]
    assert process.calls == [["git", "diff", "--name-only", "-z", "origin/master...HEAD"]]


def test_changed_files_raises_when_git_fails() -> None:
    process = FakeProcess(default=Completed(128, "", "bad ref\n"))

    with pytest.raises(GitError, match="bad ref"):
        RealGit(process, "/repo").changed_files("nope")


def test_tracked_files_raises_when_git_fails() -> None:
    process = FakeProcess(default=Completed(128, "", "not a repo\n"))

    with pytest.raises(GitError, match="not a repo"):
        RealGit(process, "/repo").tracked_files()
