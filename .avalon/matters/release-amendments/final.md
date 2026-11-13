# Final: release amendments

Chair: stand-in. The chair did not propose this matter. Status: decided in round 1 and applied.

The table decides with no round 2. Every amendment raised in round 1 either adds to the record or rewords the user's sentences.

- The chair takes each amendment that adds to the record and leaves the user's sentences as they are.
- The chair declines each amendment that rewords the user's law text or the user's added ADR sentence. Each is listed under "Held for the user", and the user may accept one.

A, B, and C are adopted with the user's wording exactly.

## 1. The decisions

### A. Amend LAW-000016 as LAW-000017 (origin: user)

Final text: "Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and turns off a check only in `pyproject.toml`."

Tally: 2 approve, 3 amend, 0 reject. Adopted with the detail file that states what "a check" covers.

### B. Amend ADR-0006: a `none` label releases nothing (origin: user)

Final text of the user's sentences: "The pull request carries exactly one of the labels `major`, `minor`, `patch`, and `none`. The label picks the version, and `none` releases nothing." The release workflow skips a commit whose pull request is labelled `none`.

Tally: 3 approve, 2 amend, 0 reject. Adopted with the Context sentence, two rejected alternatives, and a consequence on `plugin/**`.

### C. Amend ADR-0006: the label check refuses `major` below 1.0.0 (origin: user)

Final text: "While no version exists or the latest version is below 1.0.0, the label check refuses `major` unless the owner's repository variable allows it."

Tally: 2 approve, 3 amend, 0 reject. Adopted with the Jurist's wording on the merge, the shared function, and the GitHub port. The release code's refusal stays.

## 2. Replacement text

### `docs/laws/LAWS.md`

Replace the LAW-000016 row with this row:

```
| LAW-000017 | code | user | Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and turns off a check only in `pyproject.toml`. | [more](LAW-000017.md) |
```

### `docs/laws/LAW-000017.md` (new file)

````
---
law: LAW-000017
---
# Checks with no finding

A gate runs the format check, the linter, and the type checker on the authored Python. It fails on any finding.

A gate also fails on a comment in the authored Python that turns a check off. A check is a rule of one of these three tools, so these comments are covered:

- `# noqa`
- `# ruff: noqa`
- `# fmt: off`
- `# fmt: skip`
- `# type: ignore`
- `# mypy:` inline settings

`# pragma: no cover` is out of scope, because coverage is not one of the three tools.

A setting that turns a check off lives only in `pyproject.toml`. A file such as `ruff.toml` or `mypy.ini` that turns a check off breaks this law. A reviewer checks such files, because the gate reads only comments.
````

### `docs/laws/archive.md`

Add this row:

```
| LAW-000016 | Amended | Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding. | 2026-11-12 | LAW-000017 | LAW-000017 | A comment such as `# type: ignore` could empty the law, so the law bars turning off a check outside `pyproject.toml`. |
```

### `docs/adr/0006-releases.md`

`summary` key, replaced:

```
summary: A merge into master releases the next version chosen by the pull request's label, unless the label is none, and one workflow releases every newer commit not labelled none and writes nothing else.
```

`covers` key, replaced:

```
covers: [.github/workflows/release.yml, .github/workflows/pr.yml, devtools/**]
```

Context, the sentences "The decision on the label (the first heading) came from the user. The other came from the agent." replaced with:

> The decision on the label (the first heading) came from the user. The other came from the agent, except the skip of a commit labelled `none` and the label check's refusal of `major`, which came from the user.

Decision "A release is chosen by a label", full text:

> A merge into `master` releases the next version, unless its pull request is labelled `none`. The pull request carries exactly one of the labels `major`, `minor`, `patch`, and `none`. The label picks the version, and `none` releases nothing. A pull request that does not carry exactly one of these four labels cannot merge.

Decision "One workflow releases, catches up, and writes nothing else", full text:

> `release.yml` is the only workflow that runs on a push to `master`.
>
> - Each run releases every commit newer than the latest version, oldest first, each by the label of its merged pull request, and skips a commit whose pull request is labelled `none`.
> - Before the first version exists, the run starts at the commit that added `release.yml`.
> - One call makes a version: it creates the tag and the release with its notes.
> - The workflow never pushes a commit.
> - A repeated run creates no version that already exists.
>
> While no version exists or the latest version is below 1.0.0, the release code refuses `major` unless a repository variable that only the owner sets allows it. The variable's name is unknown until it is chosen. While no version exists or the latest version is below 1.0.0, the label check refuses `major` unless the owner's repository variable allows it.
>
> A commit that has no merged pull request with exactly one of the four labels, or that is refused, fails the run. The run releases nothing at or after that commit until the label or the variable is changed and the run is repeated.
>
> A bad release is never deleted or retagged. A pull request that reverts it makes the next version.

Consequences, lines added after the existing lines:

```
- A pull request labelled `none` makes no version, so its changes ship in the next version that is made.
- Nothing stops `none` on a change to `plugin/**`, so such a change ships in the next version, not its own.
- The release code keeps its own refusal of `major`, because a label can change after the merge, when no check can stop the merge.
- The label check and the release code call one shared function under `devtools/` to decide the refusal of `major`.
- The label check reads the latest version and the variable through the same GitHub port as the release code (ADR-0004).
```

Alternatives rejected, lines added after the existing lines:

```
- **Rejected: every merge releases.** The reason given is that a documentation-only or workflow-only change would still use up a version.
- **Rejected: a release is skipped by the paths a pull request changes.** The reason is unknown.
- **Rejected: a skip marker in the pull request's title.** The reason is unknown.
- **Rejected: the refusal of `major` only in the release workflow.** The reason given is that a `major` pull request could merge and have its release refused after the merge.
```

The Scout's third alternative, batching into a scheduled release, is already covered by the existing line "Rejected: release on a schedule". It gets no second line.

Changelog, lines added at the end:

```
- 2026-11-12 (user, table): Amended. A pull request labelled `none` releases nothing, and the release workflow skips its commit.
- 2026-11-12 (user, table): Amended. The label check refuses `major` below 1.0.0 unless the owner's variable allows it, and the release code keeps its own refusal.
```

### `docs/adr/README.md`

The line for ADR-0006, replaced:

```
- [0006-releases.md](0006-releases.md): A pull request's label picks the version or none, and one workflow releases every newer commit not labelled none.
```

## 3. Ledger rows

Add these rows to `docs/laws/ledger.md`:

```
| 2026-11-12 | Amended LAW-000016 as LAW-000017 | user | table | 1 | 2 approve, 3 amend, 0 reject | Sk, St, Sc: reword the law text (held for the user); all seats: state what "a check" covers, in a detail file |
| 2026-11-12 | Amended ADR-0006: a none label releases nothing | user | table | 1 | 3 approve, 2 amend, 0 reject | J: the Context must name the user's parts; Sc: add rejected alternatives, and say whether `none` may mark a change to `plugin/**` |
| 2026-11-12 | Amended ADR-0006: the label check refuses major below 1.0.0 | user | table | 1 | 2 approve, 3 amend, 0 reject | J: say no check can stop the merge, and ask the user to confirm the release code's refusal stays; St: one combined sentence (held for the user); Sc: use the same GitHub port |
```

## 4. Held for the user

Each of these rewords the user's accepted wording, so the table registers none of them. The user may accept one.

Rewordings of the law text of A:

- Skeptic: "Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and no comment in it turns a check off; tool settings that turn a check off live only in `pyproject.toml`."
- Steward: "Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and no check is turned off outside `pyproject.toml`."
- Scout: "Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and turns a check off only in `pyproject.toml`."

Rewording of the user's sentence in C:

- Steward: one combined sentence in place of the release code's refusal and the user's added sentence: "While no version exists or the latest version is below 1.0.0, the label check and the release code each refuse `major` unless a repository variable that only the owner sets allows it. The variable's name is unknown until it is chosen."

Decided by the user's delegation: the release code's refusal stays, as the screening read it. The user's sentence removes nothing, and a label or the variable can change after the merge.
