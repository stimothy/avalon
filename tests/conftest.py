"""Shared test rules: the guard for the first three suites and the unit time budget."""

from __future__ import annotations

import time
from collections.abc import Generator

import pytest

import suite_guard

_state = {"started": 0.0}


@pytest.hookimpl(wrapper=True)
def pytest_runtest_protocol(
    item: pytest.Item, nextitem: pytest.Item | None
) -> Generator[None, object, object]:
    """Guard a test's whole life: fixture setup, the call, and fixture teardown."""
    if suite_guard.is_guarded(suite_guard.suite_of(item.path)):
        with suite_guard.blocked():
            return (yield)
    return (yield)


def pytest_sessionstart(session: pytest.Session) -> None:
    _state["started"] = time.monotonic()


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    suites = {suite_guard.suite_of(item.path) for item in session.items}
    elapsed = time.monotonic() - _state["started"]
    if suites == {"unit"} and suite_guard.budget_exceeded(elapsed):
        print(f"\nThe unit run took longer than {suite_guard.UNIT_BUDGET_SECONDS} seconds.")
        session.exitstatus = pytest.ExitCode.TESTS_FAILED
