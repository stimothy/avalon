"""The verdict: the final job passes only when every other job did its part."""

from __future__ import annotations

from typing import Any


def judge(needs: dict[str, Any], gated: dict[str, str], filter_job: str) -> list[str]:
    """Return one line for each job that spoils the verdict; empty means a pass.

    `needs` is the `needs` context of the final job. `gated` maps a job to the filter
    output that says whether it applies. A job may be skipped only when its output is false.
    """
    filter_outputs: dict[str, str] = needs.get(filter_job, {}).get("outputs", {})
    problems = []
    for job, info in sorted(needs.items()):
        result = info.get("result")
        if result == "success":
            continue
        output = gated.get(job)
        if result == "skipped" and output is not None and filter_outputs.get(output) == "false":
            continue
        problems.append(f"{job}: {result}")
    return problems
