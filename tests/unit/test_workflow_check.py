from __future__ import annotations

from devtools.gates import workflow_check

SHA = "a" * 40
DRAFT = "github.event.pull_request.draft == false"


def _workflow(
    uses: str = f"actions/checkout@{SHA}",
    condition: str = DRAFT,
    permissions: str = "permissions:\n  contents: read\n",
    trigger: str = "pull_request",
) -> str:
    return (
        f"on:\n  {trigger}:\n{permissions}jobs:\n  build:\n    if: {condition}\n"
        f"    steps:\n      - uses: {uses}\n"
    )


def test_a_clean_workflow_passes() -> None:
    found = workflow_check.check("gates.yml", _workflow())

    assert found == []


def test_an_action_pinned_to_a_tag_fails() -> None:
    found = workflow_check.check("gates.yml", _workflow(uses="actions/checkout@v4"))

    assert found == ["gates.yml:9: action not pinned to a full commit SHA: actions/checkout@v4"]


def test_a_local_action_needs_no_pin() -> None:
    found = workflow_check.check("gates.yml", _workflow(uses="./.github/actions/x"))

    assert found == []


def test_a_workflow_without_permissions_fails() -> None:
    found = workflow_check.check("gates.yml", _workflow(permissions=""))

    assert found == ["gates.yml: job build states no permissions"]


def test_job_level_permissions_pass() -> None:
    text = (
        f"on:\n  pull_request:\njobs:\n  build:\n    permissions:\n      contents: read\n"
        f"    if: {DRAFT}\n    steps:\n      - uses: actions/checkout@{SHA}\n"
    )

    found = workflow_check.check("gates.yml", text)

    assert found == []


def test_a_workflow_with_no_jobs_and_no_permissions_fails() -> None:
    found = workflow_check.check("gates.yml", "on:\n  pull_request:\n")

    assert found == ["gates.yml: states no permissions"]


def test_a_write_permission_outside_the_release_job_fails() -> None:
    found = workflow_check.check(
        "gates.yml", _workflow(permissions="permissions:\n  contents: write\n")
    )

    assert found == ["gates.yml:4: write permission outside the release job"]


def test_write_all_fails() -> None:
    found = workflow_check.check("gates.yml", _workflow(permissions="permissions: write-all\n"))

    assert found == ["gates.yml:3: write permission outside the release job"]


def test_a_write_permission_in_the_release_job_passes() -> None:
    text = (
        "on:\n  push:\njobs:\n  release:\n    permissions:\n      contents: write\n"
        f"    steps:\n      - uses: actions/checkout@{SHA}\n"
    )

    found = workflow_check.check("release.yml", text)

    assert found == []


def test_a_write_permission_in_another_job_of_the_release_workflow_fails() -> None:
    text = "on:\n  push:\njobs:\n  other:\n    permissions:\n      contents: write\n"

    found = workflow_check.check("release.yml", text)

    assert found == ["release.yml:6: write permission outside the release job"]


def test_the_pull_request_target_trigger_fails() -> None:
    found = workflow_check.check("gates.yml", _workflow(trigger="pull_request_target"))

    assert found == ["gates.yml:2: the pull_request_target trigger is not allowed"]


def test_an_output_test_passes() -> None:
    found = workflow_check.check(
        "gates.yml", _workflow(condition="${{ needs.changes.outputs.plugin == 'true' }}")
    )

    assert found == []


def test_a_draft_test_joined_with_an_output_test_passes() -> None:
    condition = f"{DRAFT} && needs.changes.outputs.docs == 'true'"

    found = workflow_check.check("gates.yml", _workflow(condition=condition))

    assert found == []


def test_a_free_form_condition_fails() -> None:
    found = workflow_check.check("gates.yml", _workflow(condition="github.actor == 'me'"))

    assert found == ["gates.yml:7: job build condition: not an allowed form: github.actor == 'me'"]


def test_always_with_the_draft_test_passes_on_the_final_job_of_gates() -> None:
    found = workflow_check.check("gates.yml", _workflow(condition=f"always() && {DRAFT}"))

    assert found == []


def test_always_alone_fails_on_the_final_job() -> None:
    found = workflow_check.check("gates.yml", _workflow(condition="always()"))

    assert found == [
        "gates.yml:7: job build condition: "
        "always() only with the draft test, on the final job of gates.yml"
    ]


def test_always_fails_outside_gates() -> None:
    found = workflow_check.check("pr.yml", _workflow(condition=f"always() && {DRAFT}"))

    assert len(found) == 1


def test_a_comment_after_a_pin_is_ignored() -> None:
    found = workflow_check.check("gates.yml", _workflow(uses=f"actions/checkout@{SHA} # v4.1.0"))

    assert found == []
