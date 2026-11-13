"""The git fake and the real git adapter answer the same cases, in a throwaway repo."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from devtools.adapters.git import GitPort, RealGit
from devtools.adapters.process import RealProcess
from fakes.gate_fakes import FakeGit

GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@example.com"]


def _git(root: Path, *args: str) -> str:
    done = subprocess.run([*GIT, *args], cwd=root, check=True, capture_output=True, text=True)
    return done.stdout.strip()


def _repo(root: Path) -> list[str]:
    """Three commits, an annotated tag on the first, a lightweight one on the second."""
    _git(root, "init", "-q")
    commits = []
    for name in ("a", "b", "c"):
        (root / name).write_text(name, encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", name)
        commits.append(_git(root, "rev-parse", "HEAD"))
    _git(root, "tag", "-a", "v0.1.0", "-m", "first", commits[0])
    _git(root, "tag", "nightly", commits[1])
    return commits


def _both(root: Path) -> dict[str, GitPort]:
    commits = _repo(root)
    fake = FakeGit([], history=commits, tags={"v0.1.0": commits[0], "nightly": commits[1]})
    return {"fake": fake, "real": RealGit(RealProcess(), str(root))}


@pytest.fixture(params=["fake", "real"])
def adapter(request: pytest.FixtureRequest, tmp_path: Path) -> GitPort:
    return _both(tmp_path)[request.param]


def test_tags_lists_every_tag(adapter: GitPort) -> None:
    tags = adapter.tags()

    assert sorted(tags) == ["nightly", "v0.1.0"]


def test_commit_of_an_annotated_tag_is_the_commit_not_the_tag_object(adapter: GitPort) -> None:
    first = adapter.commits_after(adapter.commit_of("v0.1.0"), "HEAD")

    assert len(first) == 2


def test_commits_after_a_commit_come_oldest_first(adapter: GitPort) -> None:
    after = adapter.commits_after(adapter.commit_of("v0.1.0"), "HEAD")

    assert after[0] == adapter.commit_of("nightly")


def test_the_newest_commit_ends_the_walk(adapter: GitPort) -> None:
    after = adapter.commits_after(adapter.commit_of("v0.1.0"), "HEAD")

    assert after[-1] == adapter.newest_commit("HEAD")
