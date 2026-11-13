import subprocess

import pytest

import suite_guard


def test_the_guard_fails_a_process_start_in_the_integration_suite() -> None:
    with pytest.raises(suite_guard.ForbiddenCallError):
        subprocess.run(["true"], check=False)
