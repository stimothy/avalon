from __future__ import annotations

import pytest

from devtools.gates import skip_list


@pytest.mark.parametrize("folder", skip_list.PLAN_FOLDERS)
def test_a_file_under_a_plan_folder_is_skipped(folder: str) -> None:
    skipped = skip_list.is_skipped(f"{folder}/a/b.md")

    assert skipped is True


@pytest.mark.parametrize("path", skip_list.LOCK_FILES)
def test_a_lock_file_is_skipped(path: str) -> None:
    skipped = skip_list.is_skipped(path)

    assert skipped is True


def test_an_ordinary_file_is_not_skipped() -> None:
    skipped = skip_list.is_skipped("docs/a.md")

    assert skipped is False


def test_a_folder_that_only_starts_with_a_plan_folder_name_is_not_skipped() -> None:
    skipped = skip_list.is_skipped(skip_list.PLAN_FOLDERS[0] + "-more/a.md")

    assert skipped is False


def test_the_skip_list_file_may_name_a_plan_folder() -> None:
    allowed = skip_list.may_name_a_plan_folder("devtools/gates/skip_list.py")

    assert allowed is True
