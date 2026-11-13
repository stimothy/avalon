---
title: 'Story 1.14: The owner turns the rules on, and a drill proves them'
type: 'chore'
created: '2026-11-13'
status: 'in-review'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/docs/design/gates-workflow.md'
  - '{project-root}/docs/design/release.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The ruleset on `master` is mostly on, but the repo has no contributor guide beyond setup and checks, no issue or pull request templates, no design doc recording the settings, no `none` label, and no drill proving the gates and the release path.

**Approach:** Check each setting against the repo, record each with its applying command in a design doc, finish `CONTRIBUTING.md`, add the three templates, link the latest release from the README, and run one drill pull request. The owner approves each setting command.

## Boundaries & Constraints

**Always:** Docs follow LAW-000009 and state only what is true now (LAW-000005, LAW-000006). `CONTRIBUTING.md` points to laws and design docs and restates none. An agent runs a settings command only after the owner approves it. Plugin evals run on the contributor's machine; no workflow calls a model or holds a credential, and no secret is stored. The drill records each result in the pull request.

**Never:** No edit to `docs/laws/`. No `pull_request_target`. No plan citations in any tracked file or in pull request text.

</frozen-after-approval>

## Code Map

- `.github/workflows/gates.yml`, `pr.yml`, `release.yml` -- the rules the drill exercises; do not change.
- `docs/design/gates-workflow.md`, `docs/design/release.md` -- existing design docs; the settings doc is a new sibling, listed in `docs/design/README.md`.
- `CONTRIBUTING.md` -- has set-up, suites, coverage, checks; add propose-a-change, gates and labels, laws and ADRs via round table, MIT licence, pointers.
- `README.md` -- Contributing section exists; add the latest-release link.
- `.github/` -- holds CODEOWNERS and dependabot only; add `ISSUE_TEMPLATE/bug.md`, `ISSUE_TEMPLATE/proposal.md`, `pull_request_template.md`.
- Live state (read 2026-11-13): ruleset 27176766 on the default branch requires a pull request, squash only, checks `all-green` and `pr`, up-to-date branch; labels `major`, `minor`, `patch`, `none` exist; private vulnerability reporting is on.

## Tasks & Acceptance

**Execution:**
- [x] `docs/design/repository-settings.md` -- record each setting and its command, and that an agent runs one only after owner approval -- AC 3
- [x] `docs/design/README.md`, `docs/design/glossary.md` -- list the doc; define any new term -- index rule
- [x] `CONTRIBUTING.md` -- complete per the story's guide criteria, and say that the evals run locally before a push and CI never calls a model -- AC 4
- [x] `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` -- bug, proposal, pull request templates -- AC 5
- [x] `README.md` -- link the latest release -- AC 7
- [x] `none` label created (owner approved); squash message is the title alone (ADR-0005 amended by a table; the setting already matched)
- [x] Settings checked against the repo; the admin bypass removed (owner approved)
- [ ] Drill -- one pull request through draft, ready, second push, missing label, labelled merge, and a `none` merge; record results in it -- AC 6

**Acceptance Criteria:**
- Given the settings, when checked against the repo, then they match the story's first criterion.
- Given the markdown lint, the gates, and the scan of tracked files, when the docs change, then all pass.

## Implementation Notes

The owner removed the secret requirement: evals run locally and no workflow calls a model. A table amended ADR-0005 (squash message is the title alone) and ADR-0003 and ADR-0004 (no eval job). Plan text in `epics.md` and the spine was edited to match. The owner removed the admin bypass and deferred the drill, so the drill task and its acceptance criterion stay open and the story is not done. The glossary needed no new term. Local checks passed: four suites, ruff, mypy, markdown lint.

## Verification

**Commands:**
- `npx markdownlint-cli2` -- expected: no finding
- `uv run python -m devtools.gates` checks as in `CONTRIBUTING.md` -- expected: pass
- `gh api repos/stimothy/avalon/rulesets/27176766` and `gh label list` -- expected: match AC 1
