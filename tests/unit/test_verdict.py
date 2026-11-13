from __future__ import annotations

from typing import Any

from devtools.gates import verdict

GATED = {"plugin-check": "plugin"}


def _needs(plugin: str, plugin_result: str, other: str = "success") -> dict[str, Any]:
    return {
        "changes": {"result": "success", "outputs": {"plugin": plugin}},
        "plugin-check": {"result": plugin_result},
        "tests": {"result": other},
    }


def test_every_job_succeeding_passes() -> None:
    problems = verdict.judge(_needs("true", "success"), GATED, "changes")

    assert problems == []


def test_a_skip_the_filter_justified_passes() -> None:
    problems = verdict.judge(_needs("false", "skipped"), GATED, "changes")

    assert problems == []


def test_a_skip_when_the_gate_applies_fails() -> None:
    problems = verdict.judge(_needs("true", "skipped"), GATED, "changes")

    assert problems == ["plugin-check: skipped"]


def test_a_skip_of_an_ungated_job_fails() -> None:
    problems = verdict.judge(_needs("false", "success", other="skipped"), GATED, "changes")

    assert problems == ["tests: skipped"]


def test_a_failed_job_fails() -> None:
    problems = verdict.judge(_needs("true", "failure"), GATED, "changes")

    assert problems == ["plugin-check: failure"]


def test_a_cancelled_job_fails() -> None:
    problems = verdict.judge(_needs("true", "success", other="cancelled"), GATED, "changes")

    assert problems == ["tests: cancelled"]


def test_a_missing_filter_job_justifies_no_skip() -> None:
    needs = {"plugin-check": {"result": "skipped"}}

    problems = verdict.judge(needs, GATED, "changes")

    assert problems == ["plugin-check: skipped"]
