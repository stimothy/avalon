"""The workflow check: reads a workflow file and reports each rule it breaks."""

from __future__ import annotations

import re

SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
DRAFT = {"github.event.pull_request.draft == false", "!github.event.pull_request.draft"}
OUTPUT = re.compile(r"^needs\.[\w-]+\.outputs\.[\w-]+ == 'true'$")
WRITE = re.compile(r"^\s+[\w-]+:\s*write\s*$|^\s*permissions:\s*write-all\s*$")
USES = re.compile(r"^\s*(?:-\s+)?uses:\s*(.*)$")
JOB_IF = re.compile(r"^    if:\s*(.*)$")
JOB_HEADER = re.compile(r"^  ([\w-]+):\s*$")
RELEASE_WORKFLOW = "release.yml"
RELEASE_JOB = "release"
FINAL_WORKFLOW = "gates.yml"


def _strip(line: str) -> str:
    return re.sub(r"\s+#.*$", "", line).rstrip()


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


def check(name: str, text: str) -> list[str]:
    """Return one line for each finding in the workflow `name`; empty means it passes."""
    lines = [_strip(raw) for raw in text.splitlines()]
    jobs: list[str] = []
    job_has_permissions: dict[str, bool] = {}
    owners: dict[int, str] = {}
    top_level_permissions = False
    in_jobs = False
    current: str | None = None
    found: list[str] = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        if "pull_request_target" in line:
            found.append(f"{name}:{number}: the pull_request_target trigger is not allowed")
        used = USES.match(line)
        if used:
            value = used.group(1).strip().strip("'\"")
            if not value.startswith("./") and not SHA.match(value):
                found.append(f"{name}:{number}: action not pinned to a full commit SHA: {value}")
        if re.match(r"^\S", line):
            in_jobs = line.startswith("jobs:")
            current = None
            top_level_permissions = top_level_permissions or line.startswith("permissions:")
        header = JOB_HEADER.match(line)
        if in_jobs and header:
            current = header.group(1)
            jobs.append(current)
            job_has_permissions[current] = False
        if current is not None:
            owners[number] = current
        if current is not None and re.match(r"^    permissions:", line):
            job_has_permissions[current] = True
        if WRITE.match(line) and not (name == RELEASE_WORKFLOW and current == RELEASE_JOB):
            found.append(f"{name}:{number}: write permission outside the release job")

    if not top_level_permissions:
        for job in jobs:
            if not job_has_permissions[job]:
                found.append(f"{name}: job {job} states no permissions")
        if not jobs:
            found.append(f"{name}: states no permissions")

    for number, line in enumerate(lines, start=1):
        condition = JOB_IF.match(line)
        owner = owners.get(number)
        if condition and owner:
            is_final = name == FINAL_WORKFLOW and owner == jobs[-1]
            problem = _condition_problem(condition.group(1), is_final)
            if problem:
                found.append(f"{name}:{number}: job {owner} condition: {problem}")
    return found
