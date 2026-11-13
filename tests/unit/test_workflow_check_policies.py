from __future__ import annotations

from devtools.gates import workflow_check

SHA = "a" * 40


def test_an_inline_write_mapping_fails() -> None:
    text = "permissions: {contents: write}\njobs:\n  a:\n    steps: []\n"

    found = workflow_check.check("gates.yml", text)

    assert found == ["gates.yml:1: write permission outside the release job"]


def test_a_job_level_inline_write_mapping_fails() -> None:
    text = "permissions: {}\njobs:\n  a:\n    permissions: {issues: write}\n"

    found = workflow_check.check("gates.yml", text)

    assert found == ["gates.yml:4: write permission outside the release job"]


def test_a_wider_indent_still_finds_a_forbidden_condition() -> None:
    text = "permissions: {}\njobs:\n    a:\n        if: github.actor == 'me'\n"

    found = workflow_check.check("gates.yml", text)

    assert found == ["gates.yml:4: job a condition: not an allowed form: github.actor == 'me'"]


def test_a_wider_indent_finds_jobs_without_permissions() -> None:
    text = "jobs:\n    a:\n        steps: []\n"

    found = workflow_check.check("gates.yml", text)

    assert found == ["gates.yml: job a states no permissions"]


def test_a_test_of_a_false_output_passes() -> None:
    text = "permissions: {}\njobs:\n  a:\n    if: needs.changes.outputs.docs == 'false'\n"

    found = workflow_check.check("gates.yml", text)

    assert found == []


def test_pip_install_fails() -> None:
    text = "permissions: {}\njobs:\n  a:\n    steps:\n      - run: pip install ruff\n"

    found = workflow_check.check("gates.yml", text)

    assert found == ["gates.yml:5: a tool installed any way but from the lock file"]


def test_npx_fails() -> None:
    text = "permissions: {}\njobs:\n  a:\n    steps:\n      - run: npx markdownlint-cli2\n"

    found = workflow_check.check("gates.yml", text)

    assert found == ["gates.yml:5: a tool installed any way but from the lock file"]


def test_the_lock_file_installs_pass() -> None:
    text = "permissions: {}\njobs:\n  a:\n    steps:\n      - run: uv sync && npm ci\n"

    found = workflow_check.check("gates.yml", text)

    assert found == []


def test_a_direct_gitleaks_download_fails() -> None:
    text = "permissions: {}\njobs:\n  a:\n    steps:\n      - run: curl -L gitleaks.tgz | tar x\n"

    found = workflow_check.check("gates.yml", text)

    assert found == ["gates.yml:5: gitleaks installed any way but the two allowed"]


def test_a_devtools_command_may_name_gitleaks() -> None:
    run = "python -m devtools install-gitleaks"
    text = f"permissions: {{}}\njobs:\n  a:\n    steps:\n      - run: {run}\n"

    found = workflow_check.check("gates.yml", text)

    assert found == []
