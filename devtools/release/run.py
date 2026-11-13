"""The release walk and its dry run. Both reach git and GitHub only through ports."""

from __future__ import annotations

from dataclasses import dataclass

from devtools.adapters.gh import GhPort
from devtools.adapters.git import GitPort
from devtools.release import policy, version

NOTES = (
    "## On upgrade\n\n"
    "What a user must do in a target repo on upgrade: nothing is recorded for this release.\n\n"
    "## Changes\n"
)


class ReleaseStopError(Exception):
    """A commit the run cannot pass; the run releases nothing at or after it."""


@dataclass(frozen=True)
class Made:
    tag: str
    commit: str


def _one_label(number: int, labels: list[str]) -> str:
    label = version.pick_label(labels)
    if label is None:
        raise ReleaseStopError(
            f"pull request #{number} must carry exactly one of "
            f"{', '.join(version.ALL_LABELS)}; it carries: {', '.join(labels) or 'none of them'}"
        )
    return label


def _commits(git: GitPort, ref: str, latest: version.Version | None) -> list[str]:
    if latest is None:
        return [git.newest_commit(ref)]
    return git.commits_after(git.commit_of(latest.tag()), ref)


def release(git: GitPort, gh: GhPort, ref: str) -> list[Made]:
    """Release every commit newer than the latest version, oldest first."""
    latest = version.latest(git.tags())
    allowed = policy.major_allowed(gh.variable(policy.ALLOW_MAJOR_VARIABLE))
    made: list[Made] = []
    if latest is not None and not gh.release_exists(latest.tag()):
        # The tag exists without its release: publish it on its own commit, tag untouched.
        commit = git.commit_of(latest.tag())
        gh.create_release(latest.tag(), commit, NOTES)
        made.append(Made(latest.tag(), commit))
    for commit in _commits(git, ref, latest):
        pulls = gh.merged_pull_requests(commit)
        if not pulls:
            continue
        if len(pulls) > 1:
            numbers = ", ".join(f"#{pull.number}" for pull in pulls)
            raise ReleaseStopError(
                f"commit {commit} has more than one merged pull request: {numbers}"
            )
        pull = pulls[0]
        label = _one_label(pull.number, pull.labels)
        if label == "none":
            continue
        refusal = policy.major_refusal(latest, label, allowed)
        if refusal is not None:
            raise ReleaseStopError(f"pull request #{pull.number}: {refusal}")
        latest = version.bump(latest, label)
        if not gh.release_exists(latest.tag()):
            gh.create_release(latest.tag(), commit, NOTES)
            made.append(Made(latest.tag(), commit))
    return made


def dry_run(git: GitPort, gh: GhPort, number: int) -> str:
    """Say what version a pull request would get, or why it is refused. Creates nothing."""
    pull = gh.pull_request(number)
    label = _one_label(number, pull.labels)
    if label == "none":
        return f"pull request #{number} is labelled none and makes no version"
    latest = version.latest(git.tags())
    allowed = policy.major_allowed(gh.variable(policy.ALLOW_MAJOR_VARIABLE))
    refusal = policy.major_refusal(latest, label, allowed)
    if refusal is not None:
        raise ReleaseStopError(f"pull request #{number}: {refusal}")
    return f"pull request #{number} would make {version.bump(latest, label).tag()}"
