# Amendment matter: three amendments the user accepted

Kind: one slate of three amendments, one of a law and two of an ADR. Proposer: the user, who accepted each wording that a seat proposed at the previous sitting. Status: proposed; nothing is changed.

Each is the user's proposal. A table that would reword or reject one registers nothing until the user answers. An amendment of an ADR in effect always goes to a table.

## A. Amend LAW-000016: no finding is hidden by switching a check off

Current law: "Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding."

Proposed law: "Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and turns off a check only in `pyproject.toml`."

Check: gates run each tool, and a gate fails on a comment that turns a check off.

Reason given: without it, a comment such as `# type: ignore` can empty the law.

Alternative: leave the law as it is.

## B. Amend ADR-0006: a `none` label releases nothing

Current wording of the decision: "The pull request carries exactly one of the labels `major`, `minor`, and `patch`, and the label picks the version."

Proposed wording: "The pull request carries exactly one of the labels `major`, `minor`, `patch`, and `none`. The label picks the version, and `none` releases nothing." The release workflow then skips a commit whose pull request is labelled `none`.

Reason given: otherwise a documentation-only or workflow-only change must still use up a version.

Alternative: every merge releases, as now.

## C. Amend ADR-0006: the label check refuses `major` below 1.0.0

Proposed added sentence: "While no version exists or the latest version is below 1.0.0, the label check refuses `major` unless the owner's repository variable allows it."

Reason given: a `major` pull request can merge today, and the release workflow then refuses its release after the merge. The refusal moves to the merge.

Alternative: the refusal stays only in the release workflow, as now.
