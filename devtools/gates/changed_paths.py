"""The changed-path filter: which gates that apply to only some changes apply."""

from __future__ import annotations


def outputs(paths: list[str]) -> dict[str, bool]:
    """Return one output for each conditional gate, true when the gate applies."""
    return {
        "plugin": any(path.startswith("plugin/") for path in paths),
        "docs": any(path.endswith(".md") or path.startswith("docs/") for path in paths),
    }


def render(found: dict[str, bool]) -> list[str]:
    """Render the outputs as `name=true|false` lines for a GitHub output file."""
    return [f"{name}={'true' if applies else 'false'}" for name, applies in sorted(found.items())]
