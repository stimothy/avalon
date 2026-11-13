"""The one home of what the scan of tracked files skips and who may name a plan folder."""

from __future__ import annotations

PLAN_FOLDERS: tuple[str, ...] = ("_bmad-output", "_bmad", "temporary-plans")

LOCK_FILES: tuple[str, ...] = ("uv.lock", "package-lock.json")

# The only tracked files that may name a plan folder, besides this one.
MAY_NAME_A_PLAN_FOLDER: tuple[str, ...] = (
    "devtools/gates/skip_list.py",
    ".gitignore",
    "pyproject.toml",
    ".markdownlint-cli2.jsonc",
)


def is_skipped(path: str) -> bool:
    """Return True when the scan of tracked files does not read this path."""
    if path in LOCK_FILES:
        return True
    return any(path == folder or path.startswith(folder + "/") for folder in PLAN_FOLDERS)


def may_name_a_plan_folder(path: str) -> bool:
    """Return True when this path is allowed to name a plan folder."""
    return path in MAY_NAME_A_PLAN_FOLDER
