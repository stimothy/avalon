from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from devtools.adapters.git import RealGit
from devtools.adapters.process import RealProcess
from devtools.gates import __main__ as gates_main

PLAN_ID = "F" + "R-" + "9"


def _repo(root: Path, files: dict[str, str]) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    for name, text in files.items():
        (root / name).write_text(text, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)


def test_real_git_lists_the_tracked_files_only(tmp_path: Path) -> None:
    _repo(tmp_path, {"a.md": "x"})
    (tmp_path / "untracked.md").write_text("y", encoding="utf-8")

    files = RealGit(RealProcess(), str(tmp_path)).tracked_files()

    assert files == ["a.md"]


def test_real_process_runs_a_command_and_finds_a_tool() -> None:
    process = RealProcess()

    done = process.run(["git", "--version"])

    assert done.returncode == 0
    assert process.which("git") is not None


def test_the_tracked_command_fails_and_names_the_file_and_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _repo(tmp_path, {"a.md": f"ok\n{PLAN_ID}\n", "b.md": "ok"})

    code = gates_main.run(["tracked"], tmp_path)

    assert code == 1
    assert "a.md:2:" in capsys.readouterr().out


def test_the_tracked_command_skips_a_binary_file(tmp_path: Path) -> None:
    _repo(tmp_path, {"a.md": "ok"})
    (tmp_path / "bin.dat").write_bytes(b"\xff\xfe\x00")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)

    code = gates_main.run(["tracked"], tmp_path)

    assert code == 0


def test_the_pull_request_command_fails_on_a_plan_citation(tmp_path: Path) -> None:
    code = gates_main.run(["pull-request", "--title", f"Fix {PLAN_ID}", "--body", "b"], tmp_path)

    assert code == 1


def test_the_pull_request_command_passes_a_clean_pull_request(tmp_path: Path) -> None:
    code = gates_main.run(["pull-request", "--title", "Add a gate", "--body", "b"], tmp_path)

    assert code == 0


def test_the_secrets_command_exits_with_two_when_gitleaks_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _repo(tmp_path, {"a.md": "ok"})
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))

    code = gates_main.run(["secrets"], tmp_path)

    assert code == 2
    assert "not installed" in capsys.readouterr().err
