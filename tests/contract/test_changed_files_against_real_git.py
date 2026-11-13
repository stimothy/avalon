from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from devtools.adapters.git import RealGit
from devtools.adapters.process import RealProcess
from devtools.gates import __main__ as gates_main

GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@example.com"]


def _commit(root: Path, name: str) -> None:
    (root / name).write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run([*GIT, "commit", "-q", "-m", name], cwd=root, check=True)


def _repo_with_a_change(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    _commit(root, "a.md")
    subprocess.run(["git", "branch", "base"], cwd=root, check=True)
    _commit(root, "b.md")


def test_real_git_lists_the_paths_changed_since_a_base(tmp_path: Path) -> None:
    _repo_with_a_change(tmp_path)

    files = RealGit(RealProcess(), str(tmp_path)).changed_files("base")

    assert files == ["b.md"]


def test_the_changed_paths_command_prints_one_output_per_gate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _repo_with_a_change(tmp_path)

    code = gates_main.run(["changed-paths", "--base", "base"], tmp_path)

    assert (code, capsys.readouterr().out) == (0, "docs=true\nplugin=false\n")
