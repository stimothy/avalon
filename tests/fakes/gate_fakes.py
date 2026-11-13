"""Fakes for the adapters that the gates call."""

from __future__ import annotations

from devtools.adapters.process import Completed


class FakeGit:
    def __init__(self, files: list[str], changed: list[str] | None = None) -> None:
        self._files = files
        self._changed = changed or []

    def tracked_files(self) -> list[str]:
        return list(self._files)

    def changed_files(self, base: str) -> list[str]:
        return list(self._changed)


class FakeGh:
    def __init__(self, changed: list[str]) -> None:
        self._changed = changed

    def changed_files(self, pull_request: int) -> list[str]:
        return list(self._changed)


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
