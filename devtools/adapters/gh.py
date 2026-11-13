"""The one adapter of devtools that runs `gh`. Tests replace it with a fake."""

from __future__ import annotations

from typing import Protocol

from devtools.adapters.process import ProcessPort


class GhError(RuntimeError):
    """Raised when `gh` fails."""


class GhPort(Protocol):
    def changed_files(self, pull_request: int) -> list[str]: ...


class RealGh:
    """Reads facts about a pull request through the `gh` command."""

    def __init__(self, process: ProcessPort, root: str) -> None:
        self._process = process
        self._root = root

    def changed_files(self, pull_request: int) -> list[str]:
        args = ["gh", "pr", "diff", str(pull_request), "--name-only"]
        done = self._process.run(args, cwd=self._root)
        if done.returncode != 0:
            raise GhError(done.stderr.strip() or "gh pr diff failed")
        return [line for line in done.stdout.splitlines() if line]
