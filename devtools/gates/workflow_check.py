"""The workflow check: reads a workflow file and reports each rule it breaks."""

from __future__ import annotations

import re

SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
DRAFT = {"github.event.pull_request.draft == false", "!github.event.pull_request.draft"}
OUTPUT = re.compile(r"^needs\.[\w-]+\.outputs\.[\w-]+ == '(true|false)'$")
WRITE = re.compile(
    r"^\s+[\w-]+:\s*write\s*$|^\s*permissions:\s*write-all\s*$|^\s*permissions:\s*\{[^}]*:\s*write"
)
USES = re.compile(r"^\s*(?:-\s+)?uses:\s*(.*)$")
KEY = re.compile(r"^([\w-]+):(?:\s|$)")
INSTALL = re.compile(
    r"\b(pip3?\s+install|uv\s+pip\s+install|uvx|npx|npm\s+(install|i|add)\s+[^-\s])", re.IGNORECASE
)
RELEASE_WORKFLOW = "release.yml"
RELEASE_JOB = "release"
FINAL_WORKFLOW = "gates.yml"


def _strip(line: str) -> str:
    return re.sub(r"\s+#.*$", "", line).rstrip()


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _unwrap(value: str) -> str:
    value = value.strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"":
        value = value[1:-1]
    if value.startswith("${{") and value.endswith("}}"):
        value = value[3:-2].strip()
    return value


def _condition_problem(condition: str, is_final: bool) -> str | None:
    parts = [part.strip() for part in _unwrap(condition).split("&&")]
    if "always()" in parts:
        if not (is_final and any(part in DRAFT for part in parts)):
            return "always() only with the draft test, on the final job of gates.yml"
        parts = [part for part in parts if part != "always()"]
    for part in parts:
        if part not in DRAFT and not OUTPUT.match(part):
            return f"not an allowed form: {condition.strip()}"
    return None


def _line_problems(name: str, number: int, line: str) -> list[str]:
    found = []
    if "pull_request_target" in line:
        found.append(f"{name}:{number}: the pull_request_target trigger is not allowed")
    used = USES.match(line)
    if used:
        value = used.group(1).strip().strip("'\"")
        if not value.startswith("./") and not SHA.match(value):
            found.append(f"{name}:{number}: action not pinned to a full commit SHA: {value}")
    elif INSTALL.search(line):
        found.append(f"{name}:{number}: a tool installed any way but from the lock file")
    elif "gitleaks" in line.lower() and "devtools" not in line:
        found.append(f"{name}:{number}: gitleaks installed any way but the two allowed")
    return found


class _Job:
    def __init__(self, name: str) -> None:
        self.name = name
        self.prop_indent: int | None = None
        self.has_permissions = False
        self.conditions: list[tuple[int, str]] = []


def check(name: str, text: str) -> list[str]:
    """Return one line for each finding in the workflow `name`; empty means it passes."""
    lines = [_strip(raw) for raw in text.splitlines()]
    jobs: list[_Job] = []
    top_level_permissions = False
    in_jobs = False
    job_indent: int | None = None
    current: _Job | None = None
    found: list[str] = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        found += _line_problems(name, number, line)
        indent = _indent(line)
        if indent == 0:
            in_jobs = line.startswith("jobs:")
            current = None
            top_level_permissions = top_level_permissions or line.startswith("permissions:")
        elif in_jobs:
            if job_indent is None:
                job_indent = indent
            if indent == job_indent:
                header = KEY.match(line.strip())
                current = _Job(header.group(1)) if header else None
                if current:
                    jobs.append(current)
            elif current is not None:
                if current.prop_indent is None:
                    current.prop_indent = indent
                if indent == current.prop_indent:
                    key = KEY.match(line.strip())
                    if key and key.group(1) == "permissions":
                        current.has_permissions = True
                    if key and key.group(1) == "if":
                        current.conditions.append((number, line.strip()[3:]))
        in_release_job = name == RELEASE_WORKFLOW and current is not None
        in_release_job = in_release_job and current is not None and current.name == RELEASE_JOB
        if WRITE.match(line) and not in_release_job:
            found.append(f"{name}:{number}: write permission outside the release job")

    if not top_level_permissions:
        for job in jobs:
            if not job.has_permissions:
                found.append(f"{name}: job {job.name} states no permissions")
        if not jobs:
            found.append(f"{name}: states no permissions")

    for job in jobs:
        is_final = name == FINAL_WORKFLOW and job is jobs[-1]
        for number, condition in job.conditions:
            problem = _condition_problem(condition, is_final)
            if problem:
                found.append(f"{name}:{number}: job {job.name} condition: {problem}")
    return found
