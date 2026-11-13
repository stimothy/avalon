from __future__ import annotations

import pytest

from devtools.adapters.process import Completed
from devtools.gates import secret_scan
from fakes.gate_fakes import FakeGit, FakeProcess


def test_the_scan_runs_gitleaks_on_each_tracked_file() -> None:
    process = FakeProcess()

    secret_scan.scan_secrets(FakeGit(["a.md", "b.md"]), process, ".")

    assert [call[-1] for call in process.calls] == ["a.md", "b.md"]


def test_the_scan_passes_when_gitleaks_finds_nothing() -> None:
    problems = secret_scan.scan_secrets(FakeGit(["a.md"]), FakeProcess(), ".")

    assert problems == []


def test_the_scan_names_the_file_gitleaks_flags() -> None:
    process = FakeProcess(answers={"b.md": Completed(1, "leak", "")})

    problems = secret_scan.scan_secrets(FakeGit(["a.md", "b.md"]), process, ".")

    assert [p.split(":")[0] for p in problems] == ["b.md"]


def test_the_scan_fails_with_a_clear_message_when_gitleaks_is_missing() -> None:
    with pytest.raises(secret_scan.ToolMissingError, match="not installed"):
        secret_scan.scan_secrets(FakeGit(["a.md"]), FakeProcess(installed=False), ".")
