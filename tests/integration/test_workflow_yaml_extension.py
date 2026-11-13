from __future__ import annotations

from pathlib import Path

from devtools.gates import __main__ as gates_main


def test_the_workflows_command_reads_yaml_files_too(tmp_path: Path) -> None:
    folder = tmp_path / ".github" / "workflows"
    folder.mkdir(parents=True)
    (folder / "unsafe.yaml").write_text("on:\n  pull_request_target:\n", encoding="utf-8")

    code = gates_main.run(["workflows"], tmp_path)

    assert code == 1
