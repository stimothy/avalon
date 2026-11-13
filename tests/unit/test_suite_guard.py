from __future__ import annotations

import os
import socket
import subprocess
from pathlib import Path

import pytest

import suite_guard


def test_blocked_fails_a_process_start() -> None:
    with suite_guard.blocked(), pytest.raises(suite_guard.ForbiddenCallError):
        subprocess.run(["true"], check=False)


def test_blocked_fails_a_shell_command() -> None:
    with suite_guard.blocked(), pytest.raises(suite_guard.ForbiddenCallError):
        os.system("true")


def test_blocked_fails_a_connection() -> None:
    sock = socket.socket()
    with suite_guard.blocked(), pytest.raises(suite_guard.ForbiddenCallError):
        sock.connect(("127.0.0.1", 9))
    sock.close()


def test_blocked_restores_the_calls_on_exit() -> None:
    original = subprocess.Popen.__init__

    with suite_guard.blocked():
        pass

    assert subprocess.Popen.__init__ is original


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("tests/unit/test_a.py", "unit"),
        ("/repo/tests/integration/test_a.py", "integration"),
        ("tests/e2e/test_a.py", "e2e"),
        ("tests/contract/test_a.py", "contract"),
        ("tests/conftest.py", None),
        ("devtools/a.py", None),
    ],
)
def test_suite_of_reads_the_folder(path: str, expected: str | None) -> None:
    assert suite_guard.suite_of(Path(path)) == expected


@pytest.mark.parametrize(
    ("suite", "expected"),
    [("unit", True), ("integration", True), ("e2e", True), ("contract", False), (None, False)],
)
def test_guard_covers_the_first_three_suites_only(suite: str | None, expected: bool) -> None:
    assert suite_guard.is_guarded(suite) is expected


@pytest.mark.parametrize(("elapsed", "expected"), [(9.9, False), (10.0, False), (10.1, True)])
def test_budget_is_exceeded_only_above_ten_seconds(elapsed: float, expected: bool) -> None:
    assert suite_guard.budget_exceeded(elapsed) is expected


@pytest.fixture(scope="module")
def popen_during_module_fixture_setup() -> object:
    return subprocess.Popen.__init__


def test_the_guard_is_on_during_higher_scoped_fixture_setup(
    popen_during_module_fixture_setup: object,
) -> None:
    original = suite_guard.ORIGINAL_POPEN_INIT

    assert popen_during_module_fixture_setup is not original
