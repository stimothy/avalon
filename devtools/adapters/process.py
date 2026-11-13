"""The one adapter that starts processes. Tests replace it with a fake."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Completed:
    returncode: int
    stdout: str
    stderr: str


class ProcessPort(Protocol):
    def run(self, args: list[str], cwd: str | None = None) -> Completed: ...

    def which(self, name: str) -> str | None: ...


class RealProcess:
    """Starts a real process."""

    def run(self, args: list[str], cwd: str | None = None) -> Completed:
        done = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
        return Completed(done.returncode, done.stdout, done.stderr)

    def which(self, name: str) -> str | None:
        return shutil.which(name)
