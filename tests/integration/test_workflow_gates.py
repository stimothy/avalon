from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools.gates import __main__ as gates_main

SHA = "a" * 40


def _write(root: Path, name: str, text: str) -> None:
    folder = root / ".github" / "workflows"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(text, encoding="utf-8")


def test_the_workflows_command_reports_a_bad_workflow(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write(tmp_path, "gates.yml", "jobs:\n  a:\n    steps:\n      - uses: x/y@v1\n")

    code = gates_main.run(["workflows"], tmp_path)

    assert code == 1
    assert "x/y@v1" in capsys.readouterr().out


def test_the_workflows_command_passes_a_clean_workflow(tmp_path: Path) -> None:
    text = f"permissions:\n  contents: read\njobs:\n  a:\n    steps:\n      - uses: x/y@{SHA}\n"
    _write(tmp_path, "gates.yml", text)

    code = gates_main.run(["workflows"], tmp_path)

    assert code == 0


def test_the_verdict_command_fails_on_a_failed_job(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    needs = json.dumps({"tests": {"result": "failure"}})

    code = gates_main.run(["verdict", "--needs", needs], tmp_path)

    assert (code, capsys.readouterr().out) == (1, "tests: failure\n")


def test_the_verdict_command_accepts_a_justified_skip(tmp_path: Path) -> None:
    needs = json.dumps(
        {
            "changes": {"result": "success", "outputs": {"plugin": "false"}},
            "plugin-check": {"result": "skipped"},
        }
    )

    code = gates_main.run(["verdict", "--needs", needs, "--gate", "plugin-check=plugin"], tmp_path)

    assert code == 0
