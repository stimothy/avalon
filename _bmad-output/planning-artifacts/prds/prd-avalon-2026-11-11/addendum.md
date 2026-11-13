---
title: Avalon PRD addendum
status: draft
created: 2026-11-11
updated: 2026-11-11
---

# Avalon PRD: addendum

This addendum holds material that supports `prd.md` and belongs to later work: where the detail and the rationale live, which FRs have an acceptance scenario, a short review of comparable tools, the reasoning behind the Python requirement, a starting point for the engineering standards, the gates, and the release workflow, and the changes that `SPEC.md` needs.
It restates no requirement and no rationale. `SPEC.md` is the one home for requirement detail, and `BRIEF.md` is the one home for the reasoning behind each choice.

## 1. Where the detail and the rationale live

Architecture and story work read `SPEC.md` for what each feature must do, and `BRIEF.md` for why and for the alternatives it rejected.

| PRD feature | `SPEC.md` sections | `BRIEF.md` sections |
|---|---|---|
| 4.1 The document model | 2 | 1, 2, 3 |
| 4.2 Laws | 3 | 4 |
| 4.3 The ledger | 3 | 4 |
| 4.4 The round table | 4, 14 | 4, 12 |
| 4.5 ADRs | 5 | 5 |
| 4.6 Design docs, the glossary, and indexes | 6, 7 | 6, 7 |
| 4.7 The writing standard | 8 | 8 |
| 4.8 Setup, layout, loading, and conflict handling | 9, 10, 11, 12 | 9, 10, 11, 12 |
| 4.9 Skills and supporting agents | 12, 13, 14 | 12 |
| 4.10 The script | 15 | 12 |
| 4.11 Building and proving Avalon in this repo | 16 | 12, 13 |
| 4.12 The public repo and its releases | None, apart from 12 for install | None |
| 4.13 How the Avalon repo is built: standards, gates, and releases | 16, for the placeholder standards | 13 |
| 4.14 Merges, upgrades, and CI in a target repo | 16, for build step 8 | 12 |

Features 4.12 and 4.13 follow from what the user said on 2026-11-11, which PRD section 13 records.
For 4.12 the user named the public repo, the MIT licence, and the common files, and the PRD reasoned the detail.
For 4.13 the user stated the standards, the gate rules, and the release rules, and the PRD marks each consequence it reasoned.
Feature 4.14 is the PRD's own answer to three points the sources leave undefined.
`SPEC.md` needs the requirements added (section 6 below).

Four more sections matter to a reader of the PRD:

- `SPEC.md` section 17 holds the 45 acceptance scenarios.
- `SPEC.md` section 18 lists every value and mechanism the brief does not settle. The PRD carries them as OQ-1 to OQ-22 and OQ-24, and PRD section 12 answers each one.
- `BRIEF.md` section 14 lists 14 places where the design departs from the original description, each with its reason.
- `BRIEF.md` section 15 lists what is settled, what is open, and which Claude Code behaviours were checked against the Claude Code docs.

## 2. Which FRs have an acceptance scenario, and what proves the rest

Of the 62 FRs, 26 cite at least one acceptance scenario on their Source line:
FR-2, FR-5, FR-6, FR-8, FR-10, FR-11, FR-13, FR-14, FR-17, FR-18, FR-19, FR-20, FR-21, FR-24, FR-25, FR-26, FR-28, FR-31, FR-32, FR-33, FR-34, FR-36, FR-43, FR-44, FR-45, and FR-46.

The other 36 cite none. PRD question OQ-30 asks what proves each, and this table answers it.

| Proof | FRs |
|---|---|
| Script tests: a format or a command that the script enforces | FR-7, FR-9, FR-12, FR-23, FR-27, FR-30, FR-42, FR-60, FR-61, FR-62 |
| A static check of the plugin's files, with no model | FR-41 |
| Plugin evals: scored cases of an agent's judgement | FR-1, FR-3, FR-4, FR-15, FR-16, FR-22, FR-29, FR-35, FR-37, FR-38, FR-39, FR-40 |
| A gate on every pull request | FR-53, FR-54, FR-55, FR-56 |
| Release gates SM-3, SM-11, and SM-12 | FR-48, FR-49, FR-50, FR-51 |
| A drill, run once and recorded in the pull request that adds the workflow | FR-52, FR-58, FR-59 |
| Review by a person | FR-47, FR-57 |

FR-17 and FR-19 cite a scenario, and they also turn on an agent's judgement, so scored cases cover them too.
The gate for FR-54 runs the script's tests on Python 3.9 and on the current release. A plugin scenario proves the message a user sees when Python is missing or too old, because the script cannot run there.
A scored case runs three times and passes when two runs pass.
Every case for FR-20, FR-21, and FR-35 must pass, because those three protect the user's final say. At least 80% of the other cases must pass on each fixture.

The drill for FR-58 and FR-59 walks one pull request through each rule: no run while it is a draft, a run when it is ready, a cancelled run on a second push, a failed label gate, and one release on merge.

## 3. Comparable tools

A web search on 2026-11-11 looked for tools that give a repo governed documentation for agents.
No page was fetched, so every point below comes from search results and none is verified from a primary source.
The review informs positioning and risk only. It is not evidence for any requirement.

| Category | Examples | What each lacks next to Avalon |
|---|---|---|
| ADR tooling | adr-tools, MADR, Log4brains | A template or a file numbering tool. No rule that an agent loads, and no gate on a change. |
| Agent instruction files | `AGENTS.md`, `CLAUDE.md`, Cursor rules, Copilot instructions | Advice with no change control and no record of why a rule exists. |
| Spec-driven systems | GitHub Spec Kit, Kiro, OpenSpec, BMad Method | A workflow for planned work. No governed process for amending a standing rule. |
| Multi-model deliberation | "LLM council" tools | They answer a question. They tie to no rule in a repo, keep no ledger, and give no human the final say. |

Three points from the review bear on the PRD:

- **Instruction bloat.** Several sources report that agents are more likely to ignore a rule as an instruction file grows. This supports the law test and the law budget (FR-3, FR-12).
- **Rules in context are advice.** Sources recommend moving enforcement into hooks or checks. Avalon checks structure by lint and compliance by the `law-reviewer`, and the PRD lists the gap between the two as a risk (PRD section 8).
- **Correlated reviewers.** Research on multi-agent debate reports that similar models make correlated errors and tend to converge on the majority view. `SPEC.md` places the removal of this correlation out of scope. The PRD adds a counter-metric on unanimous first rounds (SM-C2).

The search found no tool that combines a gated change to a rule, a ledger, and a lint.
That is an absence in a limited search, not a proven gap.

## 4. Why the shipped script uses no virtual environment

The user asked whether the script could run in a virtual environment, so that the Python version on a machine would matter less.
The PRD answers no for the shipped script and yes for the development tools (FR-54). This section gives the reasoning.

### What a virtual environment does

- It isolates installed packages. The shipped script uses the standard library only (REQ-265), so it has no package to isolate.
- It does not supply an interpreter. A virtual environment is created by a Python that is already on the machine, and it runs on that same version.
- It needs a setup step on every machine and a place to live. A plugin's own folder is replaced on every update.

So a virtual environment would add a setup step and would leave the two real questions open: whether the machine has Python 3, and which version.

### Options considered

| Option | What it settles | What it costs |
|---|---|---|
| The Python 3 already on the machine, with a stated floor | Nothing to install. One clear requirement. | The script must run on every version from the floor upward, and the checks must prove it. |
| A virtual environment | Nothing, while the script has no dependencies | A setup step, and a folder that must survive updates |
| A tool that downloads its own Python, such as `uv` | The version | A new dependency that every user must install first |
| A compiled binary for each platform | Python is not needed at all | A build and a release for each operating system, and the script stops being one readable file |

The PRD takes the first option.

### What would change the answer

The script would need a virtual environment if it took a third-party package.
The likeliest pull is a YAML parser, because the standard library has none (PRD question OQ-10).
`SPEC.md` suggests parsing a small subset instead, which keeps the script free of dependencies.
If that changes, the Claude Code docs name the place for a plugin's installed dependencies: the plugin data folder, which survives updates.

### The floor

The floor is Python 3.9. A check of vendor sources on 2026-11-11 found these default versions:

| System | Default `python3` |
|---|---|
| macOS developer tools, on macOS 26 | 3.9.6 |
| Debian 11 | 3.9 |
| RHEL 9 | 3.9 |
| Ubuntu 22.04 | 3.10 |
| Debian 12 | 3.11 |
| Ubuntu 24.04, RHEL 10 | 3.12 |
| Debian 13 | 3.13 |
| Ubuntu 26.04 | 3.14 |

The RHEL versions come from search results, and the rest from the vendors' own pages.
A floor above 3.9 would make every macOS user install another Python, which is the setup step that FR-54 rules out.
Python 3.9 reached its end of life in October 2025, so the floor is about what machines have and not about what Python supports.
Claude Code also runs on Ubuntu 20.04 and Debian 10, whose default Python is older. A user there installs a later Python.

GitHub's hosted runners can install 3.9 on Linux. They have no 3.9 build for the macOS runners, which use Apple silicon, so the macOS gate runs the script on the system Python that the developer tools provide. That is the interpreter a macOS user has.
The current release is Python 3.15.

### What the Claude Code docs say

A reader of the Claude Code docs on 2026-11-11 reported these points. Architecture verifies each one it builds on.

- Claude Code neither ships nor requires Python.
- Claude Code supports macOS 13 and later, Windows 10 and later, and current Ubuntu, Debian, and Alpine releases. On native Windows a hook runs in Git Bash, or in PowerShell when Git Bash is absent.
- A plugin manifest has `version`, `license`, `author`, `homepage`, `repository`, and `keywords` fields. It has no field for the lowest Claude Code version.
- A manifest that sets `version` keeps every user on the installed copy until the version changes.
- A marketplace is cloned from its default branch. Automatic update is off by default for a marketplace that is not an official one.
- A plugin whose source is the repo root is copied whole into a cache, and the docs name no way to leave a file out.
- A `PreToolUse` hook that times out does not block the tool call.
- A `PreToolUse` hook can return `ask`, which sends the tool call to a permission prompt. A prompt from a subagent reaches the user. The docs do not say what `ask` does in every permission mode, so an acceptance scenario must prove each one.
- The hook input names the permission mode and the agent type. Nothing tells a hook or a skill that a session is not interactive.
- A plugin in a subfolder of its marketplace repo is supported, and only that subfolder is copied. `claude plugin validate .` at the root checks the marketplace file and the plugin.
- Agent files in a subfolder of `agents` take the subfolder into their name.
- A plugin cannot ship permission rules.
- `claude plugin eval` runs in CI with a model credential and a cost limit.

## 5. The engineering standards, the gates, and the release workflow

The user stated the standards, the gate rules, and the release rules on 2026-11-11. PRD FR-55 to FR-59 hold them.
This section is a starting point for the work that follows. The proposals in it are the PRD's working answers, and the user reviews them in build step 1.

### A proposed kind and check for each standard

Build step 1 gives each standard exact wording, a kind, and a check (PRD question OQ-23).
The table applies the law test in PRD FR-3. A law needs a reviewer to be able to say whether any piece of work complies, so a standard that rests on taste is proposed as a guideline.

| Standard | Proposed kind | Proposed check |
|---|---|---|
| Test-driven development | Guideline | A reviewer. A finished change does not show which came first, the test or the code. |
| Arrange, Act, Assert | Law | The `law-reviewer`. `SPEC.md` uses this rule as its example of a `user` law. |
| Three kinds of test, with unit and integration tests run apart | A law for the rule, and an ADR for the layout | The gates run each kind as its own job. |
| A unit test mocks everything but its unit and runs fast | Law | A gate fails when the whole unit run takes longer than its budget, which defaults to 10 seconds. |
| No git and no network in a test | Law | A gate fails any unit, integration, or end-to-end test that opens a network connection or starts `git`. |
| 80% coverage | Law | A gate. |
| Linter, formatter, type checker | A law that code passes them, and an ADR for the choice of tools | Gates. |
| CPU time and memory are weighed, and each test earns its place | Guideline | A reviewer. |
| DRY and SOLID | Guideline | A reviewer. |
| No grab-bag directories | Law | The `law-reviewer`, with the definition in PRD FR-57. |

### The nine scenarios that describe git

The user's rule is that no unit, integration, or end-to-end test uses git.
`SPEC.md` has nine script scenarios that describe real git state:

- AC-02: the install commit is unchanged after a second `scaffold`.
- AC-14, AC-43, and AC-44: the legacy test reads the repo at the install commit.
- AC-15, AC-33, and AC-34: `stale` compares commits and an uncommitted change.
- AC-35: `stale` refuses on a shallow clone.
- AC-20: the git index, `HEAD`, and every ref are unchanged after any command.

A test with no git can prove the script's logic for each of these against a fake.
It cannot prove that the script reads real git correctly, or that it leaves real git untouched.
PRD FR-55 answers with one boundary for every git read, and a fourth suite, the contract tests, that proves the boundary on a throwaway repo.
The contract tests start git, so they narrow the user's rule. They keep its aims: no network, no change to the Avalon repo's own git state, and a run that stays apart from the three kinds.

### How the gates and the release map to GitHub

The repo is on GitHub, so GitHub Actions is the likely tool. The points below come from general knowledge of GitHub, and architecture verifies each one.

- **The gates.** A workflow that runs on a pull request into `master`, for the events opened, reopened, new commits pushed, and marked ready for review. It skips a draft.
- **Cancelling.** One concurrency group for each pull request, set to cancel a run in progress.
- **The label gate.** It also runs when a label is added or removed, so that a late label clears it. A contributor from a fork cannot set a label, so a maintainer does.
- **The release.** A workflow that runs on a push to `master`. It finds the merged pull request, reads its label, works out the next version from the latest tag, and makes the tag and the GitHub release. Its runs queue and do not cancel each other.
- **Branch rules.** `master` takes changes only through a pull request, and the gates are required checks. A rule can also require a pull request to be up to date before it merges.
- **The manifest version.** The plugin manifest sets no version (PRD FR-52). Writing one would mean a push to `master` outside a pull request. GitHub's docs say a rule that requires pull requests still applies to a workflow, and that a bypass list needs a repo that an organization owns. The other way is for every pull request to carry the number, which the label is meant to spare.
- **The plugin evals.** A gate that runs only when a pull request changes a skill, an agent file, the hook, or a template. A workflow that a fork's pull request starts receives no secret, so it cannot run there.
- **The macOS gate.** It runs the script on the system Python, because the hosted runners offer no Python 3.9 for Apple silicon.

## 6. What `SPEC.md` needs

`SPEC.md` is the one home for requirement detail, and the PRD now holds answers that it lacks.
Where the two disagree, `SPEC.md` governs until it is updated.

### Requirements to change

| Requirement | Change | PRD |
|---|---|---|
| REQ-103, REQ-243, and the chair's row in section 14 | The script writes the adopted detail file, not the chair. The chair drafts it in `.avalon/` and changes law files only through the script. | FR-9, FR-16, FR-44 |
| REQ-032 | An ID never changes once it is on the shared branch. An ID that collides at a merge changes on the side that is not yet there. | FR-60 |
| REQ-076 | An agent does not wait for the user up to a daily cap. Past the cap, the skill asks first. | FR-21 |
| REQ-126 | In a repo that is empty at install, the number 0001 is held for the architecture ADR. | FR-32 |
| REQ-142 | The legacy test reads the repo as it stood before the install landed, and finds that point in the history. It does not compute from the recorded install commit. | FR-25 |
| REQ-273 to REQ-276 | The script is the only writer of the whole laws folder, and the hook and the checksum cover every detail file. | FR-44 |
| REQ-224 | The plugin's source is a subfolder of the repo, not the repo root. | FR-52 |
| REQ-196 | The rule covers tracked files. A `.avalon/` folder that ignores itself is allowed. | OQ-11 |
| REQ-202 | The system version is the version of the docs format. | FR-61 |
| REQ-248 | The confidence is one of three named levels. | FR-38 |
| REQ-267 | `status` also lists each matter that waits for the user. `adr new` and `adr log` append a ledger row, and `adr reject` is added. One command joins law and ADR changes after a merge, and a `migrate` command changes a tree to the current format. | FR-13, FR-42, FR-60, FR-61 |
| The lint checks | The lint fails on two ADRs that share a number, on a file outside the parsed subset, and on a tree that needs `migrate`. | FR-60, FR-61, OQ-10 |
| The ledger example in section 3 | It shows a decision after one round on a vote of four to one, which REQ-096 does not allow. | FR-18 |
| Section 16 | The user's stated standards replace the seven placeholders. | FR-55 to FR-57 |
| Section 18 | Each item is settled. | PRD section 12 |

### Requirements to add

- A definition of "the user" (PRD section 2).
- A definition of a unanimous round (FR-18).
- The permission prompt for a confirmation or an override (FR-20).
- The daily cap on round tables that agents convene (FR-21).
- What a skill does when the nesting depth is too low (FR-22).
- The empty repo, the repo with no commit, existing ADRs, and the `AGENTS.md` offer at `init` (FR-32).
- The exemption for the writing standard (FR-29).
- The public repo, the standards, the gates, and releases (FR-49 to FR-59).
- Merges, upgrades, and the CI recipe (FR-60 to FR-62).
- The script commands that the architecture work adds: `matter open`, `matter wait`, `matter close`, `config set`, and `cite fix`, and the name `merge` for the command in FR-60.
- The hook's approval of the plugin's own script commands (FR-44).

### Acceptance scenarios to add

The 14 FRs from FR-49 to FR-62 have no scenario.
Scenarios are also missing for the permission prompt in each permission mode, the daily cap, the unanimous round, the guard on a detail file, the Python check in a skill, and the merge and `migrate` commands.
