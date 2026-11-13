"""The adapter of devtools for git. It lists tracked and changed files and nothing else."""

from __future__ import annotations

from typing import Protocol

from devtools.adapters.process import ProcessPort


class GitError(RuntimeError):
    """Raised when git fails."""


class GitPort(Protocol):
    def tracked_files(self) -> list[str]: ...

    def changed_files(self, base: str) -> list[str]: ...

    def tags(self) -> list[str]: ...

    def commit_of(self, tag: str) -> str: ...

    def newest_commit(self, ref: str) -> str: ...

    def commits_after(self, commit: str, ref: str) -> list[str]: ...


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

    def _lines(self, args: list[str], failure: str) -> list[str]:
        done = self._process.run(args, cwd=self._root)
        if done.returncode != 0:
            raise GitError(done.stderr.strip() or failure)
        return [line for line in done.stdout.splitlines() if line]

    def tags(self) -> list[str]:
        return self._lines(["git", "tag", "--list"], "git tag failed")

    def commit_of(self, tag: str) -> str:
        """The commit a tag points at, through an annotated tag if there is one."""
        return self._lines(["git", "rev-list", "-n", "1", tag], "git rev-list failed")[0]

    def newest_commit(self, ref: str) -> str:
        return self._lines(["git", "rev-parse", ref], "git rev-parse failed")[0]

    def commits_after(self, commit: str, ref: str) -> list[str]:
        """The commits on the first-parent line after `commit` up to `ref`, oldest first."""
        return self._lines(
            ["git", "rev-list", "--reverse", "--first-parent", f"{commit}..{ref}"],
            "git rev-list failed",
        )
