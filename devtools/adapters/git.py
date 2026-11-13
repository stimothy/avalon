"""The adapter of devtools for git. It lists tracked and changed files and nothing else."""

from __future__ import annotations

from typing import Protocol

from devtools.adapters.process import ProcessPort


class GitError(RuntimeError):
    """Raised when git fails."""


class GitPort(Protocol):
    def tracked_files(self) -> list[str]: ...

    def changed_files(self, base: str) -> list[str]: ...


class RealGit:
    """Reads the files of the repo at a root folder."""

    def __init__(self, process: ProcessPort, root: str) -> None:
        self._process = process
        self._root = root

    def _names(self, args: list[str], failure: str) -> list[str]:
        done = self._process.run(args, cwd=self._root)
        if done.returncode != 0:
            raise GitError(done.stderr.strip() or failure)
        return [name for name in done.stdout.split("\0") if name]

    def tracked_files(self) -> list[str]:
        return self._names(["git", "ls-files", "-z"], "git ls-files failed")

    def changed_files(self, base: str) -> list[str]:
        """List the paths changed since the merge base with `base`."""
        return self._names(
            ["git", "diff", "--name-only", "-z", f"{base}...HEAD"], "git diff failed"
        )
