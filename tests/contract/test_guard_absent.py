import subprocess

import suite_guard


def test_the_contract_suite_may_start_a_process() -> None:
    result = subprocess.run(["git", "--version"], capture_output=True, check=False)

    assert result.returncode == 0
    assert not suite_guard.is_guarded("contract")
