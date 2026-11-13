"""The secret scan: gitleaks run over each tracked file."""

from __future__ import annotations

from devtools.adapters.git import GitPort
from devtools.adapters.process import ProcessPort

TOOL = "gitleaks"
MISSING_MESSAGE = (
    "gitleaks is not installed, so the secret scan cannot run. "
    "Install the version that the project states, then run the scan again."
)


class ToolMissingError(RuntimeError):
    """Raised when gitleaks cannot be found."""


def scan_secrets(git: GitPort, process: ProcessPort, root: str) -> list[str]:
    """Return one message for each tracked file in which gitleaks found a secret."""
    if process.which(TOOL) is None:
        raise ToolMissingError(MISSING_MESSAGE)
    problems: list[str] = []
    for path in git.tracked_files():
        done = process.run(
            [TOOL, "detect", "--no-git", "--no-banner", "--redact", "--source", path],
            cwd=root,
        )
        if done.returncode != 0:
            detail = (done.stdout + done.stderr).strip()
            problems.append(f"{path}: gitleaks reported a finding or an error\n{detail}")
    return problems
