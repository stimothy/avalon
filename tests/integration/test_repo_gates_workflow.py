from __future__ import annotations

import re
from pathlib import Path

from devtools.gates import workflow_check

ROOT = Path(__file__).resolve().parents[2]
TEXT = (ROOT / ".github" / "workflows" / "gates.yml").read_text(encoding="utf-8")


def test_the_gates_workflow_passes_the_workflow_check() -> None:
    problems = workflow_check.check("gates.yml", TEXT)

    assert problems == []


def test_the_gates_workflow_runs_only_on_a_pull_request_into_master() -> None:
    top = TEXT.split("\njobs:")[0]

    assert re.search(r"on:\n  pull_request:\n    branches: \[master\]", top)
    assert "push:" not in top


def test_the_last_job_is_the_all_green_verdict() -> None:
    jobs = re.findall(r"^  ([\w-]+):\n", TEXT.split("\njobs:")[1], re.MULTILINE)

    assert jobs[-1] == "all-green"
