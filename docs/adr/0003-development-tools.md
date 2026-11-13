---
adr: 0003
summary: Tests, coverage, lint, format, and types are handled by pytest, coverage, ruff, and mypy, configured in one pyproject.toml, and the lock file is the only home of a tool version.
covers: [pyproject.toml, uv.lock, .venv/**, .github/workflows/**]
origin: user
---
# ADR-0003: Development tools

## Context

This repo authors Python that has tests, a coverage floor (LAW-000014), and a format and type standard. Something must run the tests, measure the coverage, and check the code.

The tools run on a developer's machine and in workflows. A tool version stated in more than one place can differ between them. The repo shows no earlier choice of tools. The reason for each choice below is unknown, except where the text gives one.

The primary technologies are:

- pytest, which runs tests
- coverage, which measures them
- ruff, which lints and checks the format
- mypy, which checks types
- uv, which locks the versions of these tools

## Decision

### The development tools

- `pytest` runs tests, `coverage` measures them, `ruff` lints and checks the format, and `mypy` checks types.
- Their configuration lives in the single `pyproject.toml` at the repo root.
- A virtual environment named `.venv`, which git ignores, holds them.
- Coverage is line coverage over the Python that LAW-000014 measures.
- Each suite's gate job collects coverage data, except the eval job, which collects none.
- One job combines the data from every other suite.
- The unit run is timed against its budget with coverage on.

### The lock file is the only home of a tool version

- The development tools are declared in `pyproject.toml`, and `uv` locks their versions in `uv.lock`.
- No ADR, doc, or workflow states the version of a tool that `uv.lock` locks.
- Workflows install the tools only from the lock file.
- The workflow gate of ADR-0005 fails a workflow that installs a locked tool any other way.
- A tool that `uv.lock` cannot lock, such as `gitleaks`, has its version home in the ADR that owns it (ADR-0005).
- A reviewer checks the ADRs and docs.

## Consequences

- A tool version changes in `uv.lock` and nowhere else.
- Changing a tool, or dropping the lock, goes through a round table.
- One configuration file serves every tool, so a setting for one tool sits beside the settings for the others.
- Coverage from the eval suite is absent by design, so the combined figure covers the other suites only.
- The check on docs is a reviewer's judgment. No gate reads a doc for a tool version.

## Alternatives rejected

- **Rejected: separate linter and formatter tools, such as black and flake8.** The reason is unknown.
- **Rejected: another type checker, such as pyright.** The reason is unknown.
- **Rejected: no type checker.** The reason is unknown.
- **Rejected: unittest in place of pytest.** The reason is unknown.
- **Rejected: one config file for each tool.** The reason is unknown.
- **Rejected: coverage from the unit and integration runs only.** The reason is unknown.
- **Rejected: pin versions in each workflow.** The reason is unknown.
- **Rejected: pip with a requirements file.** The reason is unknown.
- **Rejected: pip-tools.** The reason is unknown.
- **Rejected: poetry.** The reason is unknown.
- **Rejected: pdm.** The reason is unknown.
- **Rejected: no lock.** The reason is unknown.

## Changelog

- 2026-11-12 (agent, table): Created. Recorded the development tools, their one configuration file, and the lock file as the only home of a tool version.
- 2026-11-12 (user): Confirmed the decisions of this ADR.
- 2026-11-13 (user, table): Amended. Linked the version home of a tool that `uv.lock` cannot lock to ADR-0005.
