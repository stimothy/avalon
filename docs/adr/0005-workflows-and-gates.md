---
adr: 0005
summary: Workflows hold no logic, gates run only on a pull request that is ready for review, two workflows gate a pull request with one job giving the verdict, gitleaks does the secret scan, and a ruleset protects master.
covers: [.github/workflows/**, devtools/**]
origin: user
---
# ADR-0005: Workflows and gates

## Context

This repo checks its code and docs with gates that run in GitHub workflows. A workflow is hard to test, so logic placed in one is hard to check. The Python under `devtools/` is held to the same standards and suites as the rest of the repo (ADR-0004).

The primary technologies are:

- GitHub Actions workflows
- a GitHub ruleset on `master`
- Python under `devtools/`
- gitleaks, which scans for secrets

The reason for each choice below is unknown, except where the text gives one. The decision on when gates run (the second heading) came from the user. The choice of `gitleaks` for the secret scan also came from the user. The others came from the agent.

## Decision

### Workflows hold no logic

A workflow file sets triggers, permissions, and steps that call a command. Anything that computes or branches is Python under `devtools/`, written to the same standards and tested in the same suites.

A job's `if:` takes only these forms, alone or joined by `&&`:

- the pull request is not a draft;
- a true or false output that a `devtools/` command computed in an earlier job;
- `always()`, on the final job of `gates.yml` only.

Every action is pinned to a full commit SHA, and a pin changes only by a pull request. Every workflow states its permissions. Only the job in `release.yml` may write, and only tags and releases.

A gate reads every workflow and fails on any of these:

- an `if:` of any form not in the list above;
- an action not pinned to a full commit SHA;
- a workflow that does not state its permissions;
- a write permission outside the job in `release.yml`;
- a locked tool installed any way but from the lock file;
- `gitleaks` installed any way but the two that the secret scan allows.

### Gates run only on a pull request that is ready for review

The gates run on a pull request into `master` when it is opened, reopened, given more commits, or marked ready for review. A draft runs no job. A newer push cancels the older run. No gate runs on `master` itself, and no workflow uses `pull_request_target`.

### Two workflows gate a pull request, and one job gives the verdict

- `gates.yml` holds the checks of the code and the docs.
- `pr.yml` holds the checks of the pull request itself: its version label, and the scan of its title and body.
- `pr.yml` also runs when the title, body, or labels change, because it checks them.
- A newer run of a workflow on the same pull request cancels the older run, whatever event started it.
- The final job of `gates.yml` fails unless every other job succeeded or was skipped by its own `if:`.
- A gate that applies to some changes is a job with an `if:`, not a workflow with a path filter.

### The secret scan is done by gitleaks

A gate in `gates.yml` scans the tracked files for a secret with `gitleaks`. The gate fails on a finding. Code under `devtools/` runs the tool through the one adapter that starts processes, and the unit tests replace that adapter with a fake.

- The gate scans only the files that git tracks.
- A developer and a workflow run the same gate command and the same version.
- The command fails with a clear message when `gitleaks` is missing.

`uv.lock` cannot lock `gitleaks`, because it is not a Python package. Its version lives in exactly one file under `devtools/`. That file's name is unknown until the workflow is written. No other ADR, doc, or workflow states the version.

A workflow installs `gitleaks` in one of two ways:

- a `devtools/` command that reads the version file and checks the checksum;
- an action pinned to a full commit SHA.

### A ruleset protects `master`

- A ruleset on `master` requires a pull request, the final job of `gates.yml`, the label check and the title-and-body scan of `pr.yml`, and a branch that is up to date.
- It allows squash merges only, and the squash message is the pull request's title, with no body.
- It has no bypass actors, the owner included.
- The owner sets it by hand in the repository settings, and no gate checks it.

## Consequences

- A rule about a workflow is checked by a gate, so a change to the allowed `if:` forms is a change to this ADR.
- The final job joins `always()` with the draft test, so a draft runs no job, the final job included.
- A pin to a commit SHA changes only by a pull request.
- The ruleset is set by hand and no gate checks it, so a drift in the settings goes unseen until someone looks.
- With no bypass actors, the owner cannot merge past a failing gate.
- The squash commit holds only the title, so the pull request's description is not in git history. `pr.yml` still scans the body, and the reason for that is unknown.
- The release workflow of ADR-0006 is the only workflow that runs on a push to `master`.
- GitHub's own secret scanning cannot fail a local run, so the scan is a gate.
- The version of `gitleaks` changes in its one file under `devtools/` and nowhere else.
- The check that no doc states the version of `gitleaks` is a reviewer's judgment.

## Alternatives rejected

- **Rejected: logic in shell steps inside workflows.** The reason is unknown.
- **Rejected: third-party actions that hold the logic.** The reason is unknown.
- **Rejected: the list of allowed `if:` forms kept in `devtools/`, not in the ADR.** The reason is unknown.
- **Rejected: gates on every push.** The reason is unknown.
- **Rejected: gates on drafts too.** The reason is unknown.
- **Rejected: gates on `master` after the merge.** The reason is unknown.
- **Rejected: one workflow.** The reason is unknown.
- **Rejected: a workflow for each check.** The reason is unknown.
- **Rejected: path filters on workflows.** The reason is unknown.
- **Rejected: the ruleset requires each job by name.** The reason is unknown.
- **Rejected: no ruleset, relying on review.** The reason is unknown.
- **Rejected: classic branch protection.** The reason is unknown.
- **Rejected: merge commits or rebase merges.** The reason is unknown.
- **Rejected: the default squash message.** The reason is unknown.
- **Rejected: the pull request's title and description as the squash message.** The reason is unknown.
- **Rejected: no up-to-date requirement.** The reason is unknown.
- **Rejected: trufflehog.** The reason is unknown.
- **Rejected: detect-secrets.** The reason is unknown.
- **Rejected: a pattern scan written under `devtools/`.** The reason given is that this repo would maintain its own rules.
- **Rejected: GitHub's own secret scanning and push protection, with no gate.** The reason given is that it is not a gate and cannot fail a local run.

## Changelog

- 2026-11-12 (agent, table): Created. Recorded workflows with no logic, the pull-request trigger of the gates, the two gating workflows with one verdict job, and the ruleset on master.
- 2026-11-12 (user): Confirmed the decisions of this ADR.
- 2026-11-13 (user, table): Amended. The secret scan is done by gitleaks. Its version lives in one file under `devtools/`, and a workflow installs it only by a checksum check or a pinned action.
- 2026-11-13 (user, table): Amended. The squash message is the pull request's title alone, with no body.
