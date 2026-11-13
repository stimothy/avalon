# Decision matter: tooling and delivery

Kind: decision matter, one slate, plus one held law. Proposer: the user for the calls the user stated, the planning work for the rest. Status: proposed; nothing is registered.

The chair first applies the ADR test to each decision: costly to reverse, and real alternatives that a later reader would ask about. A call that fails becomes a guideline in `docs/design/engineering-standards.md`. A call that an ADR already owns extends that ADR. Each decision has its own vote.

## The decisions

### 1. Five suites, each with a fixed reach (origin: agent)

Every test sits in one of five suites, and its folder sets the suite.

| Suite | May reach |
|---|---|
| Unit | One unit, with every port faked. |
| Integration | The real file system in a temporary folder, with git faked. |
| End-to-end | The whole command line and the hook, in process, on a temporary folder, with git faked. |
| Contract | Real git, in a throwaway repo. |
| Plugin evals | Claude Code, a model, and a copy of a fixture. |

One shared guard makes any process start and any network connection fail in the first three suites. The contract suite runs each git fake and its real adapter through the same cases. Each suite runs separately and is its own gate job. The unit run has a wall-clock budget.

Alternative: one suite with markers. Alternative: no contract suite, with the git fakes trusted. Alternative: real git in the integration suite.

### 2. The development tools (origin: agent)

`pytest` runs tests, `coverage` measures them, `ruff` lints and formats, and `mypy` checks types. Their configuration lives in the single `pyproject.toml` at the repo root. A virtual environment that git ignores holds them. Coverage is line coverage, measured once from the unit and integration runs together. The git adapters are left out of the measure, because the contract suite proves them.

Alternative: separate linter and formatter tools. Alternative: no type checker. Alternative: one config file for each tool.

### 3. The lock file is the only home of a tool version (origin: agent)

The development tools are declared in `pyproject.toml` and their versions are locked in `uv.lock`, which `uv` manages. No ADR, doc, or workflow states a tool version. Nothing under the plugin folder needs a development tool.

Alternative: pin versions in each workflow. Alternative: pip with a requirements file. Alternative: no lock.

### 4. Workflows hold no logic (origin: agent)

A workflow file sets triggers, permissions, and steps that call a command. Anything that computes or branches is Python under `devtools/`, written to the same standards and tested in the same suites. A job's `if:` takes only a few fixed forms, and a gate reads every workflow and fails on any other. Every action is pinned to a full commit SHA. Every workflow states its permissions, and only the release job may write.

Alternative: logic in shell steps inside workflows. Alternative: third-party actions that hold the logic.

### 5. Gates run only on a pull request that is ready for review (origin: user)

The gates run on a pull request into `master` when it is opened, reopened, given new commits, or marked ready for review. A draft runs no job. A newer push cancels the older run. No gate runs on `master` itself, and no workflow uses `pull_request_target`.

Alternative: gates on every push. Alternative: gates on drafts too. Alternative: gates on `master` after the merge.

### 6. Two workflows gate a pull request, and one job gives the verdict (origin: agent)

`gates.yml` holds the checks of the code and the docs. `pr.yml` holds the checks of the pull request itself: its version label, and the scan of its title and body. The final job of `gates.yml` fails unless every other job succeeded or was skipped because the change did not touch what the job covers. A gate that applies to some changes is a job with a condition, not a workflow with a path filter.

Alternative: one workflow. Alternative: a workflow for each check. Alternative: path filters on workflows.

### 7. A ruleset protects `master` (origin: agent)

A ruleset on `master` requires a pull request, the final job, the label check, and a branch that is up to date. It allows squash merges only, and the squash message is the pull request's title and description. So each pull request is one commit on `master`, with a message the gate has scanned. The ruleset comes on in stages: a job becomes a required check once the pull request that adds its workflow has merged.

Alternative: no ruleset, relying on review. Alternative: merge commits or rebase merges. Alternative: no up-to-date requirement.

### 8. A release is chosen by a label (origin: user)

A merge into `master` releases the next version. The pull request carries exactly one of the labels `major`, `minor`, and `patch`, and the label picks the version. A pull request with no single version label cannot merge.

Alternative: the version comes from commit messages. Alternative: a person tags by hand. Alternative: a release only when asked.

### 9. One workflow releases, catches up, and writes nothing else (origin: agent)

`release.yml` is the only workflow that runs on a push to `master`. Each run releases every commit newer than the latest version, oldest first, each by the label of its merged pull request. A version is made in one call that creates the tag and the release with its notes. The workflow never pushes a commit, and a run is safe to repeat. While the latest version is below 1.0.0, the release code refuses `major` unless a repository variable that only the owner sets allows it. A bad release is undone by a pull request that reverts it.

Alternative: release only the newest commit. Alternative: the workflow commits a version file. Alternative: no limit on `major` below 1.0.0.

## Held law (origin: user)

| Scope | Proposed law | Check |
|---|---|---|
| code | Python this repo authors passes the repo's linter, formatter, and type checker, which the tool-choice ADR names. | Gates run each tool. |

The Story 1.4 sitting voted 5 approve, 0 amend, 0 reject on it and held it only because the ADR it names did not exist. It goes to this table in the same sitting, after the tool-choice decision. This repo authors every git-tracked path except the plan folders and `.claude/`.

## Left for later

markdownlint is a docs-scope proposal for a later sitting.
