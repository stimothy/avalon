# Screening: release amendments

Chair: stand-in. The chair did not propose this matter. Status: screened; nothing is registered.

The slate has three amendments: one of a law (A) and two of ADR-0006 (B, C). Each is the user's proposal. The chair checked each against LAW-000001 to LAW-000016, ADR-0001, ADR-0003 to ADR-0006, and the other two items. The user's wording is kept as given. Every sentence the chair wrote is marked **[chair, consequent]**. The table hears each item with its own vote.

If the table treats a chair consequent edit as a rewording of the user's proposal, that item registers nothing until the user answers.

## Issues found

- **A, length.** The proposed law is 182 characters. The limit in `.avalon.yml` (`law_max_chars`) is 200, so it holds.
- **A, ADR-0005.** ADR-0005's list of what a gate fails is a list of workflow rules ("A gate reads every workflow and fails on any of these"). A's check reads Python source, not workflows, so it is not added to that list. It is a job in `gates.yml`, which ADR-0005 already makes the home of code checks, and its logic sits under `devtools/`. A needs no edit to ADR-0005. The check column is not law text, so the table adds no gate rule beyond it.
- **A, reach of "a check".** The law names three tools: the format check, the linter, and the type checker. So "a check" covers comments such as `# noqa`, `# ruff: noqa`, `# fmt: off`, `# fmt: skip`, `# type: ignore`, and `# mypy:` inline settings. It does not cover `# pragma: no cover`, because coverage is not one of the three tools. The table should state this reading in its record, or the gate's scope is unknown.
- **A, files.** The law also bars a check turned off in any file but `pyproject.toml`, such as a `ruff.toml` or `mypy.ini`. The check catches only comments. ADR-0003 already puts all tool configuration in the one `pyproject.toml`, and a reviewer checks the rest. No conflict.
- **A, current code.** The repo has no Python that turns a check off, so adoption breaks nothing today.
- **A, mechanics.** An amendment creates LAW-000017 with the new text and moves LAW-000016 to `docs/laws/archive.md` with status amended and "Replaced by" LAW-000017. No doc under `docs/` names LAW-000016, so no other doc changes.
- **B, ADR-0006 decision 1.** Its first sentence, "A merge into `master` releases the next version", becomes untrue under `none`. Its last sentence, "no single version label", is unclear once `none` is a label that picks no version. The chair rewrote both (below).
- **B, ADR-0006 decision 2.** The user's proposal says the release workflow skips a `none` commit. Decision 2 says each run releases every newer commit, and a commit with no single version label fails the run. Both sentences must change, and the chair wrote them (below). Decision 2's origin is agent, so these are chair words for the user's stated intent.
- **B, catch-up.** A skipped `none` commit stays newer than the latest version. Each run passes over it again. The next released commit carries its changes, because a tag marks the whole history. This is a consequence, not a conflict.
- **B, plugin changes.** Nothing stops `none` on a change to `plugin/**`. Such a change ships in the next version, not its own. The proposal adds no limit, and the chair adds none.
- **B, the label itself.** The `none` label must exist in the repository. The owner creates it by hand. No gate checks it.
- **B, ADR-0005.** ADR-0005 names "its version label" and "the label check" of `pr.yml`. Neither names the three labels, so both stay true. No edit.
- **B, index and summary.** ADR-0006's `summary` key and its line in `docs/adr/README.md` say every merge releases. They change in the same change (LAW-000005, LAW-000008).
- **B and C, `covers`.** Both items change what the label check in `pr.yml` does. ADR-0006 covers only `release.yml` and `devtools/**`. The chair adds `.github/workflows/pr.yml`.
- **C, the backstop.** The reason says "The refusal moves to the merge". The added sentence removes nothing, and the alternative says "stays only in the release workflow", so the chair reads C as adding a refusal at the merge and keeping the release code's refusal. The backstop is needed for three cases:
  - a label changed after the merge, when no check runs, and the release reads the label at release time;
  - the owner's variable changed between the label check and the release;
  - a commit merged before the label check refused `major`.

  If the user meant to remove the release code's refusal, that is a different amendment, and C registers nothing until the user answers.
- **C, placement.** C's sentence says "the owner's repository variable", which refers back to the variable that decision 2 introduces. So it goes in decision 2, right after the release code's refusal. In decision 1 it would come before the variable is defined.
- **B and C together.** No conflict. `none` and the `major` refusal touch different labels.
- **ADR-0001.** ADR-0001 bars a script command that tags. ADR-0006's release code sits under `devtools/`, outside `plugin/**`. Neither B nor C moves it, so ADR-0001 is not reached.
- **Outside `docs/`.** The planning files outside the docs tree name three labels, for example Stories 1.12 and 1.13 in `epics.md`. They are not docs under these laws, but the stories need updating before they are built. The deferred item on the first release run, whose commit may carry no version label, may be met by labelling that pull request `none`.

## The slate

### A. Amend LAW-000016: no finding is hidden by switching a check off (origin: user)

Amends LAW-000016. Creates LAW-000017 and archives LAW-000016.

| ID | Scope | Origin | Law |
|---|---|---|---|
| LAW-000017 | code | user | Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and turns off a check only in `pyproject.toml`. |

Check: gates run each tool, and a gate fails on a comment that turns a check off.

Archive row: LAW-000016, amended, its current text, "Replaced by" LAW-000017.

Reason given: without it, a comment such as `# type: ignore` can empty the law.

Alternative: leave the law as it is.

### B. Amend ADR-0006: a `none` label releases nothing (origin: user)

Amends ADR-0006, decision "A release is chosen by a label". The final text of that decision:

> **[chair, consequent]** A merge into `master` releases the next version, unless its pull request is labelled `none`. The pull request carries exactly one of the labels `major`, `minor`, `patch`, and `none`. The label picks the version, and `none` releases nothing. **[chair, consequent]** A pull request that does not carry exactly one of these four labels cannot merge.

The middle two sentences are the user's.

Consequent edits to ADR-0006, decision "One workflow releases, catches up, and writes nothing else". Each replaces the sentence named.

- **[chair, consequent]** Replaces "Each run releases every commit newer than the latest version, oldest first, each by the label of its merged pull request." with:

  > Each run releases every commit newer than the latest version, oldest first, each by the label of its merged pull request, and skips a commit whose pull request is labelled `none`.

- **[chair, consequent]** Replaces "A commit that has no merged pull request with exactly one version label, or that is refused, fails the run." with:

  > A commit that has no merged pull request with exactly one of the four labels, or that is refused, fails the run.

Other consequent edits to ADR-0006:

- **[chair, consequent]** `summary` key: "A merge into master releases the next version chosen by the pull request's label, unless the label is none, and one workflow releases every newer commit not labelled none and writes nothing else."
- **[chair, consequent]** `covers` key: `[.github/workflows/release.yml, .github/workflows/pr.yml, devtools/**]`.
- **[chair, consequent]** Consequences, added: "A pull request labelled `none` makes no version, so its changes ship in the next version that is made."
- **[chair, consequent]** Alternatives rejected, added: "**Rejected: every merge releases.** The reason given is that a documentation-only or workflow-only change would still use up a version."
- **[chair, consequent]** The line for ADR-0006 in `docs/adr/README.md`: "A pull request's label picks the version or none, and one workflow releases every newer commit not labelled none."

Reason given: otherwise a documentation-only or workflow-only change must still use up a version.

Alternative: every merge releases, as now.

### C. Amend ADR-0006: the label check refuses `major` below 1.0.0 (origin: user)

Amends ADR-0006, decision "One workflow releases, catches up, and writes nothing else". The user's sentence is added right after the release code's refusal. The release code's refusal stays. The final text of that paragraph:

> While no version exists or the latest version is below 1.0.0, the release code refuses `major` unless a repository variable that only the owner sets allows it. The variable's name is unknown until it is chosen. While no version exists or the latest version is below 1.0.0, the label check refuses `major` unless the owner's repository variable allows it.

The first two sentences are unchanged. The third is the user's.

Other consequent edits to ADR-0006:

- **[chair, consequent]** Consequences, added: "The release code keeps its own refusal of `major`, because a label can change after the merge, when no check runs."
- **[chair, consequent]** Alternatives rejected, added: "**Rejected: the refusal of `major` only in the release workflow.** The reason given is that a `major` pull request could merge and have its release refused after the merge."
- `covers`: the same edit as in B.

Reason given: a `major` pull request can merge today, and the release workflow then refuses its release after the merge. The refusal moves to the merge.

Alternative: the refusal stays only in the release workflow, as now.

## On adoption

- Each adopted item gets its own ledger row: "Amended LAW-000016 as LAW-000017" for A, and "Amended ADR-0006: ..." for B and C.
- Each adopted ADR item gets a changelog line in ADR-0006 with date, marker, and a one-line summary.
- A rejected item gets a ledger row and changes nothing.
