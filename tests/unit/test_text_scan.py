from __future__ import annotations

import pytest

from devtools.gates import skip_list, text_scan

# Sample IDs and paths are built here, so no file stores one.
PLAN_ID = "F" + "R-" + "12"
HOME_PATH = "/Us" + "ers/" + "alice/notes"
FOLDER = skip_list.PLAN_FOLDERS[0]


def test_a_plan_id_is_found_with_its_file_and_line() -> None:
    found = text_scan.scan_file("docs/a.md", f"first\nsee {PLAN_ID} here\n")

    assert [(f.path, f.line, f.text) for f in found] == [("docs/a.md", 2, PLAN_ID)]


@pytest.mark.parametrize(
    "text",
    [
        "xF" + "R-12",
        "F" + "R-12x",
        "f" + "r-12",
        "F" + "R-",
        "F" + "R12",
    ],
)
def test_the_same_letters_in_a_longer_word_or_another_case_pass(text: str) -> None:
    found = text_scan.scan_file("docs/a.md", text)

    assert found == []


def test_a_plan_folder_name_is_found_in_a_file_not_allowed_to_name_one() -> None:
    found = text_scan.scan_file("docs/a.md", f"see {FOLDER}/x.md")

    assert [f.kind for f in found] == ["plan folder"]


@pytest.mark.parametrize("path", skip_list.MAY_NAME_A_PLAN_FOLDER)
def test_a_file_allowed_to_name_a_plan_folder_passes(path: str) -> None:
    found = text_scan.scan_file(path, f"see {FOLDER}/x.md")

    assert found == []


def test_a_home_path_is_found() -> None:
    found = text_scan.scan_file("docs/a.md", f"open {HOME_PATH}")

    assert [(f.kind, f.line) for f in found] == [("home path", 1)]


def test_a_windows_home_path_is_found() -> None:
    windows = "C:" + "\\Us" + "ers\\bob\\x"

    found = text_scan.scan_file("docs/a.md", windows)

    assert [f.kind for f in found] == ["home path"]


def test_a_pull_request_title_and_body_are_checked_for_plan_citations() -> None:
    found = text_scan.scan_pull_request(f"Fix {PLAN_ID}", f"body\n{FOLDER}")

    assert [(f.path, f.kind) for f in found] == [
        ("pull request title", "plan ID"),
        ("pull request body", "plan folder"),
    ]


def test_a_pull_request_without_citations_passes() -> None:
    found = text_scan.scan_pull_request("Add a gate", "It scans files.")

    assert found == []


def test_a_finding_renders_the_file_and_the_line() -> None:
    finding = text_scan.Finding("a.md", 3, "plan ID", "X")

    rendered = finding.render()

    assert rendered == "a.md:3: plan ID: X"
