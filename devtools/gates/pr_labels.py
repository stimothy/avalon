"""The label check of a pull request: exactly one version label, and `major` only when allowed."""

from __future__ import annotations

from devtools.adapters.gh import GhPort
from devtools.adapters.git import GitPort
from devtools.release import policy, version


def check(git: GitPort, gh: GhPort, number: int) -> list[str]:
    """Return one line for each rule the pull request's labels break; empty means it passes."""
    labels = gh.pull_request(number).labels
    label = version.pick_label(labels)
    if label is None:
        carried = ", ".join(labels) or "no labels"
        return [
            f"pull request #{number} must carry exactly one of "
            f"{', '.join(version.ALL_LABELS)}; it carries: {carried}"
        ]
    allowed = policy.major_allowed(gh.variable(policy.ALLOW_MAJOR_VARIABLE))
    refusal = policy.major_refusal(version.latest(git.tags()), label, allowed)
    return [f"pull request #{number}: {refusal}"] if refusal else []
