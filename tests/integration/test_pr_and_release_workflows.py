from __future__ import annotations

import re
from pathlib import Path

import pytest

from devtools.gates import workflow_check

ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / ".github" / "workflows"


def _text(name: str) -> str:
    return (FOLDER / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("name", ["pr.yml", "release.yml"])
def test_the_workflow_passes_the_workflow_check(name: str) -> None:
    problems = workflow_check.check(name, _text(name))

    assert problems == []


def test_pr_runs_on_each_event_that_changes_what_it_checks() -> None:
    top = _text("pr.yml").split("\njobs:")[0]

    types = re.search(r"types: \[([^\]]*)\]", top)
    assert types is not None
    assert set(types.group(1).split(", ")) == {
        "opened",
        "reopened",
        "synchronize",
        "ready_for_review",
        "labeled",
        "unlabeled",
        "edited",
    }
    assert "branches: [master]" in top


def test_pr_cancels_its_own_older_run_in_its_own_group() -> None:
    top = _text("pr.yml").split("\njobs:")[0]

    assert "group: pr-${{ github.event.pull_request.number }}" in top
    assert "cancel-in-progress: true" in top
    assert "gates" not in top.split("concurrency:")[1]


def test_pr_runs_the_label_check_the_scan_and_the_dry_run() -> None:
    text = _text("pr.yml")

    for command in ("gates pr-labels", "gates pull-request", "release dry-run"):
        assert command in text


def test_release_runs_only_on_a_push_to_master_in_one_group_that_never_cancels() -> None:
    top = _text("release.yml").split("\njobs:")[0]

    assert re.search(r"on:\n  push:\n    branches: \[master\]\n", top)
    assert "pull_request" not in top
    assert "group: release\n" in top
    assert "cancel-in-progress: false" in top


def test_only_the_release_workflow_writes() -> None:
    writers = [
        path.name
        for path in sorted(FOLDER.glob("*.yml"))
        if re.search(r":\s*write\b", path.read_text(encoding="utf-8"))
    ]

    assert writers == ["release.yml"]


def test_no_other_workflow_runs_on_a_push() -> None:
    pushers = [
        path.name
        for path in sorted(FOLDER.glob("*.yml"))
        if re.search(r"^  push:", path.read_text(encoding="utf-8"), re.MULTILINE)
    ]

    assert pushers == ["release.yml"]
