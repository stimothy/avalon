from __future__ import annotations

import pytest

from devtools.adapters.gh import GhError, RealGh
from fakes.gate_fakes import FakeProcess


def test_a_missing_gh_is_an_adapter_error() -> None:
    process = FakeProcess(installed=False)

    with pytest.raises(GhError, match="not installed"):
        RealGh(process, "/repo").changed_files(7)
