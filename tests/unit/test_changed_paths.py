from __future__ import annotations

from devtools.gates import changed_paths


def test_a_plugin_path_makes_the_plugin_gate_apply() -> None:
    found = changed_paths.outputs(["plugin/skill.json"])

    assert found == {"plugin": True, "docs": False}


def test_a_markdown_path_makes_the_docs_gate_apply() -> None:
    found = changed_paths.outputs(["README.md"])

    assert found == {"plugin": False, "docs": True}


def test_a_path_under_docs_makes_the_docs_gate_apply() -> None:
    found = changed_paths.outputs(["docs/adr/x.txt"])

    assert found["docs"] is True


def test_no_conditional_gate_applies_to_code_only() -> None:
    found = changed_paths.outputs(["devtools/a.py"])

    assert found == {"plugin": False, "docs": False}


def test_outputs_render_as_sorted_lines() -> None:
    lines = changed_paths.render({"plugin": True, "docs": False})

    assert lines == ["docs=false", "plugin=true"]
