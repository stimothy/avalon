"""Fakes for the adapters that the gates and the release code call."""

from __future__ import annotations

from devtools.adapters.gh import PullRequest
from devtools.adapters.process import Completed


class FakeGit:
    """A linear history, oldest first, with tags that point into it."""

    def __init__(
        self,
        files: list[str],
        changed: list[str] | None = None,
        history: list[str] | None = None,
        tags: dict[str, str] | None = None,
    ) -> None:
        self._files = files
        self._changed = changed or []
        self._history = history or []
        self._tags = tags or {}

    def tracked_files(self) -> list[str]:
        return list(self._files)

    def changed_files(self, base: str) -> list[str]:
        return list(self._changed)

    def tags(self) -> list[str]:
        return list(self._tags)

    def commit_of(self, tag: str) -> str:
        return self._tags[tag]

    def newest_commit(self, ref: str) -> str:
        return self._history[-1]

    def commits_after(self, commit: str, ref: str) -> list[str]:
        return self._history[self._history.index(commit) + 1 :]


class FakeGh:
    def __init__(
        self,
        changed: list[str] | None = None,
        merged: dict[str, list[PullRequest]] | None = None,
        pulls: dict[int, PullRequest] | None = None,
        releases: set[str] | None = None,
        variables: dict[str, str] | None = None,
    ) -> None:
        self._changed = changed or []
        self._merged = merged or {}
        self._pulls = pulls or {}
        self.releases = releases or set()
        self._variables = variables or {}
        self.created: list[tuple[str, str, str]] = []

    def changed_files(self, pull_request: int) -> list[str]:
        return list(self._changed)

    def merged_pull_requests(self, commit: str) -> list[PullRequest]:
        return list(self._merged.get(commit, []))

    def pull_request(self, number: int) -> PullRequest:
        return self._pulls[number]

    def release_exists(self, tag: str) -> bool:
        return tag in self.releases

    def create_release(self, tag: str, commit: str, notes: str) -> None:
        self.created.append((tag, commit, notes))
        self.releases.add(tag)

    def variable(self, name: str) -> str | None:
        return self._variables.get(name)


class FakeProcess:
    """Records each call and answers from a table keyed by the last argument."""

    def __init__(
        self,
        installed: bool = True,
        answers: dict[str, Completed] | None = None,
        default: Completed | None = None,
    ) -> None:
        self.installed = installed
        self.answers = answers or {}
        self.default = default or Completed(0, "", "")
        self.calls: list[list[str]] = []

    def run(self, args: list[str], cwd: str | None = None) -> Completed:
        self.calls.append(args)
        return self.answers.get(args[-1], self.default)

    def which(self, name: str) -> str | None:
        return f"/bin/{name}" if self.installed else None
