# Revision 1: tooling and delivery, for round 2

Chair: stand-in. The chair did not propose this matter. Status: revised; nothing is registered.

Items keep the numbers in `screening.md`. Each item gives the wording put to round 2, its alternatives, its origin, and one line on the amendments the chair took and declined. Decisions 5 and 8 and the held law are the user's. Amendments that would reword them are under "Held for the user" and are not in the wording below.

## Contradictions resolved by the chair

- **Coverage scope and LAW-000014.** LAW-000014 measures all authored Python, tests excluded. The real git adapter runs only in the contract suite, so a measure taken from the unit and integration runs alone would count it as uncovered. Decision 1 now takes coverage from every suite except the evals. Nothing is left out of the measure.
- **The unit time budget and coverage.** Coverage slows a run. Decision 1 times the unit run with coverage on, which is the slower run. A unit run that meets the budget there also meets it without coverage, so LAW-000012 holds under either reading.
- **The GitHub lookup in the release code.** No suite may reach the network (LAW-000012, LAW-000013, and the contract suite's own reach). Decision 3 puts GitHub behind a port that every suite fakes. The real GitHub adapter runs only in the release workflow, and its lines count toward the LAW-000014 measure like any other line.
- **A `major` label below 1.0.0.** Decision 8 lets a pull request labelled `major` merge, and decision 9 refuses to release it. Decision 9 now says what the run does at that commit. The cleaner fix, a refusal in the label check, rewords decision 8 and is held for the user.

## The decisions

### 1. The development tools (origin: agent, ADR-0003)

`pytest` runs tests, `coverage` measures them, `ruff` lints and checks the format, and `mypy` checks types. Their configuration lives in the single `pyproject.toml` at the repo root. A virtual environment named `.venv`, which git ignores, holds them. Coverage is line coverage over the Python that LAW-000014 measures. Each suite's gate job collects coverage data, and one job combines the data from every suite except the evals. The unit run is timed against its budget with coverage on.

Alternative: separate linter and formatter tools, such as black and flake8. Alternative: another type checker, such as pyright. Alternative: no type checker. Alternative: unittest in place of pytest. Alternative: one config file for each tool. Alternative: coverage from the unit and integration runs only.

Amendments: took the contract suite in the coverage measure (Sk), the venv name and the reference to LAW-000014 without its number (St), the alternatives (Sc), and the timed run (J). Declined the reasons for ruff and mypy in the decision text (St), because reasons belong in the ADR's context and rejected alternatives.

### 2. The lock file is the only home of a tool version (origin: agent, ADR-0003)

The development tools are declared in `pyproject.toml`, and `uv` locks their versions in `uv.lock`. No ADR, doc, or workflow states the version of a tool that `uv.lock` locks. Workflows install the tools only from the lock file, and the workflow gate of decision 4 fails a workflow that installs a locked tool any other way. A reviewer checks the ADRs and docs.

Alternative: pin versions in each workflow. Alternative: pip with a requirements file. Alternative: pip-tools. Alternative: poetry. Alternative: pdm. Alternative: no lock.

Amendments: took "the version of a tool that `uv.lock` locks" and dropped the plugin-folder sentence, which repeats ADR-0001 (J); took a named check (St), split between the workflow gate and review; took the alternatives (Sc).

### Held law (origin: user), heard here

| Scope | Proposed law | Check |
|---|---|---|
| code | Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding. | Gates run each tool. |

If decision 1 fails, the law stays held.

Amendments: took "format check", "with no finding", and the ADR's ID (J), as clarifications of the user's words. Declined dropping the ADR reference (St), because ADR IDs never change, and the reference keeps tool names out of the law as the user's wording does. Held the bar on suppressions (Sk), because it adds a rule the user did not state.

### 3. Each suite has a folder and a fixed reach (origin: agent, ADR-0004)

A test's folder sets its suite. Each suite may reach only what this table allows.

| Suite | May reach |
|---|---|
| Unit | One unit, with every port faked. |
| Integration | The real file system in a temporary folder, with git and GitHub faked. |
| End-to-end | The whole command line and the hook, in process, on a temporary folder, with git and GitHub faked. |
| Contract | Real git, in a throwaway repo. |
| Eval | Claude Code, a model, and a copy of a fixture. |

The contract suite runs each git fake and its real adapter through the same cases. The release code reaches GitHub only through a port. No suite runs the real GitHub adapter. Each suite is its own gate job.

Alternative: one suite with markers. Alternative: no contract suite, with the git fakes trusted. Alternative: real git in the integration suite. Alternative: the contract suite on a schedule, not on each pull request.

Amendments: took the name "eval" (J, St), the GitHub port (J), and the scheduled contract suite as an alternative (Sc). Declined real git in one end-to-end test as an alternative (Sc), because LAW-000013 forbids it, so it is not a real choice.

### 4. Workflows hold no logic (origin: agent, ADR-0005)

A workflow file sets triggers, permissions, and steps that call a command. Anything that computes or branches is Python under `devtools/`, written to the same standards and tested in the same suites. A job's `if:` takes only these forms, alone or joined by `&&`:

- the pull request is not a draft;
- a true or false output that a `devtools/` command computed in an earlier job;
- `always()`, on the final job of `gates.yml` only.

A gate reads every workflow and fails on any other form. Every action is pinned to a full commit SHA, and a pin changes only by a pull request. Every workflow states its permissions. Only the job in `release.yml` may write, and only tags and releases.

Alternative: logic in shell steps inside workflows. Alternative: third-party actions that hold the logic.

Amendments: took the closed list in the ADR (J), took how pins change (St), and took the write exception from item 9 (St). Declined keeping the list in `devtools/` (P), because the ADR then would not say what the gate allows.

### 5. Gates run only on a pull request that is ready for review (origin: user, ADR-0005)

The gates run on a pull request into `master` when it is opened, reopened, given new commits, or marked ready for review. `pr.yml` also runs when the title, body, or labels change, because it checks them. A draft runs no job. A newer run cancels the older run. No gate runs on `master` itself, and no workflow uses `pull_request_target`.

Alternative: gates on every push. Alternative: gates on drafts too. Alternative: gates on `master` after the merge.

Amendments: took the added events for `pr.yml` (P, J) as a clarification the user's intent implies: decision 8 blocks a merge without one label, and without these events, fixing a label or title would not run the check again. "A newer push" became "a newer run" to cover those events. Declined a stated reason for no gate on `master` (St, Sk), because the user has not given one. Decision 7's up-to-date rule means the head of `master` is a state the gates passed.

### 6. Two workflows gate a pull request, and one job gives the verdict (origin: agent, ADR-0005)

`gates.yml` holds the checks of the code and the docs. `pr.yml` holds the checks of the pull request itself: its version label, and the scan of its title and body. The final job of `gates.yml` fails unless every other job succeeded or was skipped by its own `if:`. A gate that applies to some changes is a job with an `if:`, not a workflow with a path filter.

Alternative: one workflow. Alternative: a workflow for each check. Alternative: path filters on workflows. Alternative: the ruleset requires each job by name.

Amendments: took "skipped by its own `if:`" (J), which also makes every skip explicit (Sk), and the alternative (Sc).

### 7. A ruleset protects `master` (origin: agent, ADR-0005)

A ruleset on `master` requires a pull request, the final job of `gates.yml`, the label check, and a branch that is up to date. It allows squash merges only, and the squash message is the pull request's title and description. It has no bypass actors, the owner included. The owner sets it by hand in the repository settings, and no gate checks it.

Alternative: no ruleset, relying on review. Alternative: classic branch protection. Alternative: merge commits or rebase merges. Alternative: the default squash message. Alternative: no up-to-date requirement.

Amendments: took no bypass actors (Sk), the statement of who sets it and that no gate checks it (St, J), and the alternatives (Sc).

### 8. A release is chosen by a label (origin: user, ADR-0006)

A merge into `master` releases the next version. The pull request carries exactly one of the labels `major`, `minor`, and `patch`, and the label picks the version. A pull request with no single version label cannot merge.

Alternative: the version comes from commit messages, such as Conventional Commits. Alternative: a tool that reads commit messages, such as release-please or semantic-release. Alternative: a version file edited in the pull request. Alternative: a person tags by hand. Alternative: a release only when asked.

Amendments: took the alternatives (Sc), which leave the decision's words unchanged. Held the `none` label (Sk) and the refusal of `major` in the label check (J), because each rewords the user's decision.

### 9. One workflow releases, catches up, and writes nothing else (origin: agent, ADR-0006)

`release.yml` is the only workflow that runs on a push to `master`. Each run releases every commit newer than the latest version, oldest first, each by the label of its merged pull request. Before the first version exists, the run starts at the commit that added `release.yml`. One call makes a version: it creates the tag and the release with its notes. The workflow never pushes a commit, and a run is safe to repeat.

While the latest version is below 1.0.0, the release code refuses `major` unless a repository variable that only the owner sets allows it. The variable's name is unknown until it is chosen. A commit that has no merged pull request with exactly one version label, or that is refused, fails the run. The run releases nothing at or after that commit until the label or the variable is changed and the run is repeated.

A bad release is never deleted or retagged. A pull request that reverts it makes the next version. The release code lives under `devtools/`, outside `plugin/**`, so ADR-0001's rule that no script command tags does not reach it.

Alternative: release only the newest commit. Alternative: the workflow commits a version file. Alternative: no limit on `major` below 1.0.0. Alternative: release on a schedule. Alternative: a release pull request that a person merges.

Amendments: took the write exception (St), moved to item 4; took the variable "unknown until chosen" (St), "never deleted or retagged" (J), the statement about ADR-0001 (J, St), what happens to a commit with no pull request (Sk), and the alternatives (Sc). The chair added the start point before the first version, because without one the first run would reach commits with no version label and fail.

## ADR grouping

Unchanged from `screening.md`: decisions 1 and 2 form ADR-0003, decision 3 forms ADR-0004, decisions 4 to 7 form ADR-0005, and decisions 8 and 9 form ADR-0006.

## Held for the user

None of these is in the wording above. Each registers only if the user agrees.

- **Held law, suppressions (Sk).** Proposed wording: "Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and turns off a check only in `pyproject.toml`."
- **Decision 8, a `none` label (Sk).** Proposed wording: "The pull request carries exactly one of the labels `major`, `minor`, `patch`, and `none`. The label picks the version, and `none` releases nothing." Decision 9 would then skip a commit labelled `none`.
- **Decision 8, `major` below 1.0.0 (J).** Proposed added sentence: "While the latest version is below 1.0.0, the label check refuses `major` unless the owner's repository variable allows it." This stops at merge time what decision 9 now stops at release time.

## Notes for the chair

- Moving the staged required checks into `engineering-standards.md` makes that doc's count and summary untrue, so the change that registers this matter updates it (LAW-000008).
