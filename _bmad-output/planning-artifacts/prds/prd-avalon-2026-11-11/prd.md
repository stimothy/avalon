---
title: Avalon
status: draft
created: 2026-11-11
updated: 2026-11-11
---

# PRD: Avalon

## 0. Document Purpose

This PRD states what Avalon is for, who it serves, and what it must do, at the level a product owner signs off on.
It is written for the people who maintain Avalon, and for the architecture and story work that follows.

Avalon is an open-source developer product. Its repo is public on GitHub, and it is released under the MIT licence.
The rigor here is set for a public release that strangers install (A1).

It builds on two documents and does not replace them.
Both are temporary files in `tmp/` at the top of the repo, and the user removes them after the changes have landed:

- `BRIEF.md` proposes the design and holds the reasoning behind each choice. It calls itself "a design to react to, not a finished product". This PRD adopts that design.
- `SPEC.md` holds the requirement-level detail: 318 requirements (REQ-001 to REQ-318) and 45 acceptance scenarios (AC-01 to AC-45).

Each functional requirement here (FR-1 to FR-62) states one capability.
FR-1 to FR-48 name the REQ and AC IDs in `SPEC.md` that define them.
FR-49 to FR-59 cover the public repo, the engineering standards, the pull request gates, and releases. They follow from the user's directions in section 13.
FR-60 to FR-62 cover merges, upgrades, and CI in a target repo. They are this PRD's answers to questions the sources leave open.
Where this PRD reasoned a detail of those FRs, the text says so. `SPEC.md` does not cover them yet (section 11, item 8).
Where this PRD and `SPEC.md` disagree by accident, `SPEC.md` governs the detail, and the disagreement is a defect to report.
Where this PRD changes `SPEC.md` on purpose, section 11 names the change and `addendum.md` section 6 lists it. Such a change governs once the user signs this PRD off, and `SPEC.md` is then updated to match.

**How later work reads this PRD.** Architecture and story work load `SPEC.md` beside it:

- The REQ IDs on an FR's **Source** line are the requirement text for that FR.
- The AC IDs are its acceptance tests, in `SPEC.md` section 17.
- `SPEC.md` section 11 lists the nine core laws, section 14 the agents with their models, and section 15 every script command and lint check.
- `addendum.md` maps each feature to its sections of `SPEC.md` and `BRIEF.md`, shows which FRs have an acceptance scenario, and reviews comparable tools.

The first draft was produced from the two documents without an interview, and it carried seven assumptions, A1 to A7.
Section 13 records what each one became, and whether the user stated the answer or this PRD reasoned it.
Section 12 lists every question that the sources and this PRD raised, each with its answer.
An answer whose basis is "PRD" is this PRD's reasoning, and it stands until the user changes it.
Where an answer changes a requirement in `SPEC.md`, section 12 says so.

## 1. Vision

Avalon is a Claude Code plugin that gives any repo three kinds of governed document: laws, ADRs, and design docs.
Agents use them to orient themselves and to work correctly in the repo.
A human can read every one of them without help, and without the plugin.
The name comes from legend: Avalon is the isle of the Round Table's king, and the round table is the heart of the system.

Avalon serves any repo: an application, a service, a library, a story bible, or the Avalon repo itself.
For that reason it speaks of "the work" where a system for code alone would say "the code".

Avalon is open source under the MIT licence. Anyone installs it from its public GitHub repo, and it collects no usage data.

`BRIEF.md` grounds the design in how agents read a repo:

- An agent finds things with a search and often reads one matching line. A superseded line that stays in a document is read as live.
- An agent can recover what a repo does, but often not why. Without a rule against it, a document written by an agent invents a reason.
- Whatever loads in every session costs context in every session, so what always loads must stay small.
- A document drifts from the work, and nobody notices without a check.
- A proposer should not judge its own proposal, and an agent should not resolve a conflict silently.

Avalon answers with a small registry of laws that every session loads in full, living ADRs that always state the decision in effect, and design docs that describe only the present.
A law or a decision changes only after a round table of five seats and an impartial chair has heard it, with the exceptions in FR-15.
Agents govern themselves through that table, and the user steps in only when the user wants to. The user has the final say on every law and every decision.
Every outcome lands in a ledger, so one read shows the user what agents decided on their own.
One script does every mechanical step, so agents spend their reasoning on judgment.

This PRD reads the design as one thesis: agents work correctly when the rules they must obey are few, checkable, always loaded, and changed only on purpose.

That sentence is a summary, and `BRIEF.md` states each part of it (A6): a law test and a law budget that keep laws "few, checkable, and worth their token cost", a registry that every session loads in full, and a round table for every change.

## 2. Target User

The user is the human who is prompting Claude in the active session.
That may be a maintainer of Avalon or anyone who has installed the plugin.
"The user" names a role in a session. It does not name a person, an account, or the owner of a repo (A2).

The first point below restates the user's definition. This PRD reasons the other three from it.

- **One session, one user.** Whoever prompts the session holds the user's whole authority there: to confirm an `agent` law or ADR, to override the round table, and to have the final say.
- **Avalon keeps no identities.** It holds no list of people and does not tell one person from another. A governed document records a role, such as `user`, and never a name (FR-53). Git records who committed.
- **Between people, the repo decides.** In a repo that several people work in, each is the user in their own session, and one person's session can reverse what another's adopted. The repo's own review, such as pull requests and branch rules, decides which change stands. Avalon stands between an agent and the record, not between two people.
- **No human, no user.** A session that no human prompts has no user. A round table may still sit there within the limits on a table an agent convenes (FR-21). Nothing that needs the user completes, because no one can accept the prompt in FR-20 (OQ-33).

### 2.1 Jobs To Be Done

**The user:**

- Keep agents inside the rules of my repo without restating those rules in every session.
- Know why a choice was made, and keep a later agent from undoing it unknowingly.
- See in one read what agents decided without me, and confirm or reverse it.
- Change a rule with a second opinion that I can still overrule.
- Trust that a doc describes the repo as it is, or be told which docs do not.
- Use one system for a service, a library, or a story bible.
- Decide from the README whether Avalon suits my repo, and install it without help.

**A working agent:**

- Know what binds me before I change anything, at a small always-loaded cost.
- Find the decision and the description that cover the path I am about to change.
- Know what to do when a task conflicts with a law or an ADR.
- Propose a law or a decision without waiting for the user, within clear limits.

**A human reader** (a teammate or a reviewer):

- Read any governed document without help and without the plugin.

**A contributor** (a person who proposes a change to Avalon itself):

- Set up, test, and propose a change from the repo's own files.
- Know the licence my change falls under.

### 2.2 Non-Users (version 1.0)

These follow from the scope `SPEC.md` sets and from the definition of the user.

- A team that needs a record no agent can forge. The guards stop shortcuts and accidents only.
- A team that needs Avalon to give one person more authority than another. Every human who prompts a session is the user.
- A person who uses an agent tool other than Claude Code and wants to author or audit the docs. That person's agents can read and obey the docs. Only the plugin authors and audits them.
- A person who wants planned work tracked (section 7).

### 2.3 Key User Journeys

UJ-1 to UJ-11 are structured from the walk-throughs in `BRIEF.md`. UJ-12 and UJ-13 come from the public release.
The protagonist is "the user" because the user is a role and not a persona (A3).

Each journey ends with the FRs that state its rules.

- **UJ-1. The user sets Avalon up in a service repo that already has docs.**
  The user adds the Avalon marketplace from GitHub, installs the plugin once, and runs `/avalon:init` in the repo.
  `init` surveys the repo, sets its profile, and finds that `docs/adr/` holds content it did not create, so it proposes `docs/avalon/` as the root.
  The script seeds the nine core laws and the block.
  An agent that reads the repo writes the overview, the glossary, and `0001-architecture.md`, which the user confirms as a legacy record.
  `init` records `0002-documentation-system.md` as the user's own decision and lists the other decisions that have no record. The user chooses which to write.

  **Edge case:** the repo has no commits. `scaffold` refuses, changes nothing, and asks for a first commit (FR-32).

  *Features:* FR-25, FR-31 to FR-34.

- **UJ-2. A working agent starts a task in a target repo.**
  The session opens with the registry already in context through the block.
  The agent reads the overview before its first change and runs `for` on the path it will touch.
  It reads the ADR that covers the path and looks up one unknown term in the glossary.
  The always-loaded cost is the registry and the block alone. The agent reads the overview, the ADR, and the glossary entry on demand.

  **Edge case:** the task requires breaking a law. The agent follows FR-35.

  *Features:* FR-5, FR-28, FR-34, FR-35.

- **UJ-3. The user proposes a law and the chair would adopt different wording.**
  The user invokes `/avalon:law` with a rule. The chair screens it against the law test, and the `prose-editor` reviews the wording before the seats see it.
  Five seats vote blind in round 1. The round is not unanimous, and the chair revises the text for round 2.
  After the last round the chair would adopt wording that differs from the user's. It registers nothing and returns its objection with a counter-proposal.
  The user accepts, counters, or directs registration as written.

  **Edge case:** the nesting depth setting is below what a round table needs. The skill stops before it convenes and says which setting to change (FR-22).

  *Features:* FR-15 to FR-20.

- **UJ-4. A working agent proposes a law mid-task and the user reviews it later.**
  The agent sees a rule worth keeping and invokes the `law` skill without waiting for the user.
  The round table adopts it, the chair registers it with origin `agent`, and the agent names the change in its final report.
  Later the user scans the registry for `agent` laws, reads the ledger row with its tally and dissent, and confirms the law.
  The origin becomes `user`. The text does not change and no round table sits.

  *Features:* FR-8, FR-13, FR-21.

- **UJ-5. A round table that a working agent convenes recommends amending a `user` law.**
  A working agent finds that a `user` law blocks its task and convenes a round table to amend it.
  The round table recommends the amendment. The chair registers nothing, returns the recommendation, and waits for the user.
  The law binds the agent until the user answers.

  *Features:* FR-21, FR-35.

- **UJ-6. A working agent reverses an ADR with origin `agent`.**
  A working agent needs to replace a choice that an `agent` ADR records. The `adr` skill takes the reversal to the chair before any work is done.
  The Scout sits in place of the Enforcer and asks whether the real alternatives were considered.
  The round table adopts the reversal, and the `tech-writer` rewrites the ADR.
  The skill asks whether the decision implies a law.

  **Edge case:** the ADR has origin `user`. The chair changes nothing, returns the recommendation, and waits for the user.

  *Features:* FR-17, FR-21, FR-24.

- **UJ-7. The user amends a law and every citation is rechecked.**
  The user proposes an amendment to a law that three files cite, and the round table adopts it.
  The chair runs `law amend`. The script amends the law and prints the three citations.
  An agent rechecks each citation against the law in effect.
  The change is complete when the lint passes.

  *Features:* FR-10, FR-11.

- **UJ-8. The user records a decision that predates Avalon.**
  The user finds a decision that was in effect before Avalon was set up and has no record.
  The user asks for it to be recorded. The script runs the legacy test, the user confirms, and the ADR is recorded without a round table.

  **Edge case:** no `evidence` file exists. The decision goes to the round table as a late decision.

  *Features:* FR-25.

- **UJ-9. After a writing session in a story bible, the user brings the docs back in line.**
  The user runs `/avalon:sync`. The script lists the design docs whose covered paths changed after their stamp.
  An agent reviews only those docs, updates them, and resets each stamp through the script.
  `sync` flags a decision made during the session that has no record.

  *Features:* FR-26, FR-37.

- **UJ-10. The user audits the docs.**
  The user runs `/avalon:check`. It runs the lint, then an agent audit for contradictions between levels, then a prose review of every document.
  It reports what it finds and changes nothing.

  *Features:* FR-37, FR-38, FR-40.

- **UJ-11. The user hands a design conversation to `intake`.**
  The user runs `/avalon:intake` on a design, a spec, or a conversation.
  `intake` sorts it. Law candidates and decisions go to a round table, and description goes to design docs.

  *Features:* FR-36.

- **UJ-12. A visitor decides whether to use Avalon, and installs it.**
  A person finds the Avalon repo on GitHub.
  The README says what Avalon is, what it needs, what a round table costs, whether the version is a pre-release, and what the guards do not stop.
  The person runs the two install commands and then `/avalon:init` in a repo. From that first prompt, the person is the user.

  **Edge case:** the machine has no Python 3, or one below the floor. The user sees one message that names the version needed, and no file changes.

  *Features:* FR-31, FR-50, FR-52, FR-54.

- **UJ-13. A contributor proposes a change to Avalon.**
  A person forks the repo and follows `CONTRIBUTING.md`: a virtual environment for the development tools, then a failing test, then the code that makes it pass.
  The person opens a pull request into `master` as a draft, and no gate runs. When the person marks it ready for review, the gates run. A later push cancels the run in progress and starts another.
  A maintainer sets a `major`, `minor`, or `patch` label and merges. The release workflow publishes the next version.

  **Edge case:** the change touches one of the Avalon repo's own laws or ADRs. A round table hears it in the contributor's session, and the pull request carries the ledger row. The maintainer's merge decides whether it stands.

  **Edge case:** the pull request carries no version label. The label gate fails, and the pull request cannot merge.

  *Features:* FR-49, FR-51, FR-52, FR-53, FR-55, FR-58, FR-59.

## 3. Glossary

Terms are used exactly as defined here.
A term whose source is `SPEC.md` carries the meaning from `SPEC.md` section 1.
A path that starts with `docs/` assumes the default root. FR-33 says how the root is chosen.

| Term | Meaning | Source |
|---|---|---|
| ADR | A living document that records one decision that is costly to reverse. | `SPEC.md` |
| ADR test | The conditions a choice must meet to be a decision (FR-3). | PRD |
| Archive | The file of every amended or removed law: `docs/laws/archive.md`. | `SPEC.md` |
| Block | The managed section of `CLAUDE.md` that imports the registry (FR-34). | PRD |
| Chair | The agent that runs a round table, decides, and registers the outcome. | `SPEC.md` |
| Config file | `.avalon.yml` at the top of a target repo. It holds the root, the profile, the system version, the install time, the install commit, the caps, and the scope list. | PRD |
| Contract test | A test that proves the script's one git boundary against real git, in a throwaway repo (FR-55). | PRD |
| Contributor | A person who proposes a change to the Avalon repo. | PRD |
| Core set | The starting documents every target repo gets: the core laws, two core ADRs, the overview, and the glossary. | PRD |
| `covers` | The frontmatter field that lists the paths a document governs or describes. | PRD |
| Decision | A choice that passes the ADR test. | `SPEC.md` |
| Design doc | A document that describes the repo as it is. The overview and the glossary are design docs. | PRD |
| Detail file | A file that carries what a law's one sentence cannot. It is part of its law. | PRD |
| End-to-end test | A test of a full flow (FR-55). | PRD |
| Fixture | A small repo kept in the Avalon repo for testing. | PRD |
| Gate | A CI check that a pull request must pass before it merges (FR-58). | PRD |
| Hook | The plugin's `PreToolUse` hook, which denies a direct edit of the registry, the archive, or the ledger. | PRD |
| Install commit | The commit `scaffold` ran on, recorded once in the config file. It is a record, and the legacy test does not compute from it (FR-25). | PRD |
| Integration test | A test that may reach what the unit integrates with (FR-55). | PRD |
| Late decision | A decision that reaches the round table after its effect landed. | PRD |
| Law | A standing rule in the registry. It binds everything in the repo. | `SPEC.md` |
| Law test | The conditions a rule must meet to be a law (FR-3). | PRD |
| Ledger | The record of every round-table decision and every confirmation by the user: `docs/laws/ledger.md`. | `SPEC.md` |
| Legacy | In the repo before Avalon was installed. | `SPEC.md` |
| Legacy test | The three conditions a decision must meet to be recorded as legacy (FR-25). | PRD |
| Lint | The script command that checks the structure of the docs. | PRD |
| Maintainer | A person who can merge a change into the Avalon repo. | PRD |
| Matter | What a round table decides: a law matter or a decision matter. | `SPEC.md` |
| Origin | Who stands behind a law (`core`, `user`, or `agent`) or an ADR (`user` or `agent`). | PRD |
| Packet | The file the script assembles with what a seat needs to vote. | PRD |
| Plugin evals | The 12 plugin scenarios and the scored cases, which need a model to run (FR-55). | PRD |
| Profile | The kind of repo, set by `init`, such as a service or a story bible. | PRD |
| Registry | The table of every law in effect: `docs/laws/LAWS.md`. | `SPEC.md` |
| Release | A numbered version of the plugin, which the release workflow publishes when a pull request merges (FR-59). | PRD |
| Retired | Amended or removed, for a law. Deleted because it stopped applying, for an ADR. | `SPEC.md` |
| Root | The folder in a target repo that holds the `laws/`, `adr/`, and `design/` folders. | `SPEC.md` |
| Round table | Five seat agents and a chair that decide a matter in at most three rounds. | `SPEC.md` |
| `scaffold` | The script command that creates the tree, the config file, the core laws, and the block. `init` runs it. | PRD |
| Scope | A one-word tag on a law, from the scope list in the config file. | PRD |
| Script | The one command-line program that does every mechanical step. | `SPEC.md` |
| Seat | A subagent that votes at a round table from one fixed perspective. | `SPEC.md` |
| Session | The Claude Code session that asks for the work and owns the branch. | `SPEC.md` |
| Skill | A procedure that runs in the session and calls agents and script commands. | PRD |
| Slate | Related proposals heard in one sitting, with a separate vote on each. | PRD |
| Stale | Said of a design doc when a covered path changed after its stamp landed. | PRD |
| Stamp | The `verified` date and `verified_commit` of a design doc. | PRD |
| Tally | The count of votes in the last round held. | PRD |
| Target repo | A repo that Avalon is set up in. | `SPEC.md` |
| The work | Whatever a repo exists to hold: source, manuscript, configuration, or prompts. | `SPEC.md` |
| Unit test | A fast test of one unit, with everything else replaced by a mock (FR-55). | PRD |
| User | The human who is prompting Claude in the active session. A role, not a person or an account. The user has the final say on every law and every decision. | PRD |
| Working agent | A session or subagent that does a task in a target repo. | PRD |
| Writing standard | The rules for prose, diagrams, and images that every document follows. | PRD |

## 4. Features

Each FR ends with a **Source** line. `SPEC.md` holds the full detail under the IDs named there.
A value marked "default" is a suggestion in `SPEC.md` section 18 that this PRD adopts as the shipped default (A7).

### 4.1 The document model

**Description:** Avalon provides three kinds of document with a fixed precedence. Each kind answers one question in one voice. Realizes UJ-1, UJ-2.

| | Laws | ADRs | Design docs |
|---|---|---|---|
| Answers | What must always hold? | What did we choose, and why? | What is this, and how does it work? |
| Voice | Prescriptive | Decisional | Descriptive |
| How agents read it | Always, in full | The index, then the ADR for the area | The overview first, then by index |

#### FR-1: Three kinds with a fixed precedence

A target repo holds exactly three kinds of governed document, and precedence runs laws, then ADRs, then the work, then design docs.

**Consequences (testable):**
- When two levels disagree, the lower one is corrected or the higher one is changed through its own process.
- Other agent instructions in the repo, such as `CLAUDE.md`, rank below laws.

**Source:** REQ-001, REQ-003 to REQ-009.

#### FR-2: Any kind of repo

The user can set Avalon up in an application, a service, a library, a story bible, or the Avalon repo itself.

**Consequences (testable):**
- No format, template, or check assumes that the work is code.
- `init` on the story-bible fixture writes an overview with no section that does not apply (AC-31).

**Source:** REQ-002; AC-31.

#### FR-3: The law test and the ADR test

The chair applies the law test to a proposed law, and the `adr` skill applies the ADR test to a new decision.

**Consequences (testable):**
- A rule is a law only when all five hold:
  - It is stated as "must" or "never".
  - A reviewer can look at any piece of work and say whether it complies.
  - It applies to a class of work across the repo.
  - It is expected to hold indefinitely.
  - It is worth its context cost.
- A choice is a decision only when both hold:
  - It is costly to reverse.
  - There were real alternatives, and a future reader would ask why this one won.
- A law that comes from an ADR names that ADR as its source.

**Source:** REQ-010 to REQ-012, REQ-088, REQ-136.

#### FR-4: Documents state only what is true when read

Every document holds only present truth, and each fact has one home.

**Consequences (testable):**
- Replaced content is removed. History lives only in ADR changelogs, the archive, the ledger, and git.
- A line that states something no longer true, or never chosen, says so on the same line.
- An unknown reason, history, or intent is written as unknown.

**Source:** REQ-013 to REQ-017.

#### FR-5: A small always-loaded set, and docs that work without the plugin

A working agent gets the registry and the block in every session and reaches everything else through an index, on demand.

**Consequences (testable):**
- A session without the plugin has the registry in context (AC-22).
- Every document is plain markdown that an agent without the plugin can read and obey.
- The plugin is needed only to author and audit the docs.

**Source:** REQ-018 to REQ-020; AC-22.

### 4.2 Laws

**Description:** Laws live in one registry that is read in full. A law is one sentence with a permanent ID and an origin. An amended or removed law moves to the archive, and nothing else in the repo may cite it. Realizes UJ-3, UJ-4, UJ-7.

#### FR-6: One registry of the laws in effect

The registry holds one table of every law in effect, and no law that is not in effect.

**Consequences (testable):**
- The file opens with a statement that every law in the table is binding and that the whole table is read before any work.
- The columns are `ID`, `Scope`, `Origin`, `Law`, `Detail`, in that order, with no status column.
- A law is one sentence within the length cap (default: 200 characters, OQ-1).
- Rows are in ID order, and an added law is the last row with the next ID (AC-03).
- The registry is one file and is never split.

**Source:** REQ-022 to REQ-029; AC-03.

#### FR-7: Permanent law IDs

Every law has an ID of the form `LAW-` plus six digits from one sequence for the whole repo.

**Consequences (testable):**
- An ID is never reused and never changes. The sequence includes archived laws.
- The category of a law lives in `Scope`, never in the ID.

**Source:** REQ-030 to REQ-033.

#### FR-8: Origin, and confirmation by the user

Every law carries an origin of `core`, `user`, or `agent`, and all three bind equally.

**Consequences (testable):**
- The user turns an `agent` law into a `user` law by confirming it. The text does not change and no round table sits.
- `law confirm` adds one ledger row decided by `user` (AC-40).

**Source:** REQ-034, REQ-035; AC-40.

#### FR-9: Detail files

A law has a detail file only when one sentence cannot carry it.

**Consequences (testable):**
- The body has four parts: Meaning, Applies to, Examples, and Enforcement.
- The chair drafts the detail file before round 1, and the seats vote on the law and its detail file together.
- After adoption, the wording and the detail file change only by amendment.
- A working agent opens a detail file only when it cannot act on the one-line law alone.
- The script writes the adopted detail file, and the guards in FR-44 cover it (OQ-25).

**Source:** REQ-036 to REQ-040, REQ-314, REQ-315.

#### FR-10: Amendment, removal, and the archive

An amendment creates a law with a new ID, and the amended or removed row moves to the archive.

**Consequences (testable):**
- In the archive, `Replaced by` names the amending law and never changes. `Now in effect` names the end of the chain and is updated on every later change (AC-05).
- Removing a law ends its whole chain, and no earlier law is restored (AC-06).
- A return to an earlier wording is an amendment that restates it, with a new ID.
- The detail file of a retired law is deleted (AC-07).

**Source:** REQ-041 to REQ-051; AC-05 to AC-07.

#### FR-11: No citation of a retired law or ADR

No tracked text file outside the archive and the ledger may cite a retired law by ID or a retired ADR by number. This includes an ADR changelog.

**Consequences (testable):**
- Lint fails on a citation of a retired law and names the file, the line, and the law in effect (AC-08).
- Lint fails on a citation of a retired ADR and names the file and the line (AC-38).
- `law amend` and `law remove` print every citation of the retired ID (AC-09).
- An agent fixes each citation, not the script. A citation of an amended law is rechecked against the law in effect, and a citation of a removed law is deleted.
- A law change is not complete until the lint passes.

**Source:** REQ-052 to REQ-056, REQ-268; AC-08, AC-09, AC-38.

#### FR-12: The law budget

The config file sets a soft cap on the size of the registry (default: 100 laws in effect, OQ-2).

**Consequences (testable):**
- When a proposal would exceed the cap, the round table names laws to merge or remove, or states why none can go.
- The cap is a pressure, not a block: a law the round table adopts is registered either way.

**Source:** REQ-070 to REQ-072.

### 4.3 The ledger

**Description:** The ledger is the user's review tool. It records every round-table decision, including a rejection, and every confirmation by the user. Realizes UJ-4, UJ-5.

#### FR-13: One row for every decision

The script appends one ledger row for every decision a round table makes and for every confirmation by the user.

**Consequences (testable):**
- The columns are `Date`, `Decision`, `Proposed by`, `Decided by`, `Rounds`, `Tally`, `Dissent`.
- `Decided by` is `table`, `user override`, or `user`. `Dissent` names each seat that voted against the decision made, with its reason (AC-10).
- A confirmation row holds `none` for `Rounds`, `Tally`, and `Dissent`, and `Proposed by` keeps the original proposer (AC-40).
- Nothing but the script writes the ledger, and the ledger is never loaded automatically.
- A legacy record and the install record of ADR `0002` get no row.
- `adr new` and `adr log` append the row for a new or a reversed decision, and an `adr reject` command logs a rejected one. `SPEC.md` names a command only for `adr retire` and `adr confirm`. Its section 18 suggests the rest, and this PRD adopts the suggestion (OQ-15).

**Source:** REQ-057 to REQ-063, REQ-309, REQ-316; AC-10, AC-40.

#### FR-14: One tally format

A tally is written as labelled counts in the order approve, amend, reject. A row with no vote holds `none`.

**Consequences (testable):**
- Every count is written, including a zero. The counts are the votes of the last round held and add up to five.
- The script writes the tally from the recorded votes. A bare pair such as `4-1` fails the lint (AC-11).

**Source:** REQ-064 to REQ-069; AC-11.

### 4.4 The round table

**Description:** A round table hears every change to a law and every decision before it is carried out. A dedicated chair runs it, five seats vote from fixed perspectives, and the user has the final say. Realizes UJ-3, UJ-4, UJ-5, UJ-6.

#### FR-15: When a round table sits

A law is created, amended, or removed only through a round table, and a decision goes to a round table before it is carried out.

**Consequences (testable):**
- The exceptions are the core laws seeded at install (FR-32), a legacy decision (FR-25), and the install record of ADR `0002` (FR-32).
- The user or any agent may propose a matter. An agent convenes a round table by invoking the `law` or `adr` skill and does not wait for the user.
- Laws and ADRs in effect bind every agent until the round table decides.
- Related proposals may be heard as a slate.

**Source:** REQ-073 to REQ-078.

#### FR-16: A dedicated, impartial chair

A dedicated chair agent runs every round table, and whoever proposes a matter never chairs it.

**Consequences (testable):**
- The chair works in its own context and returns only the outcome and the list of files that changed.
- The chair weighs arguments and does not argue for the proposal.
- The chair's file holds the round-table procedure, the voting rules, and the vote format, and they live nowhere else.
- The chair is the only agent that changes law files, and it changes them only through the script (FR-44).
- The chair drafts a detail file in `.avalon/`, beside the packet. The law command copies the adopted draft into the laws folder.

**Source:** REQ-079 to REQ-082, REQ-242 to REQ-244.

#### FR-17: Five seats with fixed perspectives

Five seats sit at every round table. Four sit on every matter, and the fifth depends on the matter.

**Consequences (testable):**
- The Practitioner asks whether an agent can follow this in daily work, and what it costs.
- The Skeptic asks whether this is needed at all. On a decision matter it argues for the strongest alternative, including doing nothing.
- The Jurist asks whether it conflicts with, duplicates, or leaves a loophole in a law or an ADR.
- The Steward asks what this locks in and who pays a year later. It takes the lens of the repo's domain, such as an architect for a service or a continuity editor for a story bible.
- The Enforcer is the fifth seat on a law matter and asks whether a violation can be detected (AC-25).
- The Scout is the fifth seat on a decision matter and asks whether the real alternatives were considered (AC-26).
- A seat cannot write a file or spawn an agent. Its file lists only read and search tools.

**Source:** REQ-083 to REQ-087, REQ-245 to REQ-247; AC-25, AC-26.

#### FR-18: Screening, then at most three rounds

The chair screens a proposal, and the seats then vote in at most three rounds.

**Consequences (testable):**
- The chair turns away a repeat of a rejected proposal that brings no new argument.
- The `prose-editor` reviews the wording, and any draft detail file, before each round.
- In round 1 the seats vote in parallel, and no seat sees another's vote (AC-25).
- A vote is approve, amend with proposed wording, or reject, and each carries a short reason.
- The chair records the votes of each round through the script, and the script tallies the round.
- When a round is not unanimous, the chair revises the text and circulates every vote and reason.
- A later round goes to the same five seat agents by message. The message asks each seat whether the revision resolves its objection. There is no fourth round (AC-27).
- When a seat cannot be resumed, the chair starts another, and the packet gives it the earlier votes and reasons.
- A round is unanimous when all five seats approve, or when all five reject. Five amend votes are not unanimous, because each carries its own wording. `SPEC.md` does not define the word, so this PRD does (OQ-35).

**Source:** REQ-088 to REQ-100; AC-25, AC-27.

#### FR-19: Decision, registration, and hand-back

On a unanimous vote, or after round 3, the chair adopts, adopts with final edits, or rejects.

**Consequences (testable):**
- The chair decides by the weight of the arguments, not the count of votes.
- For a law, the chair runs the script's law command, which also writes the detail file the seats approved (FR-9). The law is registered as FR-6 states, and the ledger gains one row (AC-03).
- For a decision, the chair records the ledger row through the script, and the `tech-writer` then writes the ADR. FR-13 names the commands.
- The chair never commits. The session that asked for the round table commits (AC-30).
- Where the repo's conventions allow, a law change is a commit of its own.

**Source:** REQ-101 to REQ-106; AC-03, AC-30.

#### FR-20: The user's final say

The user has the final say on every law and every decision, and the round table still hears the user's proposal.

**Consequences (testable):**
- When the round table would reject or reword the user's proposal, the chair registers nothing until the user accepts, counters, or directs registration as written (AC-29).
- A law or decision registered over the round table's objection is marked `user override` in the ledger, with origin `user` and each dissenting seat named (AC-10).
- Nothing is registered as decided by `user` or by `user override` before the user answers in the session.
- A command that claims the user's confirmation or override carries a flag, and the skill passes the flag only after the user answers. The hook turns a command that carries the flag into a permission prompt, so the human accepts that exact command before it runs. The hook's match on a Bash command is best-effort, as FR-44 states. `SPEC.md` names no mechanism, so this PRD adds one (OQ-13).
- Where no prompt can be shown, such as a session that no human prompts, the command must not run. The Claude Code docs do not state how a hook's prompt behaves in every permission mode. An acceptance scenario proves each mode, and the hook denies the flag in any mode that would let the command through with no prompt.
- The hook answers within its time limit, because a hook that times out does not block the call (section 6.4).
- The prompt stops a mistaken claim. It does not stop forgery, which section 6.1 places out of scope.

**Source:** REQ-107 to REQ-111; AC-10, AC-29.

#### FR-21: Limits on a round table an agent convenes

A round table that an agent convenes registers its outcome at once only where the origin allows.

**Consequences (testable):**
- It may create a law, amend or remove an `agent` law, adopt a new decision, and reverse an `agent` ADR.
- For a `user` or `core` law, or a `user` ADR, it registers nothing. The chair returns the recommendation and waits for the user (AC-28).
- An agent cannot override the round table. An agent names every law change and every decision it caused in its final report.

- A config value caps how many matters agents bring to a round table on their own in one day (default: 5). Up to the cap an agent does not wait for the user. Past it, the skill asks the user before it convenes.
- The script counts a matter when it assembles the first packet for an agent's proposal. A day is the local calendar day of the machine. A confirmation by the user does not count, and neither does a proposal that the chair screens out.
- The count lives in `.avalon/`, so it is a count for one checkout.
- The sources set no limit, and REQ-076 says an agent does not wait for the user. This PRD changes that rule past the cap (OQ-27).

**Source:** REQ-112 to REQ-118; AC-28.

#### FR-22: Nesting depth

A session, or a subagent that the session spawned, can seat a full round table. A deeper subagent hands its proposal up to the agent that spawned it.

**Consequences (testable):**
- `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` must be at least 2 when the session convenes a round table, and at least 3 when a subagent does.

- When the setting is below what the round table needs, the skill stops before it convenes. It changes nothing and tells the user which setting to change. An unset setting allows three layers, which is enough (OQ-31).
- No skill can detect ahead of time that a Claude Code behaviour in section 6.4 is missing. When a step of a round table fails, the chair stops, registers nothing, and reports the failure. It never decides on an incomplete round and never seats a smaller table.
- `init` checks the setting and warns the user at setup.

**Source:** REQ-119 to REQ-122.

### 4.5 ADRs

**Description:** An ADR is one living document for one decision topic. It always states the decision in effect, and its changelog records how it got there. Realizes UJ-6, UJ-8.

#### FR-23: One living ADR for each decision topic

An ADR is edited in place and always states the decision in effect.

**Consequences (testable):**
- No ADR is marked superseded. Every ADR in the directory is in effect, and a proposal lives in a branch.
- The file name is a four-digit number and a topic. Numbers are sequential and never reused.
- The frontmatter holds `adr`, `summary`, `covers`, and `origin`. A legacy ADR also holds `evidence` (FR-25).
- The origin of an ADR is `user` or `agent`.
- The body sections are Context, Decision, Consequences, Alternatives rejected, and Changelog, in that order.
- Each line under Alternatives rejected carries the word "Rejected".
- Each changelog line has a date, one of the six markers in `SPEC.md` section 5, and a one-line summary.

**Source:** REQ-123 to REQ-132.

#### FR-24: Changing, retiring, and confirming an ADR

A reversal or a retirement goes to a round table. Adding detail to an ADR does not.

**Consequences (testable):**
- On a reversal the body states the new decision, the old choice moves to Alternatives rejected with its reason, and the changelog gains one line.
- `adr retire` refuses without votes or an override and changes no file (AC-36). With a complete round of five recorded votes it deletes the file, adds a ledger row that names the number, the title, and the reason, and prints every citation (AC-37).
- A round table that an agent convenes cannot retire a `user` ADR without the user's confirmation.
- The user confirms an `agent` ADR without a round table. The origin becomes `user`, the decision does not change, and the changelog gains a `(user)` line (AC-41).
- A new decision that fails the ADR test gets no round table and no ADR. A rejected decision leaves no line in any ADR.
- The `adr` skill prefers revising an existing ADR to creating one.
- After a decision is adopted, the `adr` skill asks whether it implies a law.

**Source:** REQ-133 to REQ-139, REQ-310 to REQ-312; AC-36, AC-37, AC-41.

#### FR-25: Legacy decisions

A decision that was in effect at the install commit is recorded without a round table, at install or at any time after.

**Consequences (testable):**
- The record must pass the legacy test. All three conditions hold:
  - Every `covers` path existed at the install commit (AC-14).
  - At least one `evidence` file is named, and each existed at that commit (AC-44).
  - The user confirms that the decision predates the install (AC-43).
- The record has origin `user`, and its changelog line carries `(legacy)`.
- A decision that fails the test, or that landed after install, goes to the round table as a late decision, and its ledger row says so.
- A lost reason is written as unknown.
- On a shallow clone the legacy test refuses to run and says why.
- The test reads the repo as it stood before the install landed, and it finds that point in the history: the commit before the one that added the config file, or the current commit while the config file is not committed yet. It does not compute from the recorded install commit, because a squash merge or a rebase can leave that commit outside the history. Where the install was committed straight onto the commit `scaffold` ran on, the two are the same commit. `SPEC.md` names the install commit, so this changes REQ-142 (OQ-46).

**Source:** REQ-140 to REQ-146, REQ-313, REQ-317; AC-14, AC-43, AC-44.

### 4.6 Design docs, the glossary, and indexes

**Description:** Design docs describe the repo as it is. Frontmatter lets the script find the docs that cover a path and the docs that are stale. Realizes UJ-2, UJ-9.

#### FR-26: Design docs with script-detected staleness

A design doc describes the present only, and the script lists every design doc that is stale.

**Consequences (testable):**
- A doc is stale when a covered path changed after its stamp landed, in a commit or in an uncommitted change (AC-15, AC-34).
- A doc that is stamped in the same commit as the change is not stale (AC-33). A doc whose stamp is not committed is not stale.
- The rule looks at the commits that touched a covered path after the stamp landed. It does not use `verified_commit`, which records what was checked.
- On a shallow clone, `stale` refuses to run and says why (AC-35).
- A change that makes a design doc untrue updates that doc in the same change.

**Source:** REQ-147 to REQ-153, REQ-313; AC-15, AC-33 to AC-35.

Many CI systems use a shallow clone by default, so a CI job that runs `stale` must fetch the full history. FR-62 covers what a CI job runs.

#### FR-27: The glossary

The glossary is a design doc and the one home for a definition.

**Consequences (testable):**
- It is one table of `Term` and `Meaning`, one term to a row, in alphabetical order.
- It holds only terms that are specific to the repo or used in a special sense.
- It never holds a rule. A definition that tells an agent what it must do is a law.
- The document size cap does not apply to it (FR-45).

**Source:** REQ-154 to REQ-162, REQ-318.

#### FR-28: Frontmatter, generated indexes, and `covers`

The script reads and writes frontmatter, and generates the ADR index and the design-doc index from it.

**Consequences (testable):**
- An added document appears in its index after `index` runs. Before that, the lint fails on the missing entry (AC-16).
- A document has at most five `covers` entries, and an entry that matches nothing is an error (AC-17).
- `for` on a path lists the ADRs and design docs that cover it and nothing else (AC-18).

**Source:** REQ-163 to REQ-171; AC-16 to AC-18.

### 4.7 The writing standard

**Description:** One writing standard applies to every document. It ships as the detail file of a core law, so the skills and agents that write docs load it and other sessions do not. Realizes UJ-6, UJ-9.

#### FR-29: Prose rules

Every document follows the prose rules of the writing standard.

**Consequences (testable):**
- A document has one subject. New material goes into the document that owns its subject, and a document is created only when none does.
- A document is split when it covers more than one subject or passes the size cap, and a split leaves no stub.
- A sentence holds one idea. Parallel items become a list, and a comparison becomes a table.
- A paragraph holds one point and has no length cap. An edit is woven in, not appended.
- A word that places something in time appears only in a changelog.
- A reader who has never seen the repo can follow each document. The `prose-editor` applies this test (FR-40).

**Source:** REQ-172 to REQ-181.

The writing standard ships as the detail file of a core law, and three rules for a detail file do not suit it (FR-9, FR-10). It is exempt from the four-part body. A change to it is an amendment. On amendment the file is carried to the new ID and is not deleted (OQ-20).

#### FR-30: Diagrams and images

ADRs and design docs may hold Mermaid diagrams. Design docs may hold images, and ADRs may not.

**Consequences (testable):**
- A diagram is a flowchart, sequence, state, or entity-relationship diagram. A sentence before it says what it shows.
- A diagram shows only the present and stays within the node cap (default: 15, OQ-4).
- An image shows only what Mermaid cannot draw, has alt text, and never carries a fact the text lacks.

**Source:** REQ-182 to REQ-195.

### 4.8 Setup, layout, loading, and conflict handling

**Description:** The user installs the plugin once and sets Avalon up in each repo with `init`. The block loads the registry in every session. A working agent follows one response for each kind of conflict. Realizes UJ-1, UJ-2, UJ-5.

#### FR-31: Install the plugin from GitHub

The user installs Avalon from its GitHub repo, which is both the marketplace and the plugin.

**Consequences (testable):**
- The plugin has no `bin/` directory, because claude.ai and Cowork do not install a plugin that has one.
- The plugin declares the option `default_root`, which the user sets once.
- For development, the plugin loads for one session from a local checkout with `claude --plugin-dir <path>`.
- `claude plugin validate .` passes before a release (AC-32).
- FR-52 moves the plugin into a subfolder of that repo. The repo stays the marketplace, and the local checkout path then names the subfolder.

**Source:** REQ-198, REQ-223 to REQ-229; AC-32.

#### FR-32: `init` and the core set

`init` gives every target repo the same core set and is safe to run again.

**Consequences (testable):**
- In a repo with no docs, `scaffold` creates the tree, the config file, the nine core laws, and the block, and the lint passes (AC-01).
- A second run leaves the install time, the install commit, and content outside the block unchanged (AC-02).
- An agent that reads the repo writes the core ADRs `0001-architecture.md` and `0002-documentation-system.md`, the overview, and the glossary.
- `init` records ADR `0002` as the user's decision, with origin `user`, the marker `(user)`, and no round table.
- `init` lists decisions it found that have no record, and the user chooses which to write.
- In a repo that holds no work at the install commit, `init` skips `0001-architecture.md`. The first architecture decision goes to a round table and takes the number 0001, so that `0002-documentation-system.md` has the same name in every repo. REQ-126 says numbers are sequential, and this is the one exception (OQ-21).
- In a folder that is not a git repo, or in a repo with no commit, `scaffold` refuses, changes nothing, and says that a first commit is needed (OQ-22).
- `init` leaves untouched any ADR the repo already holds, and lists each one. The user folds one in through `intake`: it becomes a legacy record, and the existing file is its evidence (OQ-34).
- The old file then states a decision that has another home. `intake` asks the user whether to delete it or to replace its body with a link. The legacy test looks at the repo as it stood before the install, so removing the file later breaks nothing.
- `init` offers to write the block into `AGENTS.md`, and writes it only when the user accepts (OQ-24).

**Source:** REQ-213 to REQ-222, REQ-235, REQ-236; AC-01, AC-02.

#### FR-33: The root, the config file, and the tree

The root is a setting for each repo, resolved from the config file, then the `default_root` option, then `docs/`.

**Consequences (testable):**
- A target repo holds only the generated docs, the config file, and the block. This PRD reads that as a rule about tracked files.
- Avalon keeps packets, draft detail files, and recorded votes in a `.avalon/` folder at the top of the repo. The folder holds its own ignore file, so git does not track it and Avalon edits no ignore file of the repo (OQ-11).
- `init` never writes into a folder that holds content it did not create. On a clash it proposes another root.
- `init` warns when a site generator publishes the whole of `docs/`.
- `move-root` moves the tree and rewrites the config file, the block, and every link, and the lint then passes (AC-19).
- No environment variable sets the root.

**Source:** REQ-196, REQ-197, REQ-199 to REQ-206; AC-19.

#### FR-34: The always-loaded block

`init` writes the block into `CLAUDE.md`, between two fixed comment lines, and the block imports the registry.

**Consequences (testable):**
- A subagent has the registry in context (AC-23). FR-5 covers the session without the plugin (AC-22).
- The built-in Explore and Plan agents do not receive `CLAUDE.md`. They only read and plan, and the session that acts on their output has the laws.
- The script rewrites only what sits between the two comment lines.
- The block states precedence, what to read before a change, and what to do on a contradiction.
- The block tells a tool that does not expand the import to read the registry in full first.
- The block says that laws change only through the `law` skill.
- The same block may go in `AGENTS.md` with a "read in full" instruction in place of the import.

**Source:** REQ-207 to REQ-210; AC-22, AC-23.

#### FR-35: Conflicts are never resolved silently

A working agent never resolves a conflict silently and never works around a law or an ADR. Each of six kinds of conflict has one response.

**Consequences (testable):**
- A design doc disagrees with the work: the agent updates the design doc.
- The work disagrees with an ADR: the agent reports it. Either the work is fixed, or the decision really changed and the ADR is revised.
- An ADR disagrees with a law: the agent reports it. Either the ADR is revised, or an amendment goes to a round table.
- A task requires breaking a law: the agent stops that part and names the ID. It may take an amendment to a round table, and the law binds until the round table decides.
- A task requires breaking an ADR: the agent stops that part and names the ID. It may take a reversal to a round table, and the ADR binds until the round table decides.
- The work already violates a law: the agent reports it, and fixes it only if it is inside the task.

**Source:** REQ-211, REQ-212.

### 4.9 Skills and supporting agents

**Description:** The user invokes seven skills. Ten agent files hold the roles the skills call: the chair, six seats, the `law-reviewer`, the `tech-writer`, and the `prose-editor`. Realizes UJ-9, UJ-10, UJ-11.

#### FR-36: Seven skills under the `avalon` name

The user invokes `init`, `intake`, `law`, `adr`, `design`, `check`, and `sync` as `/avalon:<skill>`.

**Consequences (testable):**
- No skill has a bare command.
- An agent is always spawned by its full name, such as `avalon:tech-writer`.
- In the fixture that holds decoy agents (FR-46), each agent spawns as `avalon:<agent>` and runs Avalon's prompt (AC-24).
- `intake` sorts a design, spec, or conversation: law candidates and decisions go to a round table, and description goes to design docs.
- `design` writes, updates, splits, and merges design docs.

**Source:** REQ-230 to REQ-234; AC-24.

#### FR-37: `check` reports and `sync` reconciles

`check` audits the docs and changes nothing. `sync` brings the docs back in line after work.

**Consequences (testable):**
- `check` runs the lint, then an agent audit for contradictions between levels, then a prose review of every document.
- `sync` updates stale design docs and flags unrecorded decisions and law violations.

**Source:** REQ-234, REQ-237.

#### FR-38: The law reviewer

The `law-reviewer` checks a diff or a path against the laws and ADRs and reports what it finds.

**Consequences (testable):**
- Each violation is reported with the ID, the location, and a confidence.
- The confidence is one of three levels. High: the law's text and the work plainly conflict. Medium: they conflict on the likeliest reading. Low: they may conflict, and a person should look. `SPEC.md` names no scale, so this PRD adds one (OQ-30).
- It never fixes what it finds, and it opens the detail file of every law in scope.
- `check` may run it on a stronger model for a full audit.

**Source:** REQ-241, REQ-248 to REQ-250.

#### FR-39: The tech writer

The `tech-writer` writes and edits ADRs and design docs to the writing standard.

**Consequences (testable):**
- It decides whether to extend or create a document, when to split one, and how to word each line. It writes the Mermaid diagrams.
- It words the content it is given. It does not decide what is true or chosen, and it invents no reason.
- It always loads the writing standard, and it never writes law files.

**Source:** REQ-251 to REQ-254.

#### FR-40: The prose editor

The `prose-editor` reads each document as a reader who has never seen the repo.

**Consequences (testable):**
- It is given the document and not the conversation behind it.
- It fixes prose in ADRs and design docs and lists what it changed.
- It never edits a file under `docs/laws/`. For the wording of a law or a detail file, it returns suggestions to the chair before the seats vote.
- It changes wording and never meaning. When a fix would change meaning, it reports the passage.
- Writing takes one pass: the `tech-writer` writes, the `prose-editor` edits, and the lint runs. The two agents do not go back and forth.
- Under `check`, it reviews every document and only reports.

**Source:** REQ-255 to REQ-263.

#### FR-41: Each agent sets its own model and effort

Each of the ten agent files sets its own model, effort, and tools.

**Consequences (testable):**
- The values in `SPEC.md` section 14 are starting values, tuned against the fixtures.
- No agent file names Fable or Haiku as its model.

**Source:** REQ-238 to REQ-240.

### 4.10 The script

**Description:** One script does every repeatable step that needs no reasoning. It is the only writer of the registry, the archive, and the ledger, and it never writes to git. Realizes UJ-7, UJ-9.

#### FR-42: One script for every mechanical step

A skill tells the agent which script command to run, and agents never do these steps by hand.

**Consequences (testable):**
- The script changes files and prints the list of files it changed.
- An agent runs `for` before it changes a file, and reads `status` instead of the files it summarizes.
- `status` also lists each matter that waits for the user. The votes for it stay in `.avalon/` until a law or ADR command uses them (OQ-14).
- Judgment stays with agents: what is a law or an ADR, the wording, the votes, and whether a doc is still true.

**Source:** REQ-021, REQ-264 to REQ-269, REQ-298. `SPEC.md` section 15 lists every command.

#### FR-43: The script never writes to git

The script reads git and never stages, commits, branches, tags, or pushes.

**Consequences (testable):**
- Any script command leaves the git index, `HEAD`, and every ref unchanged (AC-20).
- No command takes a commit message as an argument.

**Source:** REQ-270 to REQ-272; AC-20.

#### FR-44: Write guards

The hook and a checksum guard the laws folder, and the script refuses to register what the round table has not decided.

**Consequences (testable):**
- The hook denies an Edit or Write call on the registry, the archive, and the ledger, in the session and in subagents (AC-21). Its check of Bash commands is best-effort.
- The script records a checksum, and the lint fails when the three files, the install time, or the install commit do not match it (AC-12, AC-13).
- The same two guards cover every detail file, so the script is the only writer of anything under the laws folder. `SPEC.md` guards the three files only and has the chair write the detail file, so this PRD changes REQ-103 and widens REQ-273 to REQ-276 (OQ-25).
- A law or ADR command refuses without a complete round of five recorded votes or a user override, and changes no file (AC-04).
- The hook asks the human to approve any command that carries the flag for a confirmation or an override (FR-20).
- In a repo that Avalon is set up in, the hook approves a call that runs one of the plugin's everyday script commands and carries no such flag, so a round table does not stop for the user at every script step. It approves nothing else, and it never approves `scaffold`, `move-root`, the merge command, or `migrate`. The user's own deny and ask rules still apply. The architecture work added this consequence, after the Claude Code docs showed that each script call from the chair would otherwise prompt the user.
- A legacy decision must pass the legacy test instead. The install record of ADR `0002` needs neither votes nor the legacy test, and is accepted once (AC-39).

**Source:** REQ-273 to REQ-277; AC-04, AC-12, AC-13, AC-21, AC-39.

#### FR-45: Lint

`lint` checks the structure of every document and fails on each structural error.

**Consequences (testable):**
- It fails on each of these:
  - A registry or an archive that does not match its table format.
  - A law ID that is repeated or has the wrong form.
  - A law over the length cap.
  - A broken link, or an index that is missing a document.
  - An ADR changelog that is missing or is not the last section.
  - A glossary with two terms in a row, a repeated term, or terms out of order.
  - A document over the size cap (default: 400 lines, OQ-3).
- The size cap applies to ADRs, design docs other than the glossary, and detail files only. The lint checks no other file against it (AC-45).
- It flags a time word outside a changelog and a very long sentence, and does not fail on them (AC-42). It does not scan the registry, the archive, or the ledger for time words.
- It does not measure paragraphs.

**Source:** REQ-278 to REQ-297; AC-42, AC-45.

### 4.11 Building and proving Avalon in this repo

**Description:** Avalon is built in its own repo and runs on itself before it ships.

#### FR-46: Templates and fixtures

The plugin ships eight templates, and the repo holds three fixtures.

**Consequences (testable):**
- The templates are the registry, the archive, the law detail file, the ADR, the design doc, the block, the core laws, and the writing standard.
- The fixtures are a small code repo, a library, and a story bible.
- One fixture holds decoy project agents named `chair` and `tech-writer` and a decoy `docs/adr/` folder. `init` proposes another root there and writes nothing into the decoy folder (AC-24).
- `claude plugin eval` can run scored cases against the fixtures.

**Source:** REQ-299 to REQ-302; AC-24.

#### FR-47: Engineering standards are refined before any code

The user and the agent refine the Avalon repo's engineering standards into working standards before any code is written.

**Consequences (testable):**
- The user has stated the standards (D6, D7), and FR-55 to FR-57 hold them. They are the starting point in place of the seven placeholders in `SPEC.md` section 16.
- Each refined standard has exact wording, a kind (law, ADR, or guideline), and a stated check. `addendum.md` section 5 holds this PRD's proposal for each, and the user reviews it in step 1 (OQ-23).
- A placeholder binds nothing until it is refined. A refined standard applies from the first line of code.
- The shipped script follows NFR-3. Tools used only for development may be dependencies.

**Source:** REQ-303 to REQ-306; D6 and D7 (section 13).

#### FR-48: Avalon runs on itself, in a fixed build order

The Avalon repo runs Avalon, and its own round tables ratify the core laws before they ship.

**Consequences (testable):**
- The build follows the eight steps in section 9.2.
- Each refined standard that is a law or an ADR goes to a round table and is registered. A guideline is written into a design doc of the Avalon repo.
- Every Avalon document written for the Avalon repo follows the Avalon process, from build step 1. Before the plugin can run, a round table is held by the same procedure with stand-in agents, and its records are written by hand in the final formats (D10). `SPEC.md` waits for the round table to exist (REQ-305), so this changes it.
- The Avalon repo holds its own laws, ADRs, and design docs. They bind every change to the repo: the script, the hook, the tests, and the CI and release scripts.
- No permanent file in the Avalon repo cites this PRD, `BRIEF.md`, `SPEC.md`, any other plan file, or an ID that one of them defines. The repo's own laws, ADRs, and design docs are what a permanent file may cite (D9).
- From build step 4, a gate runs the Avalon lint on the Avalon repo's own docs (FR-58). This consequence is this PRD's reasoning.

**Source:** REQ-305, REQ-307, REQ-308; D8, D9, and D10 (section 13).

### 4.12 The public repo and its releases

**Description:** The Avalon repo is public, and it is the only place a user gets the plugin. It carries what a person needs to trust, install, and contribute to an open-source project, and it publishes nothing private. Realizes UJ-12, UJ-13.

The user named the public repo, the MIT licence, and the common files (D1). The consequences under each FR below are this PRD's reasoning.

#### FR-49: The MIT licence

Avalon is released under the MIT licence.

**Consequences (testable):**
- A `LICENSE` file at the top of the repo holds the MIT text and a copyright line. The line names "the Avalon contributors", so no person's name is needed (OQ-37).
- The plugin manifest names the licence as `MIT`, and the README states it.
- A contribution is accepted under the same licence, and `CONTRIBUTING.md` says so.
- The shipped script has no third-party dependency (NFR-3). The plugin needs no third-party notice unless a later change adds third-party code.
- Avalon writes text into a target repo: the core laws, the templates, the writing standard, and the block. A target repo keeps that text with no condition and no notice. The templates carry the MIT No Attribution licence, and the README says so (OQ-38).

**Source:** D1 (section 13). No `SPEC.md` requirement.

#### FR-50: A README that lets a stranger decide and install

The README gives a person who has never seen Avalon enough to decide whether to use it, and to install it without help.

**Consequences (testable):**
- It states what Avalon is, whether it is a pre-release, where the latest release is, and the licence.
- It states what Avalon needs: the lowest Claude Code version, the lowest Python 3 version, and the supported operating systems (FR-54).
- It gives the two install commands and the first step, `/avalon:init`.
- It states what Avalon writes into a repo, and that Avalon collects no usage data (NFR-5).
- It states what the hook approves and what it denies, and how a user turns the approval off (FR-44).
- It states the limits a user must know before trusting Avalon: the guards stop shortcuts and accidents and not forgery, and a round table costs up to 15 seat votes (sections 6.1 and 6.3).
- It links to the licence, the contributing guide, the security policy, and the release notes.
- A person who follows only the README, on a machine that has never held Avalon, reaches a passing lint after `init` (SM-11).

**Source:** D1 (section 13); REQ-225 for the install commands.

#### FR-51: The files a public repo is expected to carry

The repo carries the community files that GitHub's community standards checklist names.

**Consequences (testable):**
- `CONTRIBUTING.md` says how to set up a development environment (FR-54), run the tests and the lint, and propose a change. It states the engineering standards once they are refined (FR-47).
- `CONTRIBUTING.md` explains the gates and the version labels, and says that a maintainer sets the label (FR-58, FR-59).
- `CONTRIBUTING.md` says how a change to the Avalon repo's own laws and ADRs is proposed: a round table hears it in the contributor's session, and the pull request carries the ledger row. A maintainer's merge decides whether it stands (section 2).
- `CODE_OF_CONDUCT.md` is the Contributor Covenant, and it names a way to report a breach. A conduct report goes through the repo's private vulnerability reporting form, marked as a conduct report, and a report about a maintainer goes to GitHub's own abuse report. The user can replace this with a dedicated address at any time (OQ-40).
- Security reports go through GitHub's private vulnerability reporting, so no personal email address is published.
- `SECURITY.md` says how to report a vulnerability in private and which versions get fixes. It says that the limits in section 6.1 are known limits and not vulnerabilities.
- The repo has an issue template for a bug, an issue template for a proposal, and a pull request template.
- GitHub's community standards checklist for the repo shows every item complete (SM-12).

**Source:** D1 (section 13). No `SPEC.md` requirement.

#### FR-52: Numbered releases from a default branch that always installs

A user receives Avalon as numbered releases. From the first commit that holds a plugin manifest, the default branch, `master`, installs at every commit.

**Consequences (testable):**
- Versions follow semantic versioning, and the release workflow makes each release (FR-59).
- The plugin manifest sets no version. The Claude Code docs say an install then follows the commit. Once the release workflow lands, every commit on `master` is a release, so a user who updates receives exactly the releases. The git tag and the GitHub release carry the number (OQ-44).
- A person who installs for the first time gets `master` as it stands. So a change merges into `master` only when the gates pass, and `claude plugin validate .` is one of them (FR-58).
- The version stays below 1.0, and the README calls it a pre-release, until every release gate in section 10 passes. Version 1.0 is the first release that claims all of `SPEC.md`.
- Release notes say what changed for a user, and what a user must do in a target repo on upgrade (FR-61).
- The plugin lives in a subfolder of the repo, and the marketplace file at the root names it. The Claude Code docs say that only the plugin's folder is copied, so an install carries no planning file, test, fixture, or CI script. `SPEC.md` makes the repo root the plugin, so this needs REQ-224 changed (OQ-39).

**Source:** This PRD, following D1 (section 13); REQ-224, REQ-227. The Claude Code docs, read on 2026-11-11.

#### FR-53: Nothing private is published

No tracked file and no governed document publishes a secret or a person's private details.

**Consequences (testable):**
- No tracked file in the Avalon repo holds a secret, a credential, a personal email address, or a path on someone's machine.
- Git ignores local tool state, personal configuration, virtual environments, and working files such as decision logs and review notes.
- The fixtures hold invented content only.
- A gate scans for secrets (FR-58).
- In any repo, a document Avalon writes records a role, such as `user` or `agent`. It never records a person's name, an email address, or a path on a machine.

**Source:** This PRD, following D1 and D3 (section 13). No `SPEC.md` requirement.

#### FR-54: Stated requirements, no environment to set up, and a plain failure

The shipped script needs a Python 3 interpreter and nothing else, and it says so plainly when the interpreter is missing or too old.

**Consequences (testable):**
- A user installs no package, creates no virtual environment, and needs no network connection to run the script.
- The script runs on Python 3.9 and every later Python 3 release. The macOS developer tools provide 3.9, and so do Debian 11 and RHEL 9. A system with an older default needs a later Python installed (OQ-28).
- Each skill checks for Python 3.9 or later before its first script command. When the check fails, the user sees one message that names the version needed, and no file changes. The script cannot give this message, because it does not run without a suitable Python.
- `init` makes the check first and sets nothing up when it fails. Without Python the hook cannot run, so the guards in FR-44 would be off.
- Avalon supports macOS and Linux, including Linux under WSL. Version 1.0 does not support native Windows, and the README says so (OQ-36).
- The gates run the script's tests on the floor version and on the current Python 3 release, on each supported operating system (FR-58).
- The README states the lowest Claude Code version. It is the lowest version on which the plugin acceptance scenarios pass, found in build step 4.
- A contributor's development tools live in a virtual environment that git ignores. The shipped script never needs them.

**Source:** This PRD's answer to D2 (section 13); REQ-265, REQ-306.

### 4.13 How the Avalon repo is built: standards, gates, and releases

**Description:** The user set the standards for code and tests, the gates a pull request must pass, and the way a release is made (D4 to D7). The standards apply to all code and every script written in the Avalon repo: the shipped script, the hook, the tests, and the CI and release scripts. Realizes UJ-13.

A consequence marked "(PRD)" is this PRD's reasoning. Every other consequence restates the user.

#### FR-55: Tests come first, in three kinds that run apart

Code is written test-first, and every test is a unit test, an integration test, or an end-to-end test.

**Consequences (testable):**
- Code is written with test-driven development. The test comes before the code it covers.
- Every test has three parts, in order: Arrange, Act, Assert.
- A unit test tests one unit. It replaces everything else with a mock, so that it tests only what the unit is meant to do, and it runs fast.
- An integration test may reach what the unit integrates with.
- An end-to-end test tests a full flow.
- Unit tests and integration tests run separately.
- No unit, integration, or end-to-end test uses git or the network.
- The author of a test weighs its CPU time and its memory.
- Each test earns its place. Its author can say what it proves that no other test proves.
- The file system is what an integration test reaches, because git is the script's only other outside dependency (PRD).
- Every read of git sits behind one boundary. The three kinds of test replace the boundary with a fake, and they prove against that fake the nine script scenarios that describe git, and every other scenario that reads it (OQ-42) (PRD).
- A fourth suite, the contract tests, proves the boundary itself against real git. It works in a throwaway repo, uses no network, never touches the Avalon repo's own git state, and runs apart. It is outside the three kinds, and it is the only suite of script tests that starts git. The plugin evals run the whole plugin in a fixture, so git runs there too (OQ-42) (PRD).
- A fifth suite, the plugin evals, holds the 12 plugin scenarios and the scored cases. They need a model, so they need the network, and they are outside the three kinds (OQ-43) (PRD).

**Source:** D6 (section 13). `SPEC.md` section 16 holds the placeholders that this FR overtakes.

#### FR-56: Coverage, linters, formatters, type checkers, and sound design

Code meets a coverage floor, passes the automated checks, and follows the DRY and SOLID principles.

**Consequences (testable):**
- Tests cover at least 80% of the code. A gate fails below that (FR-58).
- Code passes a linter, a formatter, and a type checker.
- Code follows the DRY principle and the SOLID principles.
- The tools are `pytest`, `coverage`, `ruff` as linter and formatter, `mypy`, and `markdownlint`, as `BRIEF.md` suggests (OQ-23) (PRD).
- Unit tests and integration tests count together toward the 80%. The measure covers all Python in the repo except the tests (PRD).
- The whole unit run has a time budget (default: 10 seconds), and a gate fails past it (PRD).
- A reviewer judges DRY and SOLID, because no tool decides them (PRD).

**Source:** D6 (section 13). `SPEC.md` section 16 holds the placeholders that this FR overtakes.

#### FR-57: No grab-bag directories

Code is well organized, and no directory is a grab bag.

**Consequences (testable):**
- When a directory becomes a grab bag, its files are grouped into subdirectories.
- The docs tree that Avalon creates is the exception. ADRs go in the `adr` folder and are not split into subfolders.
- The exception covers the `laws` and `design` folders too, and it holds in every target repo, because `SPEC.md` fixes that layout (PRD).
- A directory is a grab bag when its name states no single purpose, such as `utils`, `helpers`, `misc`, or `common`, or when its files do not all serve the purpose its name states (OQ-23) (PRD).
- The layout that Claude Code fixes for a plugin is a second exception. Agent files stay flat in `agents`, because a subfolder becomes part of an agent's name (PRD).

**Source:** D7 (section 13). No `SPEC.md` requirement.

#### FR-58: Gates run on a pull request that is ready for review

The CI gates run on a pull request into `master` that is open for review, and nowhere else.

**Consequences (testable):**
- The gates run on a pull request whose base is `master`.
- The gates do not run while a pull request is a draft. They run once it is marked ready for review.
- A newer push to a pull request cancels the gates that are still running for an older push.
- The gates do not run on a merge or a push to `master`. The release workflow is the one exception (FR-59).
- One gate checks that the pull request carries a version label (FR-59).
- The gates are these (PRD):
  - The unit tests and the integration tests, as separate runs, and the end-to-end tests (FR-55).
  - The coverage floor, the linter, the formatter, and the type checker (FR-56).
  - The script's tests on the Python floor and on the current release, on each supported operating system (FR-54).
  - `claude plugin validate .` and the secret scan (FR-52, FR-53).
  - The contract tests, as a run of their own (FR-55).
  - From build step 4, the Avalon lint on the Avalon repo's own docs (FR-48).
  - The plugin evals, on a pull request that changes a skill, an agent file, the hook, or a template. Each run has a cost limit (FR-55).
- The plugin evals need a model credential, and a pull request from a fork does not receive one. A maintainer moves such a change to a branch of the Avalon repo before it merges (OQ-43) (PRD).
- A change reaches `master` only through a pull request whose gates pass, and a branch rule enforces it. Nothing runs on `master` to catch a change that skipped the gates (PRD).

**Source:** D4 (section 13). No `SPEC.md` requirement.

#### FR-59: A merge releases the next semantic version, chosen by a label

A release workflow runs when a pull request merges into `master`, and it publishes the next version.

**Consequences (testable):**
- Versions follow semantic versioning and are written in the form `v1.2.3`.
- A pull request carries a `major`, `minor`, or `patch` label. The label sets which part of the version the release raises.
- A gate fails when a pull request carries none of the three labels.
- The release workflow is the only workflow that runs on a merge or a push to `master`.
- The label gate also fails when a pull request carries more than one of the three labels (PRD).
- Every merged pull request releases a version, because every one carries a label (PRD).
- A release is a git tag and a GitHub release with notes (PRD).
- Releases are made in merge order, and a later merge never cancels a release in progress (PRD).
- No pull request carries `major` until every release gate in section 10 passes. The pull request that takes Avalon to `v1.0.0` is the first (PRD).
- The release workflow writes nothing to `master`. The version lives in the tag and the GitHub release, and the plugin manifest sets none (FR-52, OQ-44) (PRD).

**Source:** D5 (section 13). No `SPEC.md` requirement.

### 4.14 Merges, upgrades, and CI in a target repo

**Description:** The sources name or imply three things and define none of them: what happens when two branches change laws, what an upgrade preserves, and what a CI job runs. Every consequence in this section is this PRD's reasoning.

#### FR-60: Law and ADR changes from two branches can be joined

When a git merge joins two branches that each changed laws or ADRs, one script command makes the docs whole again.

**Consequences (testable):**
- Two branches can each allocate the same law ID or the same ADR number, and each records its own checksum. A git merge of the two leaves conflict markers in the registry, the ledger, and the config file, and the hook stops an agent from editing them by hand.
- After such a merge the lint fails and names the command to run. The lint also fails on two ADRs that share a number.
- The command reads both sides from the conflict markers, so it needs no further read of git. The user or the skill names the side that is already on the shared branch.
- That side keeps its IDs and numbers. On the other side, a law or an ADR that collides takes the next free one. The command rewrites every pointer to it in the registry, the archive, the ledger, and the name of its detail file. It prints every other citation for an agent to fix (FR-11).
- Two ADRs can share a number with no conflict to read. The user then names the file that takes the next number.
- The command keeps every row from both sides. It adds no decision and drops none.
- When both sides amended or removed the same law, the command refuses, and the matter goes to a round table.
- The command records the checksum for the joined files, and it writes nothing to git (FR-43).
- A renumbered ID had never reached the shared branch. REQ-032 says an ID never changes, so this PRD narrows that rule to an ID on the shared branch.

**Source:** This PRD (OQ-45). `SPEC.md` says nothing about a merge. The command narrows REQ-032 and adds a script command and a lint check.

#### FR-61: An upgrade never changes the record

A later version of the plugin works in a repo that an earlier version set up, and it leaves what the record says as it found it.

**Consequences (testable):**
- The system version in the config file is the version of the docs format. It changes only when a release changes a file format.
- A release recognises a tree in an older format. It refuses to write to that tree, and the lint says that the tree needs the `migrate` command.
- `migrate` changes a tree to the current format. It changes how a file is laid out and never what it says: every law, archive row, ledger row, ADR, and design doc keeps its content, and the install time and the install commit stay as they are.
- `migrate` prints each file it changed and records the system version and the checksum. It runs only when the user asks.
- `init` and `scaffold` stay safe to run again (FR-32), and neither migrates a tree.
- A change to the text of a core law in a later release reaches a repo only as an amendment that a round table hears and the user confirms. An upgrade never applies it.
- A plugin older than the tree's system version refuses to write, and tells the user to update the plugin.
- A pre-release may change a format, and its notes say so. After 1.0, a release that changes a format takes the `major` label, and its notes name the command to run (FR-59).

**Source:** This PRD (OQ-19); REQ-202, REQ-308.

#### FR-62: A CI recipe for a target repo

The Avalon docs give a target repo a recipe for running the lint in CI.

**Consequences (testable):**
- The recipe fetches the script from an Avalon release and runs `lint`. It needs Python 3 and git, and neither Claude Code nor a model.
- `lint` works on a shallow clone.
- The recipe does not run `stale`, because `stale` needs the full history (FR-26). It shows how to fetch the history for a repo that wants `stale`.
- Whether the lint gates a merge is the target repo's choice. In the Avalon repo it is a gate (FR-58).

**Source:** This PRD (OQ-18); REQ-308.

## 5. Cross-Cutting NFRs

- **NFR-1. Context cost in every session.** Only the registry and the block load in every session (REQ-018). `BRIEF.md` estimates 30 to 40 tokens for each registry row. At the default soft cap of 100 laws, the registry costs about 3,500 tokens in a session (OQ-2). The block is fixed text with the root path filled in, so it does not grow with the repo (REQ-209).
- **NFR-2. Bounded deliberation.** A matter takes at most three rounds of five votes (REQ-083, REQ-097).
- **NFR-3. No dependencies in the shipped script.** The script runs on Python 3 with the standard library only (REQ-265, REQ-306). It needs no virtual environment, because it has no dependency for one to isolate. FR-54 states the floor and the supported operating systems.
- **NFR-4. No collisions.** Every name is scoped to Avalon, and `init` never writes into a folder that holds content it did not create (REQ-204, REQ-230).
- **NFR-5. No data collection.** The script opens no network connection, and Avalon collects no usage data from any repo. Claude Code still sends a session's content to the model, as it does for any work. This PRD adds the requirement, because the plugin is public and its hook runs on a user's tool calls.

This PRD sets no latency or throughput target. Three things bound cost: NFR-2, the daily cap on round tables that agents convene (FR-21), and the cost limit on each run of the plugin evals (FR-58). `check` and `sync` run only when the user asks (OQ-27).

## 6. Constraints and Guardrails

### 6.1 Integrity

The guards stop shortcuts and accidents. They do not stop an agent that sets out to forge a record, and `SPEC.md` places that out of scope.
The hook's check of Bash commands is best-effort (REQ-275).
A mistaken claim that the user confirmed or overrode is a different case from forgery. The permission prompt in FR-20 stops it.

### 6.2 Git

FR-19 and FR-43 keep the chair and the script out of git.
The session commits, because only the session knows the branch, the repo's conventions, its hooks and signing, and whether the user keeps git for themselves.

### 6.3 Cost

Every law costs context in every session, so the law test asks whether a law is worth that cost (REQ-011).
The cost of a round table is a risk (section 8), and FR-21 caps how many an agent convenes in a day.

### 6.4 Platform dependencies

Avalon depends on Claude Code behaviours that `SPEC.md` section 12 lists. A change to any of the first five can break the product:

- A subagent can spawn subagents, three layers below the session by default.
- A subagent with `SendMessage` can resume a subagent it spawned. The Claude Code docs state this for interactive sessions only.
- A plugin's `PreToolUse` hook can deny Edit, Write, and Bash calls in the session and in subagents.
- A subagent receives `CLAUDE.md`, and an `@` import in it expands for a subagent. The built-in Explore and Plan agents do not receive it.
- The full `avalon:<agent>` name works as an agent type. The Claude Code docs do not state this, and AC-24 is the proof.

The design also relies on these checked behaviours:

- An agent file sets its model, effort, and tools.
- A plugin's agent files ignore `hooks`, `mcpServers`, and `permissionMode`.
- A plugin declares options that a user sets.
- One GitHub repo can be both marketplace and plugin.
- On a shared bare name, a project or user agent outranks a plugin agent.

A plugin cannot ship permission rules, so the hook is the blocking mechanism.

The public release adds these points from the Claude Code docs, read on 2026-11-11:

- Claude Code neither ships nor requires Python (FR-54).
- A plugin has no way to declare the lowest Claude Code version it needs. The README carries it (FR-54).
- A `PreToolUse` hook that times out does not block the call, so the hook in FR-44 must answer quickly.
- A plugin whose source is the repo root is copied whole, and the docs name no way to leave a file out. A plugin in a subfolder is copied alone (OQ-39).
- An install follows the commit when the plugin manifest sets no version (FR-52).
- A hook can turn a tool call into a permission prompt. The docs state how this behaves in most permission modes and not in all, so an acceptance scenario must prove each mode (FR-20).

### 6.5 What loads, and what does not

The archive, the ledger, and the glossary are never loaded automatically (REQ-042, REQ-058, REQ-160).
FR-5, FR-9, and FR-39 state what does load.

### 6.6 Accepted limits

`BRIEF.md` names these limits and accepts them:

- Mermaid: the lint cannot check full syntax, the layout cannot be adjusted, and a terminal shows the source.
- `covers` is coarse. A false alarm costs one review of a document, and a miss leaves a stale document.

### 6.7 The public repo

- Everything pushed is public and stays in git history. A secret that is pushed is treated as leaked, even when a later commit removes it.
- The default branch is the install source for every new user (FR-52).
- A person's identity never enters a governed document (FR-53). Commit authorship is public in git, and it is each person's own choice.

## 7. Non-Goals

These come from the out-of-scope list in `SPEC.md` section 1.

- Avalon does not hold planned work. Specs, briefs, and roadmaps live outside the system.
- A listing in an official plugin marketplace is out of scope.
- The script and the chair make no write to git.
- Avalon does not stop an agent that sets out to forge a record.
- Avalon does not check full Mermaid syntax in a target repo.
- Avalon does not set the root through an environment variable.
- Avalon does not map the whole repo through `covers`. A folder that no document covers is not an error.
- Avalon does not remove the correlation between seats that run on related models. It reduces it.

This PRD adds three, from the directions in section 13:

- Avalon does not tell one person from another, and it gives no person more authority than another.
- Avalon does not install or manage a Python interpreter or an environment for the shipped script.
- Avalon collects no usage data.

## 8. Risks

| Risk | Why it matters | What the sources do about it |
|---|---|---|
| A platform behaviour changes | The round table needs nesting, `SendMessage` resume, and full agent names (section 6.4) | AC-24 proves agent names. FR-18 gives the fallback for a seat that cannot be resumed. The README states the lowest Claude Code version (FR-54), and a plugin cannot enforce it. A round table that fails part-way registers nothing and reports the failure (FR-22). |
| Seats share blind spots | Seats run on related models, so five votes are not five independent views | Fixed perspectives, a blind first round, a standing Skeptic, and mixed models. The user's final say is the backstop. |
| A seat defends its first vote | Resumed seats keep their context, and may keep their position out of habit | The chair's message asks whether the revision resolves the objection (FR-18). A changed vote is expected when it does. |
| Round tables cost more than they return | An agent may convene a round table unprompted, and the user learns of it afterwards. Each one runs up to five seat agents for three rounds, with the chair and the Jurist on a stronger model. | Slates, resumed seats, and a daily cap on the round tables that agents convene (FR-21). |
| The registry grows | The law budget is a soft cap and never blocks | The law test, and the duty to name laws to merge or remove. |
| Agents ignore a law in context | A law in context is advice until something checks it | The `law-reviewer`, `check`, and `sync`. The lint checks structure, not compliance. |
| A confirmation or override is claimed in error | The script cannot tell the user's answer from an agent's claim | The human approves each such command at a permission prompt (FR-20). Forgery is out of scope (section 6.1). |
| A detail file is edited directly | It is part of its law, and `SPEC.md` guards only the registry, the archive, and the ledger | The guards cover the whole laws folder (FR-44). This needs `SPEC.md` changed. |
| The design meets real use late | Version 1.0 is all of `SPEC.md` | Build step 4 sets Avalon up in its own repo, and every merge releases a version below 1.0 (section 9.3). |
| A broken commit reaches new users | `master` is the install source, and a first install takes it as it stands | The gates run on every pull request before it merges (FR-58). |
| Two pull requests pass alone and break `master` together | The gates run on the pull request, and nothing runs on `master` | A branch rule can require a pull request to be up to date with `master` before it merges. Architecture decides whether to set it. |
| A merge cannot be held back from release | Every merge releases a version at once | The gates are the only stop (FR-58). The plugin evals are among them for any change to a skill, an agent file, the hook, or a template. |
| The code that reads git is never tested against git | No unit, integration, or end-to-end test may use git, and the script reads git for the legacy test, `stale`, and the install commit | The contract tests prove the one git boundary against real git (FR-55). They narrow the user's rule, so the user confirms them. |
| Two branches change laws at once | Each allocates the next law ID and records its own checksum, so a merge breaks both | One script command joins them (FR-60). |
| Users cannot name the version they run | The plugin manifest sets no version, so Claude Code shows a commit | The release notes map each version to its commit (FR-52). The alternative is that every pull request carries the version number. GitHub's rules on who may push to `master` come from its docs as read on 2026-11-11, and architecture confirms them. |
| Python differs between machines | Claude Code does not ship Python, and the interpreter's name and version vary by system | A floor of Python 3.9, tests on the floor and on the current release, and a plain failure message (FR-54). Native Windows is not supported in 1.0. |
| Something private is published | A public repo keeps every pushed commit | Ignore rules and a secret scan on every pull request (FR-53). |
| Two people reverse each other | Every human who prompts a session is the user, with the user's whole authority | The repo's own review decides between people (section 2). Avalon does not. |

A landscape review is in `addendum.md` section 3. Its findings are unverified.

## 9. Scope and Delivery

### 9.1 In scope for version 1.0

Version 1.0 is everything `SPEC.md` requires, delivered through all eight build steps, plus the public repo in section 4.12 (A4).

- The plugin: seven skills, ten agent files, one hook, one script, and the templates.
- The docs in a target repo: the generated tree, the config file, and the block.
- Three fixtures, and all 45 acceptance scenarios.
- Avalon set up in its own repo, with the core laws ratified.
- The public repo: the licence, the README, the community files, and numbered releases.
- The engineering standards, the pull request gates, and the release workflow (section 4.13).
- The merge command, the upgrade path, and the CI recipe for a target repo (section 4.14).

### 9.2 Build order

The order comes from REQ-308.

1. This repo's standards, refined from the placeholders.
2. Formats and templates: every file format, the core law text, and the writing standard.
3. The script: `scaffold`, the `law` commands, `packet`, `vote`, `tally`, `index`, and `lint` with its checksum.
4. The `law` skill, the chair, the six seats, the `prose-editor`, and the hook. Avalon is then set up in this repo. The core laws are ratified, with those of this repo's standards that are laws.
5. `init`, the `tech-writer`, and the `adr` commands, tested on the fixtures.
6. The `adr`, `design`, and `intake` skills. The standards that are ADRs are then ratified.
7. `check`, `sync`, the `law-reviewer`, and the `status`, `stale`, `verify`, and `for` commands.
8. Hardening: a CI check, `move-root`, and an upgrade path for plugin versions.

Steps 1 to 4 are the first slice. `SPEC.md` sets Avalon up in its own repo at step 4, so the design meets real use there before steps 5 to 8 are built (OQ-26).
The user has since directed that the Avalon repo follows the Avalon process from step 1 (D10). Until step 4, stand-in agents hold each round table and the records are written by hand, and from step 4 the plugin does both.

### 9.3 Releases, and where the public repo work lands

The repo is public, and it is its own marketplace. Every commit is public, and a person can install whatever `master` holds from the day it holds a plugin manifest.
Before step 4 that install holds no working round table, and the README says so.
Once the release workflow lands, every merge releases a version (FR-59). Avalon is a pre-release, with a version below 1.0, until the release gates pass (FR-52).
The eight steps stay as `SPEC.md` gives them. The public repo work, the gates, and the release workflow land beside them:

| When | What lands |
|---|---|
| The start of step 1 | The licence, a README that states the pre-release status, the ignore rules, and the code of conduct (FR-49, FR-50, FR-51, FR-53) |
| The end of step 1 | `CONTRIBUTING.md` with the refined standards, the templates, the gates, and the release workflow (FR-47, FR-51, FR-58, FR-59). From here every merge releases a version below 1.0. |
| Step 4 | The first release that governs a repo. With it come the security policy and the stated requirements (FR-51, FR-54). The Avalon lint joins the gates (FR-48). |
| Step 8 | The CI check and the upgrade path, then `v1.0.0` once every release gate passes |

The gates and the release workflow land at the end of step 1 so that they cover the first line of code. That timing is this PRD's reasoning.

### 9.4 Build step 8

`SPEC.md` names two items in build step 8 and defines neither. This PRD defines both:

- The CI check is a recipe for a target repo (FR-62).
- The upgrade path is FR-61.

## 10. Success Metrics

`BRIEF.md` and `SPEC.md` state no success metrics. This PRD sets them as follows (A5):

- The release gates are binding. Version 1.0 does not ship until each one passes.
- The primary and secondary metrics are measured in the Avalon repo only, from its ledger, its lint, and its fixtures. Avalon collects no usage data (NFR-5), so nothing is measured in another person's repo.
- No primary or secondary metric has a target before version 1.0, because no baseline exists. The Avalon repo records each one from build step 4, and the user sets targets from that baseline after 1.0 (OQ-29).

**Release gates**

- **SM-1.** All 45 acceptance scenarios pass: 33 script scenarios as automated tests and 12 plugin scenarios. They validate the 26 FRs that cite a scenario. The other 36 FRs have no scenario, and `addendum.md` section 2 names what proves each (OQ-30). Nine of the script scenarios describe real git state. The end-to-end tests prove them against a fake, and the contract tests prove the git boundary (FR-55).
- **SM-2.** `claude plugin validate .` passes (AC-32). Validates FR-31.
- **SM-3.** The Avalon repo's own round tables have ratified the nine core laws. Validates FR-48.
- **SM-11.** A person who follows only the README, on a machine that has never held Avalon, installs the plugin and reaches a passing lint after `init`. The gate runs once on each supported operating system. Validates FR-50, FR-54.
- **SM-12.** GitHub's community standards checklist shows every item complete, and the secret scan finds nothing in the tracked files. Validates FR-49, FR-51, FR-53.

**Primary: does the thesis hold?** Each is measured in the Avalon repo itself, which runs Avalon from build step 4.

- **SM-4.** Decisions reach the round table first. The count of ledger rows for a late decision. Lower is better. Validates FR-15, FR-25.
- **SM-5.** Conflicts are caught when they happen. The count of violations a working agent reports during a task, against the count first found later by `check` or the `law-reviewer`. Validates FR-35, FR-37, FR-38.
- **SM-6.** The user reviews what agents decide. The share of `agent` laws and ADRs that the user later confirms or reverses. Validates FR-8, FR-13, FR-21.

**Secondary**

- **SM-7.** The law budget presses. Every adoption that takes the registry over the soft cap names laws to merge or remove, or states why none can go. Validates FR-12.
- **SM-8.** Docs stay true. `stale` lists no design doc at the end of a `sync`. Validates FR-26, FR-37.
- **SM-9.** `init` works on every profile. On each of the three fixtures, `init` leaves a tree whose lint passes. Validates FR-2, FR-32.
- **SM-10.** Scored cases under `claude plugin eval` meet a threshold on each fixture. Each case runs three times and passes when two runs pass. Every case for FR-20, FR-21, and FR-35 passes, and at least 80% of the other cases pass (OQ-30). Validates FR-46.

**Counter-metrics (do not optimize)**

- **SM-C1.** The number of laws. More laws is not better, and each one costs context in every session. A registry kept small by rejecting sound laws is not better either. Counterbalances SM-7.
- **SM-C2.** The share of unanimous first rounds. This is this PRD's own signal. A round table that never disagrees over a long run suggests that the seats are correlated. Counterbalances SM-4.
- **SM-C3.** A passing lint. A lint that passes because documents were deleted or emptied is not a success. Counterbalances SM-8 and SM-9.

## 11. Source Observations

These are points where the sources leave a gap or pull against each other. `SPEC.md` says such a point is reported, not worked around.
Each item names this PRD's answer. `addendum.md` section 6 lists each change that `SPEC.md` needs.

1. REQ-057 and REQ-138 require a ledger row for every decision, and the ADR commands name one only for `adr retire` and `adr confirm`. FR-13 adds the rest (OQ-15).
2. REQ-213 gives every target repo the same core set. An empty repo cannot get `0001-architecture.md` under the legacy test, so FR-32 skips it there (OQ-21).
3. REQ-315 says a detail file changes only by amendment, and no guard covers it. FR-44 widens the guards (OQ-25).
4. The writing standard ships as a detail file, and three rules for a detail file do not suit it. FR-29 exempts it (OQ-20).
5. The core laws are a draft until the Avalon repo's round tables ratify them (REQ-215), so the law text that ships is not final. This is by design.
6. REQ-196 says a target repo holds only the generated docs, the config file, and the block. Packets and votes need a `.avalon/` folder. The folder ignores itself, and this PRD reads REQ-196 as a rule about tracked files (OQ-11).
7. REQ-096 and REQ-101 turn on a unanimous round, and no requirement says which votes make one. FR-18 defines it (OQ-35). The ledger example in `SPEC.md` shows a round table that decides after one round on a vote of four to one. That fits neither the rule nor any reading of the word, so the example needs a change.
8. `SPEC.md` holds no requirement for the public repo, the Python floor, the pull request gates, the release workflow, merges, upgrades, or a CI recipe. FR-49 to FR-62 have no AC behind them, and most have no REQ. `SPEC.md` is the one home for requirement detail, so it needs them added.
9. `SPEC.md` places specs and briefs outside the system, and it makes the repo root the plugin (REQ-224). `BRIEF.md` and `SPEC.md` are tracked in `tmp/` and the planning files in `_bmad-output/`, so they would reach every user who installs. FR-52 moves the plugin into a subfolder, which changes REQ-224 (OQ-39).
10. `SPEC.md` names "the user" throughout and never defines the term. Section 2 holds the definition the user gave.
11. `SPEC.md` section 16 holds seven placeholder standards. The user has since stated the standards in full (D6, D7), and they go beyond the placeholders: three kinds of test, mocks, no git and no network in tests, formatters and type checkers, DRY and SOLID, and no grab-bag directories. Section 16 needs to catch up.
12. The user's rule that no test uses git meets nine script scenarios that describe real git state: AC-02, AC-14, AC-15, AC-20, AC-33, AC-34, AC-35, AC-43, and AC-44. FR-55 proves them against a fake and adds the contract tests (OQ-42).
13. `SPEC.md` says nothing about a git merge that joins two branches that each changed laws or ADRs. Both allocate the next ID, and both record a checksum. FR-60 adds a command and a lint check, and it narrows REQ-032 (OQ-45).
14. REQ-202 puts a system version in the config file and does not say what it counts. FR-61 defines it as the version of the docs format.
15. REQ-248 has the law reviewer report a confidence and names no scale. FR-38 adds one (OQ-30).
16. REQ-103 has the chair write a detail file directly, and REQ-243 and the agent table in section 14 call the chair the writer of law files. FR-44 makes the script the only writer of the laws folder, so all three need a change (OQ-25).
17. REQ-076 says an agent that convenes a round table does not wait for the user. FR-21 makes it ask past a daily cap (OQ-27).
18. REQ-126 says ADR numbers are sequential. FR-32 holds the number 0001 for the architecture ADR in an empty repo (OQ-21).
19. REQ-142 has the legacy test read the repo at the recorded install commit. A squash merge or a rebase can leave that commit outside the history, and the test would then have nothing to read. REQ-151 already avoids this for a stamp. FR-25 does the same for the install (OQ-46).

## 12. Questions and Answers

Every question that the sources and this PRD raised is answered below. OQ-40 has a working answer that the user may replace with a dedicated address.
The Basis column says where an answer comes from:

- **SPEC**: a suggestion in `SPEC.md` section 18, adopted here. `SPEC.md` says each one is for the user to set, so the user changes any of them by saying so (A7).
- **User**: the user stated it (section 13).
- **PRD**: this PRD reasoned it. It stands until the user changes it.

| ID | Question | Answer | Basis |
|---|---|---|---|
| OQ-1 | Length cap for a law | 200 characters. | SPEC |
| OQ-2 | Soft cap on the registry | 100 laws in effect, about 3,500 tokens in a session. | SPEC |
| OQ-3 | Size cap for a document | 400 lines. | SPEC |
| OQ-4 | Node cap for a diagram | 15. | SPEC |
| OQ-5 | Size cap and formats for an image | 500 KB. PNG, JPEG, SVG, and WebP. | SPEC |
| OQ-6 | Length at which a sentence is flagged | 40 words. | SPEC |
| OQ-7 | The list of time words | "previously", "formerly", "new", "now", "currently", "recently", and "no longer", refined against the fixtures. | SPEC |
| OQ-8 | The default scope list | `all`, `laws`, `adr`, `design`, and `docs`. Each repo adds its own. | SPEC |
| OQ-9 | The list of repo profiles | `application`, `service`, `library`, `story-bible`, and `other`. | SPEC |
| OQ-10 | How the script parses the config file and frontmatter with no YAML parser | A subset of flat keys, scalar values, and inline lists. Every example in `BRIEF.md` fits it. A file outside the subset fails the lint, which names the line. | SPEC. PRD for the lint failure. |
| OQ-11 | Where packets and recorded votes live | In a `.avalon/` folder at the top of the repo. The folder holds its own ignore file, so Avalon edits no ignore file of the repo. REQ-196 is read as a rule about tracked files. | SPEC. PRD for the ignore file. |
| OQ-12 | Where the checksum lives | In a field in `.avalon.yml`. The file is tracked, so a clone and a CI job can verify it. | SPEC |
| OQ-13 | How the user's confirmation or override reaches the script | A flag on the law and ADR commands, which the skill passes only after the user answers. The hook turns every command that carries the flag into a permission prompt, so the human accepts that exact command. Where no prompt can be shown, the command does not run (FR-20). | SPEC for the flag. PRD for the prompt. |
| OQ-14 | Where a recommendation waits for the user | The chair returns it, and the votes stay in `.avalon/` until a law or ADR command uses them. `status` lists each matter that waits for the user. | SPEC. PRD for `status`. |
| OQ-15 | Which command writes the ledger row for a new, reversed, or rejected decision | `adr new` and `adr log` append it, and an `adr reject` command is added (FR-13). | SPEC |
| OQ-16 | Who may change the scope list | The user edits it, and an agent asks first. | SPEC |
| OQ-17 | Script output and exit codes | 0 on success, 1 on lint findings, and 2 on a refusal or a usage error. | SPEC |
| OQ-18 | What the CI check in build step 8 runs, whether it gates a merge, and how it works on a shallow clone | It is a recipe for a target repo that runs `lint`, which works on a shallow clone. Gating is the target repo's choice (FR-62). The Avalon repo's own gates are FR-58. | PRD |
| OQ-19 | What an upgrade to a later plugin version must preserve in a target repo | Every law, archive row, ledger row, ADR, and design doc, and the install time and commit. A `migrate` command handles a format change, and it runs only when the user asks (FR-61). | PRD |
| OQ-20 | How the writing standard fits the rules for a detail file | It is exempt from the four-part body, a change to it is an amendment, and the file is carried to the next ID (FR-29). | SPEC |
| OQ-21 | What `init` does with `0001-architecture.md` in an empty repo | `init` skips it. The first architecture decision goes to a round table and takes the number 0001 (FR-32). | SPEC. PRD for the number. |
| OQ-22 | What `scaffold` does in a repo with no commits | It refuses, changes nothing, and asks for a first commit. It does the same in a folder that is not a git repo (FR-32). | SPEC. PRD for the second case. |
| OQ-23 | The wording, kind, and check of each engineering standard. Which tools? What counts toward the 80%? How fast is fast? What is a grab bag? How are skills and agent files tested? | FR-55 to FR-57 hold the standards with their tools, the coverage measure, the unit time budget, and the definition of a grab bag. `addendum.md` section 5 proposes a kind and a check for each. `claude plugin validate` and the plugin evals test skills and agent files. The user reviews the wording in step 1, as REQ-303 requires. | User (D6, D7) for the standards. `BRIEF.md` for the tools. PRD for the rest. |
| OQ-24 | Whether `init` writes the block into `AGENTS.md` | `init` offers it and writes it only when the user accepts (FR-32). | SPEC |
| OQ-25 | Should a guard cover detail files? | Yes. The hook and the checksum cover the whole laws folder, and the script writes the detail file (FR-44). This changes REQ-103 and widens REQ-273 to REQ-276. | PRD |
| OQ-26 | Are build steps 1 to 4 a first slice? Is anything released to other users before step 8? | Yes to both. Every merge releases a version below 1.0 from the end of step 1, and the first release that governs a repo comes at step 4 (section 9.3). | PRD |
| OQ-27 | Is there a cost budget or a limit for round tables, `check`, and `sync`? | A config value caps the matters that agents bring to a round table on their own in one day, with a default of 5. This changes REQ-076 past the cap (FR-21). `check` and `sync` run only when the user asks, so they have no budget. No latency target is set. | PRD |
| OQ-28 | What are the lowest supported versions of Python and Claude Code, and which operating systems are supported? | Python 3.9, with no virtual environment. The macOS developer tools still provide 3.9.6, and Debian 11 and RHEL 9 ship 3.9. The lowest Claude Code version is found in step 4 and stated in the README. macOS and Linux are supported (FR-54). | PRD, checked against vendor sources on 2026-11-11 |
| OQ-29 | Which success metrics does the user adopt, and with what targets? | This PRD proposes the metrics, and the user adopts them at sign-off. The release gates are binding. The other metrics have no target before 1.0, and the user sets targets from the Avalon repo's baseline after it (section 10). | PRD |
| OQ-30 | What proves the FRs that no acceptance scenario covers, and the agent judgment in FR-16, FR-17, FR-19, FR-35, and FR-37 to FR-40? Which threshold applies, and what confidence scale? | `addendum.md` section 2 names a proof for each of the 36 FRs. A scored case runs three times and passes when two runs pass. Every case for FR-20, FR-21, and FR-35 passes, and at least 80% of the rest (SM-10). The confidence scale has three levels (FR-38). | PRD |
| OQ-31 | What does a skill do when the nesting depth is too low, or a Claude Code behaviour is missing? | When the setting is too low, it stops before it convenes, changes nothing, and tells the user which setting to change. A missing behaviour cannot be detected ahead of time, so a round table that fails part-way registers nothing and reports the failure (FR-22). | PRD |
| OQ-32 | Who is the user in a repo that several people work in? | The human who is prompting Claude in the active session. Each person is the user in their own session, and the repo's own review decides between people (section 2). | User (D3) for the definition. PRD for the review between people. |
| OQ-33 | Does a round table run in a session that no human prompts? | Yes, within the limits on a table an agent convenes and the daily cap (FR-21). Nothing that needs the user completes there. A repo that wants no unattended round table sets the cap to 0. Claude Code gives a skill no way to detect such a session, so the rule does not depend on detecting one. | PRD |
| OQ-34 | What happens to ADRs that a target repo already holds? | `init` leaves them untouched and lists them. The user folds one in through `intake` as a legacy record, with the existing file as its evidence (FR-32). | PRD |
| OQ-35 | Which votes make a round unanimous? | Five approve votes, or five reject votes. Five amend votes are not unanimous (FR-18). | PRD |
| OQ-36 | Does version 1.0 support native Windows? | No. It supports macOS, Linux, and WSL, and the README says so (FR-54). | PRD |
| OQ-37 | Which name goes on the copyright line of the licence? | "The Avalon contributors", so that no person's name is needed (FR-49). | PRD |
| OQ-38 | On what terms does a target repo keep the text Avalon writes into it? | With no condition and no notice. The templates carry the MIT No Attribution licence (FR-49). | PRD |
| OQ-39 | Which tracked files reach a user who installs? | Only the plugin. It moves into a subfolder that the marketplace file at the root names (FR-52). This changes REQ-224, and the change takes effect when the user signs this PRD off. | PRD |
| OQ-40 | Which code of conduct applies, and where do conduct reports and security reports go? | The Contributor Covenant, version 3.0. Security reports go through GitHub's private vulnerability reporting. Conduct reports go through the same private form, marked as conduct reports, because it is private to the maintainers and publishes no address. A report about a maintainer goes to GitHub's own abuse report. GitHub's docs say its content reports reach repo admins only in a repo that an organization owns (FR-51). | PRD. The user may supply a dedicated address in its place. |
| OQ-41 | Which version scheme applies, and where do release notes live? | Semantic versioning, written as `v1.2.3`. A `major`, `minor`, or `patch` label on the pull request sets the next version, and a release workflow publishes it on merge (FR-59). Notes live in GitHub Releases. | User (D5) for the scheme, the labels, and the workflow. PRD for the notes. |
| OQ-42 | No test may use git. What proves the nine script scenarios that describe git, and the code that reads git? | Every git read sits behind one boundary. The three kinds of test prove the scenarios against a fake. A fourth suite, the contract tests, proves the boundary against real git in a throwaway repo, with no network, as a run of its own (FR-55). | PRD. It narrows D6. |
| OQ-43 | Where do the 12 plugin scenarios and the scored cases run? | In a fifth suite, the plugin evals. It is a gate on a pull request that changes a skill, an agent file, the hook, or a template, with a cost limit on each run. A pull request from a fork gets no credential, so a maintainer moves it to a branch of the Avalon repo (FR-58). | PRD |
| OQ-44 | How does a released version reach the plugin manifest? | It does not. The manifest sets no version, an install follows the commit on `master`, and every commit there is a release. The tag and the GitHub release carry the number (FR-52). GitHub's docs, as read on 2026-11-11, give a workflow no way past a rule that requires pull requests in a repo that a person owns, and architecture confirms this. The alternative is that every pull request carries the number. | PRD |
| OQ-45 | What happens when a git merge joins two branches that each changed laws or ADRs? | One script command joins them. It keeps every row, gives the next free number to the law or ADR that is not yet on the shared branch where two collide, and refuses when both changed the same law. This narrows REQ-032 (FR-60). | PRD |
| OQ-46 | The recorded install commit can fall outside the history after a squash merge or a rebase. What does the legacy test read? | The repo as it stood before the install landed: the commit before the one that added the config file, or the current commit while the config file is not committed yet. The recorded install commit stays as a record, written once and covered by the checksum. This changes REQ-142 (FR-25). | PRD. The story work raised it. |

**Answers for the user to look at first**

- **They change `SPEC.md`.** OQ-25 changes REQ-103 and REQ-243 and widens REQ-273 to REQ-276. OQ-39 changes REQ-224. OQ-27 changes REQ-076. OQ-45 narrows REQ-032. OQ-46 changes REQ-142. OQ-21 makes an exception to REQ-126. OQ-14, OQ-15, OQ-19, and OQ-45 add to the script's commands.
- **They narrow or extend something the user said.** OQ-42 lets one suite start git, and OQ-43 lets one suite use the network. OQ-44 keeps the version out of the plugin manifest. OQ-27 caps the round tables that agents convene. FR-57 adds a second exception to the rule on grab-bag directories.
- **One has a working answer the user may want to replace.** OQ-40 sends conduct reports to the repo's private reporting form until the user supplies a dedicated address.

**What remains is work, not questions**

- The user reviews the wording of each engineering standard in build step 1, as REQ-303 requires (FR-47).
- `SPEC.md` takes in the changes that `addendum.md` section 6 lists.
- Acceptance scenarios prove the Claude Code behaviours that the docs leave unstated: the permission prompt in each permission mode (FR-20), and the plugin evals in CI (FR-58).

## 13. Assumptions and Directions

The first draft carried seven assumptions. On 2026-11-11 the user gave nine directions, asked one question, and asked that each assumption be reasoned to a position.
The user then asked that every open question be reasoned and answered. Section 12 holds the answers.

**What the user said**

- **D1.** A direction: the repo is public. The PRD covers what that requires, such as the MIT licence and the other files a public repo carries.
- **D2.** A question about Python: can the script run in a virtual environment?
- **D3.** A direction: the user is the human who is prompting Claude, whether that is the maintainer or someone who has downloaded the plugin. It is the active user interacting with Claude.
- **D4.** A direction: CI gates run only on a pull request into `master`, and only when it is open for review and not a draft. A more recent push cancels the gates still running. The gates do not run on a merge or a push to `master`, with one exception, the release workflow.
- **D5.** A direction: a release workflow releases a new version of the code, with semantic versioning in the form `v1.2.3`. A `major`, `minor`, or `patch` label on the pull request sets which version comes next, and a CI check ensures that a label exists.
- **D6.** A direction on code and tests: test-driven development; tests in Arrange, Act, Assert form; unit tests that use mocks to test only the unit, and that run fast; integration tests that reach the integration; end-to-end tests of full flows; unit and integration tests run separately; no git and no network in any test; 80% code coverage; linters, formatters, and type checkers; CPU time and memory weighed when tests are written; every test merits its existence; DRY and SOLID.
- **D7.** A direction: no grab-bag directories. When a directory becomes one, its files are grouped into subdirectories. The structure of the docs system is the exception, so ADRs stay in the `adr` directory. The user wants this to apply to any code or script written, and this PRD reads that as covering D6 as well.
- **D8.** A direction: the Avalon repo is bound by Avalon, and it holds its own laws, ADRs, and design docs.
- **D9.** A direction, given with the architecture work: the BMad output files, `BRIEF.md`, and `SPEC.md` are implementation plans and will not stay with the code. Real files created in the repo do not reference them or any code they define. Avalon is used in the Avalon repo as well as built in it, and its documents are the permanent files that may be referenced.
- **D10.** A direction, given with the architecture work: every Avalon document written for the Avalon repo follows the same process, even though the agents and the script do not exist yet. Laws and ADRs that the repo needs still go to the round table.

**What each assumption became**

"User" means the user stated the answer. "PRD" means this PRD reasoned it, and it stands until the user changes it.

| ID | The assumption | What it became | Basis |
|---|---|---|---|
| A1 | Avalon is a builder-led developer product, with rigor set for architecture and story work. | An open-source developer product in a public repo under the MIT licence, with rigor set for a public release (sections 0 and 4.12). | User (D1) |
| A2 | The user is one person who owns a repo and is its one decision-maker. | The user is the human who is prompting Claude in the active session: a role, not a person. Avalon keeps no identities, and the repo's own review decides between people (section 2). | User (D3) for the definition. PRD for what follows from it. |
| A3 | The journeys are structured from `BRIEF.md` and carry role names. | Kept. Role names are right, because the user is a role. Two journeys are added for the public release (section 2.3). | PRD |
| A4 | v1 is all of `SPEC.md`, delivered through eight build steps. | Version 1.0 is all of `SPEC.md` plus the public repo, the standards, the gates, and the release workflow. Steps 1 to 4 are the first slice, and every merge releases a version below 1.0 until the release gates pass (section 9). | PRD, with D5 for releases |
| A5 | The success metrics are proposals. | The release gates are binding. The other metrics are measured in the Avalon repo only and have no target before 1.0 (section 10). | PRD |
| A6 | The thesis sentence is this PRD's reading. | Kept as a summary. `BRIEF.md` states each of its parts (section 1). | PRD |
| A7 | The suggestions in OQ-1 to OQ-24, except OQ-13, are working defaults. | OQ-1 to OQ-9 are adopted as the shipped defaults. Every other question is answered in section 12, from the `SPEC.md` suggestion where one exists and from this PRD's reasoning otherwise. | PRD |

**The answer to D2.** The shipped script uses no virtual environment, and the development tools do.
A virtual environment isolates installed packages, and the shipped script has none.
It also runs on the interpreter that created it, so it neither supplies Python 3 nor settles which version a machine has.
FR-54 states the requirement, and `addendum.md` section 4 gives the reasoning and the case that would change the answer.
