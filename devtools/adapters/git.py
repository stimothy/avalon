"""The adapter of devtools for git. It lists tracked files and nothing else."""

from __future__ import annotations

from typing import Protocol

from devtools.adapters.process import ProcessPort


class GitError(RuntimeError):
    """Raised when git fails."""


class GitPort(Protocol):
    def tracked_files(self) -> list[str]: ...


class RealGit:
    """Reads the tracked files of the repo at a root folder."""

    def __init__(self, process: ProcessPort, root: str) -> None:
        self._process = process
        self._root = root

    def tracked_files(self) -> list[str]:
        done = self._process.run(["git", "ls-files", "-z"], cwd=self._root)
        if done.returncode != 0:
            raise GitError(done.stderr.strip() or "git ls-files failed")
        return [name for name in done.stdout.split("\0") if name]
