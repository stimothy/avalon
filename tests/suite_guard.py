"""The shared guard: a process start or a network connection fails a test.

The guard covers the unit, integration, and end-to-end suites. The contract
suite is outside it, because contract tests start real git in a throwaway repo.
"""

from __future__ import annotations

import contextlib
import os
import socket
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any

GUARDED_SUITES = frozenset({"unit", "integration", "e2e"})
UNIT_BUDGET_SECONDS = 10.0
ORIGINAL_POPEN_INIT = subprocess.Popen.__init__

_PROCESS_CALLS: tuple[tuple[Any, str], ...] = (
    (subprocess.Popen, "__init__"),
    (os, "system"),
    (os, "posix_spawn"),
    (os, "posix_spawnp"),
    (os, "fork"),
)
_NETWORK_CALLS: tuple[tuple[Any, str], ...] = (
    (socket.socket, "connect"),
    (socket.socket, "connect_ex"),
)


class ForbiddenCallError(AssertionError):
    """Raised when a guarded test starts a process or opens a connection."""


def suite_of(path: Path) -> str | None:
    """Return the suite a test file belongs to, from its folder under tests/."""
    parts = path.parts
    if "tests" not in parts:
        return None
    below = parts[len(parts) - parts[::-1].index("tests") :]
    return below[0] if len(below) > 1 else None


def is_guarded(suite: str | None) -> bool:
    """Say whether the guard applies to a suite."""
    return suite in GUARDED_SUITES


def budget_exceeded(elapsed: float, limit: float = UNIT_BUDGET_SECONDS) -> bool:
    """Say whether a unit run took longer than its budget."""
    return elapsed > limit


def _refuse(kind: str) -> Any:
    def refuse(*_args: object, **_kwargs: object) -> Any:
        raise ForbiddenCallError(f"A guarded test must not {kind}.")

    return refuse


@contextlib.contextmanager
def blocked() -> Iterator[None]:
    """Fail any process start or network connection made inside the block."""
    saved: list[tuple[Any, str, Any]] = []
    groups = ((_PROCESS_CALLS, "start a process"), (_NETWORK_CALLS, "open a connection"))
    for targets, kind in groups:
        for owner, name in targets:
            if hasattr(owner, name):
                saved.append((owner, name, getattr(owner, name)))
                setattr(owner, name, _refuse(kind))
    try:
        yield
    finally:
        for owner, name, original in reversed(saved):
            setattr(owner, name, original)
