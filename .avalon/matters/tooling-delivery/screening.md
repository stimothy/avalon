# Screening: tooling and delivery

Chair: stand-in. The chair did not propose this matter. Status: screened; nothing is registered.

Each call was put to the ADR test (costly to reverse, and real alternatives that a later reader would ask about) and checked against ADR-0001, ADR-0002, and LAW-000001 to LAW-000015. Nine decisions pass. They are numbered in the order the seats hear them. The held law is heard after decision 2. Each decision has its own vote.

## Reported to the table

- **LAW-000014.** The proposal left the git adapters out of the coverage measure. LAW-000014 measures all the Python this repo authors, with only tests excluded, so the exclusion narrows the law. The chair struck it from decision 1. To keep it, the law must be amended through a round table (LAW-000003).
- **ADR-0001, no tags.** ADR-0001 says no agent and no script command tags. Decision 9 tags from a workflow, through code under `devtools/`. That code is not the plugin's script, and ADR-0001 covers only `plugin/**`, so the chair finds no contradiction. ADR-0006 states that its release code sits outside the plugin's script.
- **LAW-000011 to LAW-000013.** The proposal's suite decision restated these laws: suites run separately, a guard blocks processes and the network, and the unit run has a time budget. The chair removed those parts from decision 3, because the laws already state them.

## The decisions

### 1. The development tools (origin: agent, ADR-0003)

`pytest` runs tests, `coverage` measures them, `ruff` lints and formats, and `mypy` checks types. Their configuration lives in the single `pyproject.toml` at the repo root. A virtual environment that git ignores holds them. Coverage is line coverage, measured once from the unit and integration runs together.

Alternative: separate linter and formatter tools. Alternative: no type checker. Alternative: one config file for each tool.

### 2. The lock file is the only home of a tool version (origin: agent, ADR-0003)

The development tools are declared in `pyproject.toml`, and `uv` locks their versions in `uv.lock`. No ADR, doc, or workflow states a tool version. Nothing under the plugin folder needs a development tool.

Alternative: pin versions in each workflow. Alternative: pip with a requirements file. Alternative: no lock.

### Held law (origin: user), heard here

| Scope | Proposed law | Check |
|---|---|---|
| code | Python this repo authors passes the repo's linter, formatter, and type checker, which the tool-choice ADR names. | Gates run each tool. |

The tool-choice ADR is ADR-0003. If decision 1 fails, the law stays held.

### 3. Each suite has a folder and a fixed reach (origin: agent, ADR-0004)

A test's folder sets its suite. Each suite may reach only what this table allows.

| Suite | May reach |
|---|---|
| Unit | One unit, with every port faked. |
| Integration | The real file system in a temporary folder, with git faked. |
| End-to-end | The whole command line and the hook, in process, on a temporary folder, with git faked. |
| Contract | Real git, in a throwaway repo. |
| Plugin evals | Claude Code, a model, and a copy of a fixture. |

The contract suite runs each git fake and its real adapter through the same cases. Each suite is its own gate job.

Alternative: one suite with markers. Alternative: no contract suite, with the git fakes trusted. Alternative: real git in the integration suite.

### 4. Workflows hold no logic (origin: agent, ADR-0005)

A workflow file sets triggers, permissions, and steps that call a command. Anything that computes or branches is Python under `devtools/`, written to the same standards and tested in the same suites. A job's `if:` takes only a few fixed forms, and a gate reads every workflow and fails on any other. Every action is pinned to a full commit SHA. Every workflow states its permissions, and only the release job may write.

Alternative: logic in shell steps inside workflows. Alternative: third-party actions that hold the logic.

### 5. Gates run only on a pull request that is ready for review (origin: user, ADR-0005)

The gates run on a pull request into `master` when it is opened, reopened, given new commits, or marked ready for review. A draft runs no job. A newer push cancels the older run. No gate runs on `master` itself, and no workflow uses `pull_request_target`.

Alternative: gates on every push. Alternative: gates on drafts too. Alternative: gates on `master` after the merge.

### 6. Two workflows gate a pull request, and one job gives the verdict (origin: agent, ADR-0005)

`gates.yml` holds the checks of the code and the docs. `pr.yml` holds the checks of the pull request itself: its version label, and the scan of its title and body. The final job of `gates.yml` fails unless every other job succeeded or was skipped because the change did not touch what the job covers. A gate that applies to some changes is a job with a condition, not a workflow with a path filter.

Alternative: one workflow. Alternative: a workflow for each check. Alternative: path filters on workflows.

### 7. A ruleset protects `master` (origin: agent, ADR-0005)

A ruleset on `master` requires a pull request, the final job, the label check, and a branch that is up to date. It allows squash merges only, and the squash message is the pull request's title and description. So each pull request is one commit on `master`, with a message the gate has scanned.

Alternative: no ruleset, relying on review. Alternative: merge commits or rebase merges. Alternative: no up-to-date requirement.

### 8. A release is chosen by a label (origin: user, ADR-0006)

A merge into `master` releases the next version. The pull request carries exactly one of the labels `major`, `minor`, and `patch`, and the label picks the version. A pull request with no single version label cannot merge.

Alternative: the version comes from commit messages. Alternative: a person tags by hand. Alternative: a release only when asked.

### 9. One workflow releases, catches up, and writes nothing else (origin: agent, ADR-0006)

`release.yml` is the only workflow that runs on a push to `master`. Each run releases every commit newer than the latest version, oldest first, each by the label of its merged pull request. One call makes a version: it creates the tag and the release with its notes. The workflow never pushes a commit, and a run is safe to repeat. While the latest version is below 1.0.0, the release code refuses `major` unless a repository variable that only the owner sets allows it. A bad release is undone by a pull request that reverts it.

Alternative: release only the newest commit. Alternative: the workflow commits a version file. Alternative: no limit on `major` below 1.0.0.

## ADR grouping

No kept decision extends an existing ADR. ADR-0001 covers only `plugin/**`, and ADR-0002 covers only the documentation system.

| ADR | Decisions | Origin | Summary |
|---|---|---|---|
| ADR-0003: Development tools | 1, 2 | agent | pytest, coverage, ruff, and mypy, configured in one `pyproject.toml`, with versions only in the `uv` lock file. |
| ADR-0004: Test suites | 3 | agent | A test's folder sets its suite, each suite has a fixed reach, and a contract suite runs the git fakes and the real adapter through the same cases. |
| ADR-0005: Workflows and gates | 4, 5, 6, 7 | agent (mixed) | Workflows that hold no logic gate a pull request that is ready for review, one job gives the verdict, and a ruleset allows only squash merges into `master`. |
| ADR-0006: Releases | 8, 9 | agent (mixed) | A version label on the pull request picks the release, and one workflow tags, catches up, and pushes no commit. |

## Failed calls

- **Required checks come on in stages** (from proposal decision 7). A job becomes a required check once the pull request that adds its workflow has merged. The step is cheap to reverse and has no real alternative, so it fails the ADR test. It becomes a guideline in `docs/design/engineering-standards.md`.
- **Suite rules the laws already state** (from proposal decision 1): suites run separately, a guard blocks processes and the network in the first three suites, and the unit run has a time budget. They fail the duplicate check against LAW-000011, LAW-000012, and LAW-000013. They are removed, not made guidelines.
- **Git adapters left out of coverage** (from proposal decision 2). The clause narrows LAW-000014, so the chair struck it. It is reported above.
