"""The one adapter of devtools that runs `gh`. Tests replace it with a fake."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

from devtools.adapters.process import Completed, ProcessPort


class GhError(RuntimeError):
    """Raised when `gh` fails."""


@dataclass(frozen=True)
class PullRequest:
    number: int
    labels: list[str]


class GhPort(Protocol):
    def changed_files(self, pull_request: int) -> list[str]: ...

    def merged_pull_requests(self, commit: str) -> list[PullRequest]: ...

    def pull_request(self, number: int) -> PullRequest: ...

    def release_exists(self, tag: str) -> bool: ...

    def create_release(self, tag: str, commit: str, notes: str) -> None: ...

    def variable(self, name: str) -> str | None: ...


class RealGh:
    """Reads and writes facts about a repo's pull requests and releases through `gh`."""

    def __init__(self, process: ProcessPort, root: str) -> None:
        self._process = process
        self._root = root

    def _run(self, args: list[str]) -> Completed:
        if self._process.which("gh") is None:
            raise GhError("gh is not installed or not on PATH")
        return self._process.run(["gh", *args], cwd=self._root)

    def _ok(self, args: list[str]) -> str:
        done = self._run(args)
        if done.returncode != 0:
            raise GhError(done.stderr.strip() or f"gh {args[0]} failed")
        return done.stdout

    def changed_files(self, pull_request: int) -> list[str]:
        out = self._ok(["pr", "diff", str(pull_request), "--name-only"])
        return [line for line in out.splitlines() if line]

    def merged_pull_requests(self, commit: str) -> list[PullRequest]:
        out = self._ok(["api", f"repos/{{owner}}/{{repo}}/commits/{commit}/pulls"])
        return [
            PullRequest(item["number"], [label["name"] for label in item["labels"]])
            for item in json.loads(out)
            if item.get("merged_at")
        ]

    def pull_request(self, number: int) -> PullRequest:
        out = self._ok(["pr", "view", str(number), "--json", "number,labels"])
        data = json.loads(out)
        return PullRequest(data["number"], [label["name"] for label in data["labels"]])

    def release_exists(self, tag: str) -> bool:
        done = self._run(["release", "view", tag])
        if done.returncode == 0:
            return True
        if "not found" in done.stderr.lower():
            return False
        raise GhError(done.stderr.strip() or "gh release view failed")

    def create_release(self, tag: str, commit: str, notes: str) -> None:
        self._ok(
            [
                "release",
                "create",
                tag,
                "--target",
                commit,
                "--title",
                tag,
                "--notes",
                notes,
                "--generate-notes",
            ]
        )

    def variable(self, name: str) -> str | None:
        done = self._run(["variable", "get", name])
        if done.returncode == 0:
            return done.stdout.strip()
        if "not found" in done.stderr.lower():
            return None
        raise GhError(done.stderr.strip() or "gh variable get failed")
