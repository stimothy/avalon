# Final: tooling and delivery

Chair: stand-in. The chair did not propose this matter. Status: adopted after round 2, with no round 3. The nine decisions are recorded in ADR-0003 to ADR-0006, and their ledger rows are written. The held law is not registered: the table reworded the user's proposal, so it waits for the user (see `outcome.md`), and its ledger row is pending.

Items keep the numbers in `screening.md`. The final wording below is the wording of `revision-1.md` with the round 2 amendments in `votes-2.md` taken. Each amendment fixes wording so that a check can be made, and none changes what a decision chooses. The tallies are the round 2 tallies in `votes-2.md`.

## Chair's ruling

- No round 3. Every item passed round 2 with no reject, and every round 2 amendment is a wording fix that the chair takes.
- Decision 5 returns to the user's own wording in `proposal.md`, exactly. The `pr.yml` events and the cancelling of a newer run that is not a push move to decision 6 (J).
- The table approved the held law as worded in `revision-1.md`. That wording differs from the user's, so it registers only when the user accepts it. Its suppressions amendment stays under "Held for the user" and is not registered.
- No ADR states "No suite may reach the network", because the eval suite reaches a model (J). The contradiction on the GitHub lookup is settled by decision 3's transport port instead.
- Each suite's coverage collection excludes the evals (J). Decision 1 says so.

## The decisions

### 1. The development tools

- **Origin:** agent
- **Target ADR:** ADR-0003, development tools
- **Tally (round 2):** 5 approve, 0 amend, 0 reject

`pytest` runs tests, `coverage` measures them, `ruff` lints and checks the format, and `mypy` checks types. Their configuration lives in the single `pyproject.toml` at the repo root. A virtual environment named `.venv`, which git ignores, holds them. Coverage is line coverage over the Python that LAW-000014 measures. Each suite's gate job collects coverage data, except the eval job, which collects none. One job combines the data from every other suite. The unit run is timed against its budget with coverage on.

Rejected alternatives:

- Separate linter and formatter tools, such as black and flake8.
- Another type checker, such as pyright.
- No type checker.
- unittest in place of pytest.
- One config file for each tool.
- Coverage from the unit and integration runs only.

### 2. The lock file is the only home of a tool version

- **Origin:** agent
- **Target ADR:** ADR-0003, development tools
- **Tally (round 2):** 5 approve, 0 amend, 0 reject

The development tools are declared in `pyproject.toml`, and `uv` locks their versions in `uv.lock`. No ADR, doc, or workflow states the version of a tool that `uv.lock` locks. Workflows install the tools only from the lock file, and the workflow gate of decision 4 fails a workflow that installs a locked tool any other way. A reviewer checks the ADRs and docs.

Rejected alternatives:

- Pin versions in each workflow.
- pip with a requirements file.
- pip-tools.
- poetry.
- pdm.
- No lock.

### Held law: the code passes its checks

- **Origin:** user
- **Target:** LAW-000016, in `docs/laws/LAWS.md`
- **Tally (round 2):** 5 approve, 0 amend, 0 reject

| Scope | Law | Check |
|---|---|---|
| code | Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding. | Gates run each tool. |

Rejected alternatives:

- A law with no ADR reference (St, round 1). The reference keeps tool names out of the law, as the user's wording does.

### 3. Each suite has a folder and a fixed reach

- **Origin:** agent
- **Target ADR:** ADR-0004, test suites
- **Tally (round 2):** 4 approve, 1 amend, 0 reject

A test's folder sets its suite. Each suite may reach only what this table allows.

| Suite | May reach |
|---|---|
| Unit | One unit, with every port faked. |
| Integration | The real file system in a temporary folder, with git and GitHub faked. |
| End-to-end | The whole command line and the hook, in process, on a temporary folder, with git and GitHub faked. |
| Contract | Real git, in a throwaway repo. |
| Eval | Claude Code, a model, and a copy of a fixture. |

The contract suite runs each git fake and its real adapter through the same cases. The release code reaches GitHub only through a port. The real GitHub adapter takes its HTTP transport as a port, and every suite fakes that transport, so no suite reaches GitHub and the adapter's lines run under test. Each suite is its own gate job.

Rejected alternatives:

- One suite with markers.
- No contract suite, with the git fakes trusted.
- Real git in the integration suite.
- The contract suite on a schedule, not on each pull request.

### 4. Workflows hold no logic

- **Origin:** agent
- **Target ADR:** ADR-0005, workflows and gates
- **Tally (round 2):** 3 approve, 2 amend, 0 reject

A workflow file sets triggers, permissions, and steps that call a command. Anything that computes or branches is Python under `devtools/`, written to the same standards and tested in the same suites. A job's `if:` takes only these forms, alone or joined by `&&`:

- the pull request is not a draft;
- a true or false output that a `devtools/` command computed in an earlier job;
- `always()`, on the final job of `gates.yml` only.

Every action is pinned to a full commit SHA, and a pin changes only by a pull request. Every workflow states its permissions. Only the job in `release.yml` may write, and only tags and releases.

A gate reads every workflow and fails on any of these:

- an `if:` of any form not in the list above;
- an action not pinned to a full commit SHA;
- a workflow that does not state its permissions;
- a write permission outside the job in `release.yml`;
- a locked tool installed any way but from the lock file.

Rejected alternatives:

- Logic in shell steps inside workflows.
- Third-party actions that hold the logic.
- The list of allowed `if:` forms kept in `devtools/`, not in the ADR.

### 5. Gates run only on a pull request that is ready for review

- **Origin:** user
- **Target ADR:** ADR-0005, workflows and gates
- **Tally (round 2):** 4 approve, 1 amend, 0 reject

The gates run on a pull request into `master` when it is opened, reopened, given new commits, or marked ready for review. A draft runs no job. A newer push cancels the older run. No gate runs on `master` itself, and no workflow uses `pull_request_target`.

Rejected alternatives:

- Gates on every push.
- Gates on drafts too.
- Gates on `master` after the merge.

### 6. Two workflows gate a pull request, and one job gives the verdict

- **Origin:** agent
- **Target ADR:** ADR-0005, workflows and gates
- **Tally (round 2):** 5 approve, 0 amend, 0 reject

`gates.yml` holds the checks of the code and the docs. `pr.yml` holds the checks of the pull request itself: its version label, and the scan of its title and body. `pr.yml` also runs when the title, body, or labels change, because it checks them. A newer run of a workflow on the same pull request cancels the older run, whatever event started it. The final job of `gates.yml` fails unless every other job succeeded or was skipped by its own `if:`. A gate that applies to some changes is a job with an `if:`, not a workflow with a path filter.

Rejected alternatives:

- One workflow.
- A workflow for each check.
- Path filters on workflows.
- The ruleset requires each job by name.

### 7. A ruleset protects `master`

- **Origin:** agent
- **Target ADR:** ADR-0005, workflows and gates
- **Tally (round 2):** 4 approve, 1 amend, 0 reject

A ruleset on `master` requires a pull request, the final job of `gates.yml`, the label check and the title-and-body scan of `pr.yml`, and a branch that is up to date. It allows squash merges only, and the squash message is the pull request's title and description. It has no bypass actors, the owner included. The owner sets it by hand in the repository settings, and no gate checks it.

Rejected alternatives:

- No ruleset, relying on review.
- Classic branch protection.
- Merge commits or rebase merges.
- The default squash message.
- No up-to-date requirement.

### 8. A release is chosen by a label

- **Origin:** user
- **Target ADR:** ADR-0006, releases
- **Tally (round 2):** 5 approve, 0 amend, 0 reject

A merge into `master` releases the next version. The pull request carries exactly one of the labels `major`, `minor`, and `patch`, and the label picks the version. A pull request with no single version label cannot merge.

Rejected alternatives:

- The version comes from commit messages, such as Conventional Commits.
- A tool that reads commit messages, such as release-please or semantic-release.
- A version file edited in the pull request.
- A person tags by hand.
- A release only when asked.

### 9. One workflow releases, catches up, and writes nothing else

- **Origin:** agent
- **Target ADR:** ADR-0006, releases
- **Tally (round 2):** 3 approve, 2 amend, 0 reject

`release.yml` is the only workflow that runs on a push to `master`. Each run releases every commit newer than the latest version, oldest first, each by the label of its merged pull request. Before the first version exists, the run starts at the commit that added `release.yml`. One call makes a version: it creates the tag and the release with its notes. The workflow never pushes a commit, and a repeated run creates no version that already exists.

While no version exists or the latest version is below 1.0.0, the release code refuses `major` unless a repository variable that only the owner sets allows it. The variable's name is unknown until it is chosen. A commit that has no merged pull request with exactly one version label, or that is refused, fails the run. The run releases nothing at or after that commit until the label or the variable is changed and the run is repeated.

A bad release is never deleted or retagged. A pull request that reverts it makes the next version. The release code lives under `devtools/`, outside `plugin/**`, so ADR-0001's rule that no script command tags does not reach it.

Rejected alternatives:

- Release only the newest commit.
- The workflow commits a version file.
- No limit on `major` below 1.0.0.
- Release on a schedule.
- A release pull request that a person merges.

## ADR grouping

| ADR | Decisions |
|---|---|
| ADR-0003: Development tools | 1, 2 |
| ADR-0004: Test suites | 3 |
| ADR-0005: Workflows and gates | 4, 5, 6, 7 |
| ADR-0006: Releases | 8, 9 |

## Sorted out for design docs

- **Required checks come on in stages.** A job becomes a required check once the pull request that adds its workflow has merged. It fails the ADR test, so it becomes a guideline in `docs/design/engineering-standards.md`. That change makes the doc's count and summary untrue, so the same change updates them (LAW-000008).

## Held for the user

None of these is adopted or registered. Each registers only if the user agrees.

- **Held law, suppressions (Sk).** Proposed wording: "Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and turns off a check only in `pyproject.toml`."
- **Decision 8, a `none` label (Sk).** Proposed wording: "The pull request carries exactly one of the labels `major`, `minor`, `patch`, and `none`. The label picks the version, and `none` releases nothing." Decision 9 would then skip a commit labelled `none`.
- **Decision 8, `major` below 1.0.0 (J).** Proposed added sentence: "While the latest version is below 1.0.0, the label check refuses `major` unless the owner's repository variable allows it." This stops at merge time what decision 9 stops at release time.

## Ledger rows to add

Each row is in the format of `docs/laws/ledger.md`. Dissent gives the reason of each seat whose round 2 vote was amend. The chair took every such amendment into the final wording.

| Date | Decision | Proposed by | Decided by | Rounds | Tally | Dissent |
|---|---|---|---|---|---|---|
| 2026-11-12 | Added LAW-000016 (pending: written only after the user accepts the table's wording) | user | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0003: pytest, coverage, ruff, and mypy, configured in one pyproject.toml | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0003: the lock file is the only home of a tool version | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0004: each suite has a folder and a fixed reach | agent | table | 2 | 4 approve, 1 amend, 0 reject | St: the GitHub adapter takes its HTTP transport as a port that every suite fakes, so its lines run under test |
| 2026-11-12 | Adopted ADR-0005: workflows hold no logic | agent | table | 2 | 3 approve, 2 amend, 0 reject | Sk, J: the gate must name every failure it checks: `if:` forms, SHA pins, permissions, writes, and lock-file installs |
| 2026-11-12 | Adopted ADR-0005: gates run only on a pull request that is ready for review | user | table | 2 | 4 approve, 1 amend, 0 reject | J: keep the user's wording; move the pr.yml events and the newer-run cancel to decision 6 |
| 2026-11-12 | Adopted ADR-0005: two workflows gate a pull request, and one job gives the verdict | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0005: a ruleset protects master | agent | table | 2 | 4 approve, 1 amend, 0 reject | J: require the title-and-body scan of pr.yml as well as the label check |
| 2026-11-12 | Adopted ADR-0006: a release is chosen by a label | user | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0006: one workflow releases, catches up, and writes nothing else | agent | table | 2 | 3 approve, 2 amend, 0 reject | Sk, J: cover the case of no version yet, and say a repeated run creates no version that already exists |
