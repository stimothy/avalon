from __future__ import annotations

import pytest

from devtools.adapters.gh import GhError, PullRequest
from devtools.release import __main__ as release_main
from fakes.gate_fakes import FakeGh, FakeGit


class _BrokenGit(FakeGit):
    def tags(self) -> list[str]:
        raise GhError("no auth")


def test_release_prints_each_version_it_made(capsys: pytest.CaptureFixture[str]) -> None:
    git = FakeGit([], history=["c1", "c2"], tags={"v0.1.0": "c1"})
    gh = FakeGh(merged={"c2": [PullRequest(2, ["patch"])]})

    code = release_main.run(["release"], git, gh)

    assert (code, capsys.readouterr().out) == (0, "v0.1.1 at c2\n")


def test_dry_run_prints_the_version(capsys: pytest.CaptureFixture[str]) -> None:
    git = FakeGit([], history=["c1"], tags={"v0.1.0": "c1"})
    gh = FakeGh(pulls={3: PullRequest(3, ["minor"])})

    code = release_main.run(["dry-run", "--pr", "3"], git, gh)

    assert (code, capsys.readouterr().out) == (0, "pull request #3 would make v0.2.0\n")


def test_a_stop_exits_one_and_names_the_pull_request(
    capsys: pytest.CaptureFixture[str],
) -> None:
    git = FakeGit([], history=["c1", "c2"], tags={"v0.1.0": "c1"})
    gh = FakeGh(merged={"c2": [PullRequest(8, [])]})

    code = release_main.run(["release"], git, gh)

    assert code == 1
    assert "pull request #8" in capsys.readouterr().out


def test_an_adapter_failure_exits_two(capsys: pytest.CaptureFixture[str]) -> None:
    git = _BrokenGit([])

    code = release_main.run(["release"], git, FakeGh())

    assert (code, capsys.readouterr().err) == (2, "no auth\n")
