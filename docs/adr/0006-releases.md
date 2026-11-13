---
adr: 0006
summary: A merge into master releases the next version chosen by the pull request's label, unless the label is none, and one workflow releases every newer commit not labelled none and writes nothing else.
covers: [.github/workflows/release.yml, .github/workflows/pr.yml, devtools/**]
origin: user
---
# ADR-0006: Releases

## Context

This repo is released from `master`. A version needs a rule for who chooses it and what creates it. The release code lives under `devtools/`, outside `plugin/**`, so the rule of ADR-0001 that no script command tags does not reach it.

The primary technologies are:

- GitHub pull request labels
- GitHub tags and releases
- a GitHub Actions workflow, `release.yml`

The reason for each choice below is unknown, except where the text gives one. The decision on the label (the first heading) came from the user. The other came from the agent, except the skip of a commit labelled `none` and the label check's refusal of `major`, which came from the user.

## Decision

### A release is chosen by a label

A merge into `master` releases the next version, unless its pull request is labelled `none`. The pull request carries exactly one of the labels `major`, `minor`, `patch`, and `none`. The label picks the version, and `none` releases nothing. A pull request that does not carry exactly one of these four labels cannot merge.

### One workflow releases, catches up, and writes nothing else

`release.yml` is the only workflow that runs on a push to `master`.

- Each run releases every commit newer than the latest version, oldest first, each by the label of its merged pull request, and skips a commit whose pull request is labelled `none`.
- Before the first version exists, the run starts at the commit that added `release.yml`.
- One call makes a version: it creates the tag and the release with its notes.
- The workflow never pushes a commit.
- A repeated run creates no version that already exists.

While no version exists or the latest version is below 1.0.0, the release code refuses `major` unless a repository variable that only the owner sets allows it. The variable's name is unknown until it is chosen. While no version exists or the latest version is below 1.0.0, the label check refuses `major` unless the owner's repository variable allows it.

A commit that has no merged pull request with exactly one of the four labels, or that is refused, fails the run. The run releases nothing at or after that commit until the label or the variable is changed and the run is repeated.

A bad release is never deleted or retagged. A pull request that reverts it makes the next version.

## Consequences

- A pull request that merges with the wrong label releases the wrong version, and the version stays.
- A failed commit blocks every later release until its label or the variable is fixed.
- The release code reaches GitHub only through a port (ADR-0004).
- Only the job in `release.yml` writes, and only tags and releases (ADR-0005).
- A pull request labelled `none` makes no version, so its changes ship in the next version that is made.
- Nothing stops `none` on a change to `plugin/**`, so such a change ships in the next version, not its own.
- The release code keeps its own refusal of `major`, because a label can change after the merge, when no check can stop the merge.
- The label check and the release code call one shared function under `devtools/` to decide the refusal of `major`.
- The label check reads the latest version and the variable through the same GitHub port as the release code (ADR-0004).

## Alternatives rejected

- **Rejected: the version comes from commit messages, such as Conventional Commits.** The reason is unknown.
- **Rejected: a tool that reads commit messages, such as release-please or semantic-release.** The reason is unknown.
- **Rejected: a version file edited in the pull request.** The reason is unknown.
- **Rejected: a person tags by hand.** The reason is unknown.
- **Rejected: a release only when asked.** The reason is unknown.
- **Rejected: release only the newest commit.** The reason is unknown.
- **Rejected: the workflow commits a version file.** The reason is unknown.
- **Rejected: no limit on `major` below 1.0.0.** The reason is unknown.
- **Rejected: release on a schedule.** The reason is unknown.
- **Rejected: a release pull request that a person merges.** The reason is unknown.
- **Rejected: every merge releases.** The reason given is that a documentation-only or workflow-only change would still use up a version.
- **Rejected: a release is skipped by the paths a pull request changes.** The reason is unknown.
- **Rejected: a skip marker in the pull request's title.** The reason is unknown.
- **Rejected: the refusal of `major` only in the release workflow.** The reason given is that a `major` pull request could merge and have its release refused after the merge.

## Changelog

- 2026-11-12 (agent, table): Created. Recorded the label that picks a version and the one workflow that releases every commit newer than the latest version.
- 2026-11-12 (user): Confirmed the decisions of this ADR.
- 2026-11-12 (user, table): Amended. A pull request labelled `none` releases nothing, and the release workflow skips its commit.
- 2026-11-12 (user, table): Amended. The label check refuses `major` below 1.0.0 unless the owner's variable allows it, and the release code keeps its own refusal.
