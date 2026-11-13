---
title: 'Story 1.10: Gate logic lives in tested code'
type: 'feature'
created: '2026-11-13'
status: 'in-review'
baseline_commit: 'ae3b1b1d600bd3e83d9ae933309ec3e9eef3cf1d'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/docs/adr/0005-workflows-and-gates.md'
  - '{project-root}/docs/adr/0004-test-suites.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Gates.yml (Story 1.11) must hold no logic, but the code that decides which gates apply, gives the verdict, and checks workflow files does not exist yet, and `devtools/` has no adapter for `gh`.

**Approach:** Add three tested Python gates under `devtools/gates/` (changed-path filter, verdict, workflow check) and a `gh` adapter beside the existing git adapter, each wired into `python -m devtools.gates`. Tests replace both adapters with fakes.

## Boundaries & Constraints

**Always:** Follow LAW-000010 to LAW-000018 and ADR-0004/0005: one Act per test, unit tests touch no file system, subprocess, or network, mypy strict, ruff clean, 80% coverage. Python 3.9 compatible. The allowed `if:` forms are exactly ADR-0005's list.

**Never:** Write `.github/workflows/*` (Story 1.11). Edit ADRs or laws. Add a `utils`/`helpers`/`common`/`misc`/`tmp` directory. Add third-party dependencies (parse workflow YAML with a small line-based reader, not a new library).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Filter, plugin change | changed paths include `plugin/x` | prints `plugin=true`; `docs=false` if no `*.md` changed | N/A |
| Filter, none apply | only `devtools/a.py` | every output `false` | N/A |
| Verdict ok | all `success`, or `skipped` where the filter said not applicable | exit 0 | N/A |
| Verdict bad | a job `failure`, `cancelled`, or an unexplained `skipped` | exit 1, names the job | N/A |
| Workflow bad | unpinned action, no `permissions`, write permission outside the release job, `pull_request_target`, or a disallowed `if:` | exit 1, one line per finding | N/A |
| `gh`/git failure | adapter raises | exit 2, message on stderr | clear message |

</frozen-after-approval>

## Code Map

- `devtools/gates/__main__.py` -- argparse CLI; add subcommands `changed-paths`, `verdict`, `workflows`.
- `devtools/adapters/process.py`, `devtools/adapters/git.py` -- existing process/git adapters; git is extended, `gh` copies the pattern.
- `tests/fakes/gate_fakes.py` -- `FakeProcess`, `FakeGit`; add `FakeGh` and `changed_files` to `FakeGit`.
- `tests/unit/test_git_adapter.py` -- shape of an adapter unit test; `tests/contract/` holds fake-vs-real cases.
- `docs/adr/0005-workflows-and-gates.md` -- source of the rules to check.
- `docs/design/` -- update only if a doc becomes untrue (LAW-000008).

## Tasks & Acceptance

**Execution:**
- [x] `devtools/adapters/gh.py` -- `GhPort` + `RealGh` running `gh` through `ProcessPort` (`changed_files(pr)`) -- the one gh adapter
- [x] `devtools/adapters/git.py` -- add `changed_files(base)` -- adapter of its own for git
- [x] `devtools/gates/changed_paths.py` -- pure `outputs(paths) -> dict[str,bool]`: `plugin` (any path under `plugin/`) and `docs` (any `*.md` or under `docs/`) -- one output per conditional gate
- [x] `devtools/gates/verdict.py` -- pure `judge(results, applies) -> list[str]` of failures
- [x] `devtools/gates/workflow_check.py` -- pure `check(name, text) -> list[str]` implementing the rules
- [x] `devtools/gates/__main__.py` -- wire commands; outputs written as `name=true|false` lines for `$GITHUB_OUTPUT`
- [x] `tests/unit/test_changed_paths.py`, `test_verdict.py`, `test_workflow_check.py`, `test_gh_adapter.py`, `tests/fakes/gate_fakes.py` -- unit tests with fakes, one Act each
- [x] `tests/contract/` -- fake-versus-real git `changed_files` in a throwaway repo
- [x] `docs/design/` -- record the new commands if a doc lists the gates

**Acceptance Criteria:**
- Given changed paths, when the filter runs, then it emits one boolean per conditional gate.
- Given job results and filter outputs, when the verdict runs, then it passes only for success or a filter-justified skip.
- Given a workflow file, when the check runs, then each violation is reported and a clean file passes.
- Given `devtools/`, when it reaches GitHub or git, then it goes through `RealGh` or `RealGit` and tests use fakes.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

Choices made without the user (not visible in results): the two conditional gates are `plugin` (for `claude plugin validate`) and `docs` (markdown lint); Story 1.11 may add more by extending `changed_paths.py`.

## Verification

**Commands:**
- `uv run pytest tests/unit` -- expected: pass, under 10 s
- `uv run ruff check . && uv run ruff format --check . && uv run mypy` -- expected: no findings
- `uv run coverage run -m pytest && uv run coverage report` -- expected: >= 80%
