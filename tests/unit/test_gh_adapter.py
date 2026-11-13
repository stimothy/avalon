from __future__ import annotations

import pytest

from devtools.adapters.gh import GhError, RealGh
from devtools.adapters.process import Completed
from fakes.gate_fakes import FakeProcess


def test_changed_files_splits_the_lines() -> None:
    process = FakeProcess(default=Completed(0, "a.md\ndir/b.py\n", ""))

    files = RealGh(process, "/repo").changed_files(7)

    assert files == ["a.md", "dir/b.py"]


def test_changed_files_asks_gh_for_the_pull_request() -> None:
    process = FakeProcess()

    RealGh(process, "/repo").changed_files(7)

    assert process.calls == [["gh", "pr", "diff", "7", "--name-only"]]


def test_changed_files_raises_when_gh_fails() -> None:
    process = FakeProcess(default=Completed(1, "", "no auth\n"))

    with pytest.raises(GhError, match="no auth"):
        RealGh(process, "/repo").changed_files(7)
