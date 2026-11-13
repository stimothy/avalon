# Avalon: specification

This document states what Avalon must do.
It is derived from `BRIEF.md`, which holds the reasoning behind each choice.
A requirement here that disagrees with the brief is a defect in one of the two. It is reported, not worked around.

## How to read this spec

- Each requirement has a permanent ID of the form `REQ-001`.
  An ID is never reused and never renumbered. A removed requirement leaves a gap.
  A requirement or scenario added later takes the next ID, wherever it sits in the document.
- "Must" and "never" state a requirement. "May" states a permission.
- Each acceptance scenario in section 17 has an ID of the form `AC-01`.
- A requirement that names a cap or a list without giving its value takes the value from the config file.
  Section 18 lists every value and mechanism that the brief does not settle.
- A path that starts with `docs/` assumes the default root. Section 9 says how the root is chosen.

## 1. Scope

Avalon is a Claude Code plugin that gives any repo three kinds of governed document: laws, ADRs, and design docs.

It has two parts:

- **The plugin,** built in this repo: seven skills, ten agent files, one hook, one script, and the templates.
- **The docs in a target repo:** the generated docs tree, the config file, and a managed block in `CLAUDE.md`.

### Out of scope

- Planned work. Specs, briefs, and roadmaps live outside the system.
- A listing in an official plugin marketplace.
- Any write to git by the script or by the chair.
- Stopping an agent that sets out to forge a record. The guards stop shortcuts and accidents only.
- Checking full Mermaid syntax in a target repo.
- Choosing the root through an environment variable.
- A complete map of the repo through `covers`. A folder that no document covers is not an error.
- Removing the correlation between seats that run on related models. The design reduces it and does not remove it.

### Terms

| Term | Meaning |
|---|---|
| ADR | A living document that records one decision that is costly to reverse. |
| Archive | The file of every amended or removed law: `docs/laws/archive.md`. |
| Chair | The agent that runs a round table, decides, and registers the outcome. |
| Decision | A choice that passes the ADR test. |
| Law | A standing rule in the registry. It binds everything in the repo. |
| Ledger | The record of every round-table decision and every confirmation by the user: `docs/laws/ledger.md`. |
| Legacy | In the repo at the install commit. |
| Matter | What a round table decides: a law matter or a decision matter. |
| Registry | The table of every law in effect: `docs/laws/LAWS.md`. |
| Retired | Amended or removed, for a law. Deleted because it stopped applying, for an ADR. |
| Root | The folder in a target repo that holds the `laws/`, `adr/`, and `design/` folders. |
| Round table | Five seat agents and a chair that decide a matter in at most three rounds. |
| Script | The one command-line program that does every mechanical step. |
| Seat | A subagent that votes at a round table from one fixed perspective. |
| Session | The Claude Code session that asks for the work and owns the branch. |
| Target repo | A repo that Avalon is set up in. |
| The work | Whatever a repo exists to hold: source, manuscript, configuration, or prompts. |

## 2. The model

### Kinds and precedence

- **REQ-001** The system provides exactly three kinds of governed document: laws, ADRs, and design docs.
- **REQ-002** The system works for any repo, including an application, a service, a library, a story bible, and this repo.
  No format, template, or check assumes that the work is code.
- **REQ-003** Precedence is laws, then ADRs, then the work, then design docs.
- **REQ-004** Nothing may contradict a law.
- **REQ-005** An ADR must not contradict a law.
- **REQ-006** The work must not contradict a law or an ADR.
- **REQ-007** A design doc must not contradict the work, an ADR, or a law.
- **REQ-008** When two levels disagree, the lower one is corrected, or the higher one is changed through its own process.
- **REQ-009** Other agent instructions in the repo, such as `CLAUDE.md`, rank below laws.

### The two tests

- **REQ-010** A decision warrants an ADR only when both of these hold:
  - The choice is costly to reverse.
  - There were real alternatives, and a future reader would ask why this one won.
- **REQ-011** A rule warrants a law only when all of these hold:
  - It is stated as "must" or "never".
  - A reviewer can look at any piece of work and say whether it complies.
  - It applies to a class of work across the repo, not to one place.
  - It is expected to hold indefinitely.
  - It is worth its cost, given that every agent reads every law in every session.
- **REQ-012** A law that comes from an ADR names that ADR as its source. A law may also stand alone.

### Principles

- **REQ-013** A document holds only what is true at the time it is read. Replaced content is removed, not kept beside its replacement.
- **REQ-014** History lives only in ADR changelogs, the law archive, the ledger, and git.
- **REQ-015** Every line is true on its own.
  A line that states something no longer true, or never chosen, carries its marker on the same line.
- **REQ-016** Each fact has one home. Other documents link to it and do not restate it.
- **REQ-017** Unknown is written as unknown. A document never invents a rationale, a history, or an intent.
- **REQ-018** Only the registry and the `CLAUDE.md` block load in every session. Everything else is reached through an index, on demand.
- **REQ-019** Every document is plain markdown. An agent without the plugin can read and obey the docs.
- **REQ-020** The plugin is needed only to author and audit the docs.
- **REQ-021** Every repeatable step that needs no reasoning is a script command. A skill tells the agent which command to run.

## 3. Laws

### The registry

- **REQ-022** `docs/laws/LAWS.md` holds one table of every law in effect, and nothing that is not in effect.
- **REQ-023** The table has the columns `ID`, `Scope`, `Origin`, `Law`, and `Detail`, in that order. It has no status column.
- **REQ-024** The file opens with a statement that every law in the table is binding and that the whole table is read before any work.
  It also says to open a detail file only when the one-line law is not enough to act on.
- **REQ-025** A law is one sentence, within the length cap.
- **REQ-026** There is one registry file. It is never split.
- **REQ-027** Rows are in ID order, and a law that is added is always the last row.
- **REQ-028** `Scope` is a one-word tag from the fixed list in the config file.
  It never changes where a law lives or how the table is ordered.
- **REQ-029** `Detail` is empty, or it links to the law's detail file.

```markdown
| ID | Scope | Origin | Law | Detail |
|---|---|---|---|---|
| LAW-000001 | all | core | Nothing in this repo may contradict a law in this table. | |
| LAW-000010 | tests | user | Every test is structured as Arrange, Act, Assert. | [more](LAW-000010.md) |
| LAW-000011 | api | agent | Every public endpoint carries its version in its path. | |
```

### Law IDs

- **REQ-030** A law ID has the form `LAW-` followed by six digits, such as `LAW-000001`.
- **REQ-031** IDs come from a single sequence for the whole repo. The sequence counts archived laws.
- **REQ-032** An ID is permanent and carries no meaning. It is never reused and never changes.
- **REQ-033** The category of a law lives in the `Scope` column, never in the ID.

### Origin

- **REQ-034** `Origin` is one of three values, and all three bind equally.

| Origin | Meaning |
|---|---|
| `core` | Shipped with the system and seeded at install. |
| `user` | Proposed by the user, or confirmed by the user after an agent proposed it. This includes a law registered by user override. |
| `agent` | Proposed by an agent and adopted by the round table without the user. |

- **REQ-035** The user turns an `agent` law into a `user` law by confirming it.
  The text does not change, and no round table sits.

### Detail files

- **REQ-036** A law has a detail file only when one sentence cannot carry it.
- **REQ-037** The file is named for the law, such as `docs/laws/LAW-000010.md`.
- **REQ-038** Its frontmatter names the law, and the source ADR if there is one. It never names the law it replaced.
- **REQ-039** Its body has four parts:
  - **Meaning:** what the law requires, in plain terms.
  - **Applies to:** where it applies, and any exceptions.
  - **Examples:** one that complies and one that violates.
  - **Enforcement:** how a violation is detected.
- **REQ-040** A working agent opens a detail file only when it cannot act on the one-line law alone.
- **REQ-314** A detail file is part of its law. The chair drafts it before round 1, and the seats vote on the law and its detail file together.
- **REQ-315** After a law is adopted, its wording and its detail file change only by amendment.

### The archive

- **REQ-041** `docs/laws/archive.md` holds every law that was amended or removed.
- **REQ-042** The archive is never loaded automatically. Its first line says that nothing in the file is in effect.
- **REQ-043** The table has the columns `ID`, `Status`, `Text`, `Date`, `Replaced by`, `Now in effect`, and `Reason`, in that order.
- **REQ-044** `Status` is `Amended` or `Removed`, and it sits on the same line as the law text.
- **REQ-045** An amendment creates a law with a new ID. The old row moves to the archive.
- **REQ-046** A removal moves the row to the archive with its reason.
- **REQ-047** `Replaced by` names the law that amended the row, or `none`. It never changes after it is written.
- **REQ-048** `Now in effect` names the law at the end of the chain, or `none`. It is updated on every later amendment or removal in the chain.
- **REQ-049** Removing a law ends its whole chain. Every row in the chain then shows `none` as the law now in effect, and no earlier law is restored.
- **REQ-050** A return to an earlier wording is an amendment that restates that wording. It takes a new ID.
- **REQ-051** When a law is amended or removed, its detail file is deleted.

```markdown
| ID | Status | Text | Date | Replaced by | Now in effect | Reason |
|---|---|---|---|---|---|---|
| LAW-000012 | Removed | Every module has a README. | 2027-01-14 | none | none | Design docs made it redundant. |
| LAW-000013 | Amended | Unit tests are structured as Arrange, Act, Assert. | 2026-12-01 | LAW-000019 | LAW-000031 | Widened to all tests. |
| LAW-000019 | Amended | All tests are structured as Arrange, Act, Assert. | 2027-03-10 | LAW-000031 | LAW-000031 | Exempted generated tests. |
```

### Citing a retired law or ADR

- **REQ-052** Nothing in the repo may cite an amended or removed law by its ID, except the archive and the ledger.
- **REQ-053** The rule covers every tracked text file: the work, ADRs and their changelogs, design docs, law detail files, `CLAUDE.md`, and code comments.
- **REQ-054** Nothing may cite a retired ADR by its number, except the archive and the ledger.
  A citation is the form `ADR-0003` or the ADR's file name.
- **REQ-055** An agent fixes each citation, not the script.
  A citation of an amended law is rechecked against the law in effect. A citation of a removed law is deleted.
- **REQ-056** A law change is not complete until the lint passes.

### The ledger

- **REQ-057** `docs/laws/ledger.md` records every decision a round table makes, one row per decision.
  That covers every decision on a law and every decision on an ADR, including a rejection.
- **REQ-058** The ledger is never loaded automatically.
- **REQ-059** The script appends to the ledger. Nothing else writes it.
- **REQ-060** The table has the columns `Date`, `Decision`, `Proposed by`, `Decided by`, `Rounds`, `Tally`, and `Dissent`, in that order.
- **REQ-061** `Proposed by` is `user` or `agent`. `Decided by` is `table`, `user override`, or `user`.
- **REQ-309** `Decided by` is `user` only for a confirmation: the user confirms an `agent` law or an `agent` ADR, and no table sits.
  The ledger records each confirmation as one row.
  That row has `none` for `Rounds`, `Tally`, and `Dissent`, and `Proposed by` keeps the original proposer.
- **REQ-062** `Dissent` names each seat that voted against the decision that was made, with its reason, or `none`.
- **REQ-063** A decision that reached the table late, after its effect landed, says so in its ledger row.
- **REQ-316** A legacy record and the install record of ADR `0002` get no ledger row.

```markdown
| Date | Decision | Proposed by | Decided by | Rounds | Tally | Dissent |
|---|---|---|---|---|---|---|
| 2026-12-01 | Amended LAW-000013 to LAW-000019 | agent | table | 1 | 5 approve, 0 amend, 0 reject | none |
| 2027-01-20 | Added LAW-000024 | user | user override | 3 | 2 approve, 0 amend, 3 reject | Skeptic, Jurist, Steward: it overlaps LAW-000010. |
| 2027-02-02 | Rejected: functions are at most 20 lines | agent | table | 3 | 1 approve, 0 amend, 4 reject | Practitioner: wanted a softer cap. |
| 2027-03-02 | Reversed ADR-0003: Vitest replaces Jest | user | table | 1 | 4 approve, 0 amend, 1 reject | Steward: the migration cost is not justified. |
```

### The tally format

- **REQ-064** A tally is written as labelled counts, such as `4 approve, 0 amend, 1 reject`. This is the only form used anywhere.
  A ledger row with no vote holds `none` in place of a tally.
- **REQ-065** The order is always approve, amend, reject.
- **REQ-066** Every count is written, including a zero.
- **REQ-067** The counts are the votes of the last round held, and they add up to five.
- **REQ-068** A bare pair of numbers, such as `4-1`, is never used.
- **REQ-069** The script writes the tally from the recorded votes. No agent types it by hand.

### The law budget

- **REQ-070** The config file sets a soft cap on the size of the registry.
- **REQ-071** When a proposal would exceed the cap, the round table must also name laws to merge or remove, or state why none can go.
- **REQ-072** The cap never blocks registration. A law the table adopts is registered either way.

## 4. The round table

### When a table sits

- **REQ-073** A law is created, amended, or removed only through a round table.
- **REQ-074** A decision that is being made goes to a round table before it is carried out.
  That covers a new decision, the reversal of a decision in effect, and the retirement of one, whoever proposes it.
- **REQ-075** The user or any agent may propose a matter.
- **REQ-076** An agent convenes a table by invoking the `law` or `adr` skill. It does not wait for the user.
- **REQ-077** The laws and ADRs in effect bind every agent until the table decides.
- **REQ-078** Related proposals may be heard together as a slate in one sitting, with a separate vote on each.

### The chair

- **REQ-079** A dedicated chair agent runs every table and spawns the seats.
- **REQ-080** Whoever proposes a matter never chairs it.
- **REQ-081** The chair works in its own context. It returns only the outcome and the list of files that changed.
- **REQ-082** The chair is impartial. It weighs the arguments and does not argue for the proposal.

### The seats

- **REQ-083** Five seats sit at every table, each with one perspective.
- **REQ-084** The Practitioner, Skeptic, Jurist, and Steward sit on every matter.
  The Enforcer is the fifth seat on a law matter. The Scout is the fifth seat on a decision matter.
- **REQ-085** Each seat asks the questions in this table.

| Seat | Sits on | Asks about a law | Asks about a decision |
|---|---|---|---|
| Practitioner | Both | Can an agent follow this in daily work? What does it cost? | What is it like to build on this choice every day? |
| Skeptic | Both | Is this needed? Is it a law at all, or an ADR, a design note, or a lint rule? | Is a decision needed at this point? It argues for the strongest alternative, including doing nothing. |
| Jurist | Both | Does it conflict with, duplicate, or leave a loophole in existing laws and ADRs? | Does it conflict with a law or with another ADR? |
| Steward | Both | What does this lock in? Who pays for it a year later? | What does this lock in? Who pays for it a year later? |
| Enforcer | Laws | Can a violation be detected? Would two readers reach the same verdict? | Does not sit. |
| Scout | Decisions | Does not sit. | Were the real alternatives considered? What would it take to undo this choice? |

- **REQ-086** The Steward takes the lens of the repo's domain, such as an architect for a service or a continuity editor for a story bible.
- **REQ-087** A seat cannot write a file or spawn an agent.

### The process

- **REQ-088** **Screening.** The chair applies the law test to a law proposal and checks every proposal for duplicates and conflicts.
- **REQ-089** The chair frames a law proposal as new, as an amendment of a named law, or as a removal of a named law.
- **REQ-090** When a removal targets a law that has earlier versions, the chair shows the chain.
  It confirms whether the proposer means removal or a return to an earlier wording.
- **REQ-091** The chair turns away a repeat of a rejected proposal that brings no new argument.
- **REQ-092** The prose editor reviews the wording, and any draft detail file, before each round.
- **REQ-093** **Round 1.** The seats vote in parallel, and no seat sees another seat's vote.
- **REQ-094** A vote is approve, amend with proposed wording, or reject. Each vote carries a short reason.
- **REQ-095** The chair records the votes of each round through the script, and the script tallies the round.
- **REQ-096** **Rounds 2 and 3.** If a round is not unanimous, the chair revises the text and circulates every vote and reason. The seats then vote again.
- **REQ-097** There are at most three rounds.
- **REQ-098** The chair sends each later round to the same five seat agents by message. It does not start new ones.
- **REQ-099** The chair's message asks each seat whether the revision resolves its objection.
  The message says that changing a vote is expected when it does.
- **REQ-100** If a seat cannot be resumed, the chair starts a new one. The packet gives that seat its earlier votes and reasons.
- **REQ-101** **Decision.** On a unanimous vote, or after round 3, the chair decides: adopt, adopt with final edits, or reject.
- **REQ-102** The chair weighs the arguments. It does not simply count votes.
- **REQ-103** **Registration.** For a law, the chair runs the script's law command, and writes the detail file that the seats approved, if the law has one.
- **REQ-104** For a decision, the chair records the ledger row through the script, and the `tech-writer` then writes the ADR.
- **REQ-105** **Hand-back.** The chair never commits.
  The session that asked for the table commits the files, following the conventions of the repo and its own instructions.
- **REQ-106** Where the repo's conventions allow, a law change is a commit of its own.

### The user's authority

- **REQ-107** The user has the final say on every law and every decision.
- **REQ-108** The table still sits on a proposal from the user.
- **REQ-109** If the table would reject or reword the user's proposal, the chair registers nothing.
  It returns its objection, with a counter-proposal if it has one, and asks the user to confirm.
- **REQ-110** The user then chooses one of three things: accept the outcome, make a counter-proposal that goes back to the table, or direct that the proposal be registered as written.
- **REQ-111** A law or decision registered over the table's objection is marked `user override` in the ledger.

### Agent proposals

- **REQ-112** The chair's decision on an agent's law proposal is registered at once, with origin `agent`.
- **REQ-113** A table convened by an agent may create a law, and may amend or remove a law of origin `agent`.
- **REQ-114** For a law of origin `user` or `core`, a table convened by an agent registers nothing.
  The chair returns the table's recommendation and waits for the user to confirm.
- **REQ-115** A table convened by an agent may adopt a new decision, which takes origin `agent`. It may reverse an ADR of origin `agent`.
- **REQ-116** For an ADR of origin `user`, a table convened by an agent changes nothing.
  The chair returns the table's recommendation and waits for the user to confirm.
- **REQ-117** An agent cannot override the table. Only the user can.
- **REQ-118** An agent names every law change and every decision it caused in its final report.

### Nesting depth

- **REQ-119** The chain is session, then chair, then seats, which is two layers of subagent.
- **REQ-120** A first-layer subagent may invoke the `law` or `adr` skill and seat a full table. The seats then run at the third layer.
- **REQ-121** A subagent at the second layer or deeper hands its proposal up to the agent that spawned it.
- **REQ-122** The round table requires `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` to be at least 2 when the session convenes it, and at least 3 when a first-layer subagent does.

## 5. ADRs

### The file

- **REQ-123** An ADR is a living document about one decision topic. It is edited in place and always states the decision in effect.
- **REQ-124** No ADR is ever marked superseded.
- **REQ-125** The file name is a four-digit number and a topic, such as `docs/adr/0003-test-framework.md`.
- **REQ-126** Numbers are sequential and are never reused.
- **REQ-127** Every ADR in the directory is in effect. A proposal lives in a branch, not in the docs.
- **REQ-128** The frontmatter holds `adr`, `summary`, `covers`, and `origin`.
  - `summary` states the decision in effect.
  - `covers` lists the paths the decision governs.
  - `origin` is `user` or `agent`. A legacy decision and a user override have origin `user`.
- **REQ-129** The body has these sections, in order: Context, Decision, Consequences, Alternatives rejected, Changelog.
- **REQ-130** Each line under "Alternatives rejected" carries the word "Rejected" on the same line as the alternative.

```markdown
---
adr: 0003
summary: Unit tests use Vitest. End-to-end tests use Playwright and run on every pull request.
covers: [tests/**, vitest.config.ts, playwright.config.ts]
origin: user
---
# ADR-0003: Test framework

## Context
## Decision
## Consequences
## Alternatives rejected
- **Rejected: Cypress.** Slower in CI at our suite size.
- **Rejected: Jest.** It was the first choice for unit tests. Vitest shares config with the build.

## Changelog
- 2026-11-10 (user, table): Created.
- 2027-03-02 (user, table): Replaced Jest with Vitest for unit tests, to share config with the build.
```

### The changelog

- **REQ-131** The changelog is the last section of the ADR. Each line has a date, a marker, and a one-line summary of the change.
- **REQ-132** The marker is one of these six.

| Marker | Meaning |
|---|---|
| `(legacy)` | The decision predates the system. It was recorded with no table. |
| `(user)` | The user added detail, confirmed an agent's decision, or adopted the system at install. No table was needed. |
| `(agent)` | An agent added detail. No table was needed. |
| `(user, table)` | The user proposed or confirmed a decision, and the table agreed. |
| `(agent, table)` | An agent proposed a decision, and the table adopted it. |
| `(user override)` | The user directed a decision over the table's objection. |

### Changing an ADR

- **REQ-133** When a decision changes, the body is rewritten to state the decision in effect.
  The old choice moves into "Alternatives rejected", with the reason it was left.
  The changelog gets one dated line.
- **REQ-134** When a decision stops applying, the ADR is retired and the file is deleted.
  The ledger row of the retirement is its record. It names the number, the title, and the reason.
  The index keeps no list of retired ADRs.
- **REQ-310** Retiring an ADR follows the rules for a reversal.
  A table sits first, the user has the final say, and a table convened by an agent cannot retire an ADR of origin `user` without the user's confirmation.
- **REQ-311** `adr retire` deletes the file, appends the ledger row, and prints every citation of the retired number.
- **REQ-135** Anyone may add detail to an ADR without changing the decision in effect. No table sits.
- **REQ-312** The user turns an `agent` ADR into a `user` ADR by confirming it.
  The decision does not change, no table sits, and the changelog gets a `(user)` line.
- **REQ-136** Before a table sits on a new decision, the `adr` skill applies the ADR test. A new decision that fails the test gets no table and no ADR.
  A reversal or a retirement of an ADR in effect always gets a table.
- **REQ-137** The `adr` skill prefers revising an existing ADR to creating one.
- **REQ-138** A rejected decision is logged in the ledger and leaves no line in any ADR.
- **REQ-139** After a decision is adopted, the `adr` skill asks whether it implies a law. If it does, that law goes to the table as a proposal of its own.

### Legacy decisions

- **REQ-140** Legacy means in the repo before the system was installed. It has no other meaning.
- **REQ-141** `scaffold` writes the install time, and the commit it ran on, into the config file. It writes them once.
- **REQ-142** A decision is legacy only when the decision itself was in effect in the repo at the install commit.
  A covered area that existed at install does not make a decision about it legacy. All three of these must hold:
  - Every `covers` entry of the ADR matches a path that existed at that commit. The script checks this. It shows only that the area existed.
  - The ADR's frontmatter holds `evidence`: at least one file that shows the decision in effect at that commit. The script checks that each file existed at that commit.
  - The user confirms that the decision predates the install.
- **REQ-317** When the evidence or the user's confirmation is missing, the decision is not recorded as legacy. It goes to the table as a late decision.
- **REQ-143** A legacy decision is only recorded. No table sits, its origin is `user`, and its changelog line carries `(legacy)`.
- **REQ-144** A legacy decision may be recorded at any time after install. The test is the same.
- **REQ-145** A decision that landed after the install time is never legacy, even if it landed without an ADR. It goes to the table late.
- **REQ-146** The lost reasons of a legacy decision are written as unknown.

## 6. Design docs

- **REQ-147** A design doc describes the repo as it is: what it is, what it does, and how its parts fit together.
- **REQ-148** A design doc has no changelog. Its history is in git only.
- **REQ-149** A design doc describes the present only.
- **REQ-150** The frontmatter holds `summary`, `covers`, `verified`, and `verified_commit`.
  - `summary` says what the doc covers and when to read it.
  - `covers` lists the paths in the work that the doc describes.
  - `verified` is the date the doc was last checked against those paths.
  - `verified_commit` is the commit that was checked out when the doc was verified.
- **REQ-151** The `verified` and `verified_commit` values are the doc's stamp.
  A design doc is stale when a covered path changed after its stamp landed.
  That covers every commit that is reachable from `HEAD` and not from the commit in which the stamp landed, and every uncommitted change to a covered path.
  A doc whose stamp is not yet committed is not stale. The script lists every stale design doc.
  `verified_commit` records what was checked and makes each stamp distinct. The staleness rule does not compute from it.
- **REQ-313** On a shallow clone, `stale` and the legacy test refuse to run and say why.
- **REQ-152** An agent reviews each listed doc, updates it if needed, and resets the stamp through the script.
- **REQ-153** A change that makes a design doc untrue updates that doc in the same change.

```markdown
---
summary: How users sign in and how sessions are kept. Read it before changing login or tokens.
covers: [src/auth/**]
verified: 2026-11-10
verified_commit: 3f9c2ab
---
# Authentication
```

### The glossary

- **REQ-154** `docs/design/glossary.md` defines the terms a reader needs to follow the repo. It is a design doc.
- **REQ-155** It is one table with the columns `Term` and `Meaning`, with one term per row, in alphabetical order.
- **REQ-156** It is the one home for a definition. Other documents link to it and do not define the term again.
- **REQ-157** It holds terms that are specific to the repo, or used in a special sense. It does not define general vocabulary.
- **REQ-158** A meaning is one or two sentences. A longer explanation belongs in a design doc, and the row links to it.
- **REQ-159** A known synonym is named in the row.
- **REQ-160** The glossary is never loaded automatically.
- **REQ-161** The document size cap does not apply to the glossary.
- **REQ-318** The document size cap applies to ADRs, design docs, and law detail files only.
  The registry, the archive, the ledger, and the two indexes are exempt, because each is a table that grows by design and cannot be split.
  The registry has its own soft cap, the law budget.
- **REQ-162** The glossary never holds a rule. A definition that tells an agent what it must do is a law, and goes to the round table.

## 7. Frontmatter and indexes

- **REQ-163** Frontmatter holds only the facts about a document that the script needs. It holds nothing that the body also states.
- **REQ-164** The script reads and writes frontmatter fields.
- **REQ-165** `docs/adr/README.md` and `docs/design/README.md` are the indexes.
  Each lists every document in its folder with one line.
- **REQ-166** The script generates both indexes from the `summary` fields. They are never written by hand.

### The `covers` field

- **REQ-167** A `covers` entry is a glob at folder level, such as `src/auth/**`.
  A single file is listed only when it stands alone, such as a config file.
- **REQ-168** A document has at most five `covers` entries.
- **REQ-169** A document that needs more than five entries is split.
- **REQ-170** A broad document uses a shallow glob. The overview matches only the top level of the repo.
- **REQ-171** An entry that matches no path is an error.

## 8. Writing standard

- **REQ-172** The standard applies to every document in the system.
- **REQ-173** The standard ships as the detail file of a core law. The doc-writing skills and agents load it, and other sessions do not.

### Prose

- **REQ-174** A document has one subject. The title names it and the summary states it.
- **REQ-175** Material goes into the document that owns its subject. A document is created only when no document owns the subject.
- **REQ-176** A document is split when it covers more than one subject or passes the size cap.
  A split leaves no stub, and the links and the index are updated.
- **REQ-177** A sentence holds one idea. Parallel items become a list, and comparisons become a table.
- **REQ-178** A paragraph holds one point and breaks where a reader would expect. It has no length cap.
- **REQ-179** An edit is woven in, not appended.
  The writer rewrites the paragraph, splits it, or adds one, so that the passage reads as if it were written in one sitting.
- **REQ-180** Documents use the present tense. A word that places something in time, such as "previously", "new", or "now", appears only in a changelog.
  The prose editor judges whether a word is used in that sense. The registry, the archive, and the ledger are exempt, because the script writes them.
- **REQ-181** A reader who has never seen the repo can follow each document.
  A term is defined once, in the glossary, and linked after that.

### Diagrams

- **REQ-182** ADRs and design docs may hold diagrams.
- **REQ-183** A diagram is written in Mermaid, in a fenced block inside the document.
- **REQ-184** A sentence before the diagram says what it shows.
- **REQ-185** The diagram is the home for what connects to what. The prose says why, and what each part does.
- **REQ-186** A diagram shows only the present. It never draws a rejected alternative or an earlier design.
- **REQ-187** A diagram has at most about fifteen nodes. A larger one is split, or its document is.
- **REQ-188** The allowed diagram types are flowchart, sequence, state, and entity-relationship.

### Images

- **REQ-189** Design docs may hold images. ADRs may not.
- **REQ-190** An image is used only for what Mermaid cannot draw, such as a screenshot, a mock-up, a map, a sketch, or artwork.
- **REQ-191** Images live in `docs/design/assets/`. A file is named for its document and its subject, such as `overview-site-map.png`.
- **REQ-192** Every image has alt text that says what it shows.
- **REQ-193** An image never carries a fact that the text lacks.
- **REQ-194** When a design doc is reviewed as stale, the reviewer opens its images too.
- **REQ-195** An image is within the size cap and in one of the allowed formats.

## 9. Layout and loading

### The tree

- **REQ-196** A target repo holds only the generated docs, the config file, and the `CLAUDE.md` block.
- **REQ-197** The docs tree has this layout under the root.

```text
docs/
  laws/
    LAWS.md        registry, always read in full
    archive.md     amended and removed laws; never loaded automatically
    ledger.md      every round-table decision and confirmation; never loaded automatically
    LAW-000010.md  detail file, only for laws that need one
  adr/
    README.md      generated index
    0001-architecture.md
    0002-documentation-system.md
  design/
    README.md      generated index
    overview.md
    glossary.md
    assets/        images used by design docs
.avalon.yml        at the top of the repo
```

### The root and the config file

- **REQ-198** The plugin is installed once, for the user. The system is then set up in each repo by `init`.
- **REQ-199** The root is a per-repo setting. It is resolved in this order:
  1. The repo's config file.
  2. The plugin's `default_root` option.
  3. `docs/`.
- **REQ-200** No environment variable sets the root.
- **REQ-201** The config file is `.avalon.yml` at the top of the repo. Its path is fixed, so the script finds it without knowing the root.
- **REQ-202** The config file holds the root path, the repo profile, the system version, the install time, the install commit, the caps, and the scope list.
- **REQ-203** The three folders sit beside any docs that are already in the root.
- **REQ-204** `init` never writes into a folder that holds content it did not create. On a clash it proposes another root, such as `docs/avalon/`.
- **REQ-205** `init` warns when a site generator publishes the whole of `docs/`, and suggests another root.
- **REQ-206** Changing the root is one script command.
  It moves the tree and rewrites the config file, the `CLAUDE.md` block, and every link.

### How agents load the docs

- **REQ-207** Install writes a managed block into `CLAUDE.md`, between the markers `<!-- avalon:start -->` and `<!-- avalon:end -->`.
  The script rewrites only what is between the markers.
- **REQ-208** The block imports the registry with an `@` import, so the registry loads in every session without a hook and without the plugin.
- **REQ-209** The block holds the text below, with each path following the root.

```markdown
<!-- avalon:start -->
@docs/laws/LAWS.md

- The laws above are binding. If no table of laws appears above, read `docs/laws/LAWS.md` in full before anything else.
- Precedence: laws > ADRs > the work > design docs.
- Before your first change, read `docs/design/overview.md`.
- Before changing an area, read its ADR. The index is `docs/adr/README.md`.
- For a term you do not know, search `docs/design/glossary.md`.
- If you find a contradiction, or are asked to break a law or an ADR, stop that part of the work and report it with the ID.
- Laws change only through the law skill. Outside that skill, never edit a file in `docs/laws/`.
<!-- avalon:end -->
```

- **REQ-210** The same block may go in `AGENTS.md`, with a "read this file in full" instruction in place of the import.

## 10. When things conflict

- **REQ-211** An agent never resolves a conflict silently and never works around a law or an ADR.
- **REQ-212** An agent handles each conflict as this table says.

| Conflict | What the agent does |
|---|---|
| A design doc disagrees with the work | Updates the design doc. |
| The work disagrees with an ADR | Reports it. Either the work is fixed, or the decision really changed and the ADR is revised. |
| An ADR disagrees with a law | Reports it. Either the ADR is revised, or an amendment goes to a round table. |
| A task requires breaking a law | Stops that part of the task and names the ID. It may take an amendment to a round table. The law binds until the table decides. |
| A task requires breaking an ADR | Stops that part of the task and names the ID. It may take a reversal to a round table. The ADR binds until the table decides. |
| The work already violates a law when it is found | Reports it. Fixes it only if that is inside the task. |

## 11. The core set

- **REQ-213** Every target repo gets the same starting set: the core laws, two core ADRs, and two core design docs.
  Section 18 lists the one open case: a repo that is empty at install.
- **REQ-214** The script copies the core laws verbatim. An agent that reads the repo writes the core ADRs and design docs during `init`.
- **REQ-215** The core laws are the nine below. Their text is a draft until this repo's own round tables ratify it.
  Each is seeded with origin `core`. LAW-000009 links to its detail file, which holds the writing standard.

| ID | Scope | Law |
|---|---|---|
| LAW-000001 | all | Nothing in this repo may contradict a law in this table. |
| LAW-000002 | all | Precedence is laws, then ADRs, then the work, then design docs; when two disagree, the lower one is corrected or the higher one is changed through its own process. |
| LAW-000003 | laws | A law is created, amended, or removed only by a round table. |
| LAW-000004 | all | A contradiction, or a request that would break a law or an ADR, is reported with its ID and never silently resolved or worked around. |
| LAW-000005 | docs | Docs state only what is true now; replaced content is removed, and history lives in ADR changelogs, the law archive, the ledger, and git. |
| LAW-000006 | docs | Docs state only what the repo shows or the user has said; unknowns are written as unknown. |
| LAW-000007 | adr | After install, a decision that meets the ADR test goes to the round table before it is carried out, and is recorded in an ADR when it is adopted. |
| LAW-000008 | design | A change that makes a design doc untrue updates that doc in the same change. |
| LAW-000009 | docs | Every doc follows the writing standard. |

- **REQ-216** `0001-architecture.md` records the load-bearing structure of the repo: its form, its major parts and their boundaries, and its primary technologies or formats.
  Reasons are given where they are known and marked unknown where they are not.
- **REQ-217** `0002-documentation-system.md` records the decision to adopt this system, with the root path and any local settings.
  It is the user's decision, made by running `init`. `init` records it with origin `user` and the marker `(user)`, and no table sits.
  The decision is made at install, and the law on decisions applies after install.
- **REQ-218** `init` lists the other decisions it found in the repo that pass the ADR test but have no record. The user chooses which to write.
- **REQ-219** `overview.md` is required. It contains these sections, and a section that does not apply is left out, not left empty:
  - what the repo is, in one paragraph
  - its purpose and audience
  - what it does or contains
  - its main parts and how they relate
  - a map of the repo
  - how to work in it
- **REQ-220** `glossary.md` is required. It starts with the system's own terms, such as law, ADR, round table, ledger, legacy, and the work.
  `init` adds the terms it finds in the repo.
- **REQ-221** The overview links to the glossary and keeps no term list of its own.
- **REQ-222** `init` suggests further design docs from the repo profile, such as interfaces and data for a service, or characters and timeline for a story bible.

## 12. The plugin

### Packaging and install

- **REQ-223** The system ships as a Claude Code plugin named `avalon`.
- **REQ-224** This repo is both the marketplace and the plugin. Its marketplace file lists one plugin whose source is the repo root.
- **REQ-225** The plugin installs from this repo on GitHub with `claude plugin marketplace add <owner>/<repo>` and `claude plugin install <plugin>@<marketplace>`.
- **REQ-226** The plugin loads for one session from a local checkout with `claude --plugin-dir <path>`.
- **REQ-227** `claude plugin validate .` passes before a release.
- **REQ-228** The plugin has no `bin/` directory.
- **REQ-229** The plugin declares the option `default_root`, which the user sets once.

### Names

- **REQ-230** Every name is scoped to Avalon, so nothing collides with another plugin or with a repo's own files.
- **REQ-231** A skill is invoked as `/avalon:<skill>`. A skill file sets no `name` field, so no skill has a bare command.
- **REQ-232** An agent is always spawned by its full name, such as `avalon:tech-writer`, and never by its bare name.
- **REQ-233** The script is one file named `avalon`. It is called by its path inside the plugin, through `${CLAUDE_PLUGIN_ROOT}`, and it is not put on the PATH.

### Platform facts the design depends on

Each fact below was checked against the Claude Code docs, except where it says otherwise.

- A subagent can spawn subagents, up to three layers below the main session by default.
- An agent file sets its model, effort, and tools in frontmatter. A plugin's agent files ignore `hooks`, `mcpServers`, and `permissionMode`.
- A subagent that has the `SendMessage` tool can resume a subagent it spawned. The docs state this for interactive sessions only.
- A subagent receives `CLAUDE.md`. The built-in Explore and Plan agents do not receive it.
- An `@` import in `CLAUDE.md` expands for a subagent. The docs imply this, and a live test confirmed it.
- A plugin's `PreToolUse` hook can deny Edit, Write, and Bash calls, in the main session and in subagents.
- **Not checked:** that a plugin cannot ship permission rules. The brief states it, and the hook is the blocking mechanism either way.
- On a shared bare name, a project or user agent outranks a plugin agent.
- **Not stated in the docs:** that the full `avalon:<agent>` name works as the Agent tool's agent type. Scenario AC-24 proves it.

## 13. Skills

- **REQ-234** The plugin ships seven skills. A skill is a procedure that runs in the session and calls agents and script commands.

| Skill | Does |
|---|---|
| `init` | Surveys the repo, sets its profile, seeds the core set, and writes the `CLAUDE.md` block. |
| `intake` | Takes a design, spec, or conversation and sorts it: law candidates and decisions to a round table, description to design docs. |
| `law` | Frames a proposal to create, amend, or remove a law, hands it to the chair, and reports the outcome. Records the user's confirmation of an `agent` law. |
| `adr` | Applies the ADR test, takes a decision to the chair, and records the outcome. Adds detail to an existing ADR without a table. Records the user's confirmation of an `agent` ADR. |
| `design` | Writes, updates, splits, and merges design docs. |
| `check` | Reports problems. Runs the lint, then an agent audit for contradictions between levels, then a prose review of every document. |
| `sync` | After work is done, reviews the changes and updates stale design docs. Flags unrecorded decisions and law violations. |

- **REQ-235** `init` is safe to run again on a repo that is already set up.
- **REQ-236** `init` seeds the glossary with the system's own terms and with the terms it finds in the repo.
- **REQ-237** `check` only reports. It changes no document.

## 14. Agents

- **REQ-238** The plugin ships the ten agent files below. Each file sets its own model, effort, and tools.

| Agent | Role | Called by | Writes files | Model | Effort |
|---|---|---|---|---|---|
| `chair` | Runs the round table, decides, and registers the outcome | `law`, `adr`, `intake`, `init` | Law files only | Opus | high |
| `seat-practitioner` | Seat, for laws and decisions | The chair | No | Sonnet | medium |
| `seat-skeptic` | Seat, for laws and decisions | The chair | No | Sonnet | high |
| `seat-jurist` | Seat, for laws and decisions | The chair | No | Opus | high |
| `seat-steward` | Seat, for laws and decisions | The chair | No | Sonnet | medium |
| `seat-enforcer` | Seat, for laws only | The chair | No | Sonnet | medium |
| `seat-scout` | Seat, for decisions only | The chair | No | Sonnet | high |
| `law-reviewer` | Checks work against the laws and ADRs | `check`, `sync`, or the user | No | Sonnet | high |
| `tech-writer` | Writes and edits ADRs and design docs | `adr`, `design`, `init`, `sync` | Docs only | Sonnet | medium |
| `prose-editor` | Reviews prose as a human reader would | The chair, `adr`, `design`, `init`, `sync`, `check` | ADRs and design docs only, nothing under `docs/laws/` | Sonnet | medium |

- **REQ-239** No agent file names Fable or Haiku.
- **REQ-240** The models and effort levels are starting values. They are tuned against the fixture repos.
- **REQ-241** `check` may raise the `law-reviewer` to Opus for a full audit.

### The chair

- **REQ-242** The chair's file holds the round-table procedure, the voting rules, and the vote format. They live nowhere else.
- **REQ-243** The chair is the only agent that writes law files.
- **REQ-244** The chair's file lists the `Agent` tool and the `SendMessage` tool.

### The seats

- **REQ-245** Each seat file holds only its perspective: what it cares about and what it asks.
  A seat that sits on both kinds of matter holds its questions for each.
- **REQ-246** A seat's file lists only read and search tools.
- **REQ-247** The chair seats five of the six files, by the kind of matter, and passes the voting rules and the vote format to each.

### The law reviewer

- **REQ-248** The law reviewer receives a diff or a path. It reports each violation with the ID, the location, and its confidence.
- **REQ-249** The law reviewer never fixes what it finds.
- **REQ-250** The law reviewer opens the detail file of every law in scope.

### The tech writer

- **REQ-251** The tech writer always loads the writing standard.
- **REQ-252** The tech writer decides whether to extend or create a document, when to split one, and how to word each line. It writes the Mermaid diagrams.
- **REQ-253** The tech writer words the content it is given. It makes no decision and invents no reason.
- **REQ-254** The tech writer never writes law files.

### The prose editor

- **REQ-255** The prose editor is given the document and not the conversation behind it. It reads as a reader who has never seen the repo.
- **REQ-256** It checks audience, clarity, flow, sentence structure, paragraph structure, punctuation, grammar, defined terms, and whether each line is true on its own.
- **REQ-257** It checks that each paragraph holds one point and that the latest edit was woven in.
  It restructures a paragraph that has grown by one addition after another.
- **REQ-258** It flags a repo-specific term that the glossary does not define, and a term that a document defines for itself.
  The `tech-writer` adds or moves the entry.
- **REQ-259** For ADRs and design docs, it fixes the prose directly and lists what it changed.
- **REQ-260** It never edits a file under `docs/laws/`.
  For the wording of a law, it returns suggested wording to the chair before the seats vote.
  For a law detail file, it returns its suggestions to the chair before the seats vote. After adoption it only reports.
- **REQ-261** It changes wording and never meaning.
  When a fix would change what a sentence says, or the meaning is unclear, it reports the passage instead of editing it.
- **REQ-262** Writing takes one pass: the writer writes, the editor edits, and the lint runs. The two agents do not go back and forth.
- **REQ-263** Under `check`, the prose editor reviews every document and only reports.

## 15. The script

- **REQ-264** One command-line script does every mechanical step. Agents never do these steps by hand.
- **REQ-265** The script runs on Python 3 with the standard library only.
- **REQ-266** The script changes files and prints the list of files it changed.

### Commands

- **REQ-267** The script provides these commands.

| Command | Does |
|---|---|
| `scaffold` | Creates the tree, copies the templates and core laws, writes the config file, and writes or refreshes the `CLAUDE.md` block. |
| `status` | Prints a short summary: the law count against the budget, stale design docs, and the lint result. |
| `law add`, `law amend`, `law remove`, `law reject`, `law confirm` | Allocates the ID and writes the registry row. Moves retired rows to the archive and updates every "now in effect" pointer in the chain. Deletes retired detail files. Appends the ledger row. `law confirm` changes the origin of an `agent` law to `user`. |
| `packet` | Assembles what a seat needs to vote into one file: the proposal with any draft detail file, the registry, and the related ADRs. For a later round it adds the earlier votes and reasons. |
| `vote`, `tally` | Records the votes of a round. Prints the result in the one tally format. |
| `for` | Lists the ADRs and design docs that cover a path. |
| `adr new`, `adr log`, `adr retire`, `adr confirm` | Allocates the number, creates the file from the template, and appends a dated changelog line. `adr retire` deletes the file, appends the ledger row, and prints every citation of the retired number. `adr confirm` changes the origin of an `agent` ADR to `user`. |
| `index` | Regenerates both indexes from the `summary` fields. |
| `stale`, `verify` | Lists the design docs that are stale under the stamp rule. Stamps a doc with the date and the current commit. |
| `lint` | Runs every check in "Lint checks" below. |
| `move-root` | Moves the tree and rewrites the config file, the `CLAUDE.md` block, and every link. |

- **REQ-268** `law amend` and `law remove` print every citation of the retired ID.
- **REQ-269** An agent runs `for` before it changes a file, and reads `status` instead of the files it summarizes.

### Git

- **REQ-270** The script never writes to git. It does not stage, commit, branch, tag, or push.
- **REQ-271** No command takes a commit message as an argument.
- **REQ-272** The script reads git for four things only:
  - history, for the staleness check
  - the install commit, for the legacy test
  - the current commit, when it records an install or stamps a design doc
  - the list of tracked files, for the lint

### Write guards

- **REQ-273** The script is the only writer of the registry, the archive, and the ledger.
- **REQ-274** A `PreToolUse` hook denies any Edit or Write call that targets those three files, in the session and in subagents.
- **REQ-275** The same hook inspects Bash commands that write to those files. This check is best-effort.
- **REQ-276** The script records a checksum of the three files each time it writes them. The checksum also covers the install time and the install commit.
- **REQ-277** The law and ADR commands refuse to register a law, or to record, reverse, or retire a decision, without a complete round of five recorded votes or a user override.
  A legacy decision must pass the legacy test instead. The install record of ADR `0002` needs neither, and the script accepts it once.

### Lint checks

`lint` fails on each of these, except where a check says that it only flags.

- **REQ-278** The registry or the archive does not match its table format.
- **REQ-279** A law ID is not unique, or does not have the `LAW-` six-digit form.
- **REQ-280** A law is longer than the length cap.
- **REQ-281** A `Scope` value is not in the scope list.
- **REQ-282** An archived row in a chain does not point to the end of its chain.
- **REQ-283** A tracked text file outside the archive and the ledger cites a retired law.
  The error names the file, the line, and the law in effect. For a removed law it says that none is.
- **REQ-284** A tracked text file outside the archive and the ledger cites a retired ADR. The script reads the retired numbers from the ledger.
- **REQ-285** A tally in the ledger is not in the one tally format. A confirmation row, which holds `none`, is exempt.
- **REQ-286** The registry, the archive, the ledger, the install time, or the install commit does not match the recorded checksum.
- **REQ-287** An index is missing a document or lists one that does not exist.
- **REQ-288** A link is broken.
- **REQ-289** An ADR changelog is missing, is not the last section, or has a line without a date and a marker.
- **REQ-290** A `covers` list has more than five entries, or an entry that matches nothing.
- **REQ-291** An ADR, a design doc other than the glossary, or a law detail file passes the size cap.
  The registry, the archive, the ledger, and the two indexes are never checked against it.
- **REQ-292** A diagram is not one of the four allowed types, has no lead-in sentence, or passes the node cap.
- **REQ-293** An image file is missing, is not referenced, has no alt text, passes the size cap, or is not in an allowed format.
- **REQ-294** `lint` flags a time word outside a changelog for the prose editor. It does not fail on one.
  It does not scan the registry, the archive, or the ledger for time words.
- **REQ-295** The glossary has more than one term in a row, is out of alphabetical order, or repeats a term.
- **REQ-296** `lint` flags a very long sentence for the prose editor. It does not fail on one.
- **REQ-297** `lint` does not measure paragraphs.

### Judgment that stays with agents

- **REQ-298** These are never script work:
  - whether something is a law, an ADR, or neither
  - the wording of every law and every document
  - the votes and the chair's decision
  - whether a design doc is still true
  - whether the work contradicts a law or an ADR

## 16. Building Avalon in this repo

### Templates and fixtures

- **REQ-299** The plugin ships a template for the registry, the archive, the law detail file, the ADR, the design doc, the `CLAUDE.md` block, the core laws, and the writing standard.
- **REQ-300** This repo holds fixture repos for testing: a small code repo, a library, and a story bible.
- **REQ-301** One fixture holds decoy project agents named `chair` and `tech-writer`, and a decoy `docs/adr/` folder.
- **REQ-302** The fixture repos are for testing `init` and `check`. `claude plugin eval` can run scored cases against them.

### This repo's standards

The standards below are rough placeholders.
None of them is a requirement of this spec, a law, or an ADR.
The user and the agent refine each one together, and its wording, its kind, and its check are all open until they do.

| Placeholder | Rough intent | To refine |
|---|---|---|
| Test-driven | Tests come before the code they cover. | How strictly it applies, and to which code. |
| Arrange, Act, Assert | Each test has those three parts, in that order. | Whether it is a law, and how it is checked. |
| Tests separated by kind | Unit tests and integration tests live apart and run apart. | Which kinds exist, and where the line between them falls. |
| Separation of concerns | Parsing, decisions, and file writes are separate units. | How far the split goes, and whether it can be checked. |
| Coverage | Tests cover about 80% of the code written in this repo. | The exact threshold, what counts as code, and how coverage is measured. |
| Efficiency | CPU time and memory are weighed, and never outrank quality. | Whether this is a checkable rule or only a design guideline. |
| Linted | Code and markdown pass a linter. | Which tools, which rules, and what blocks a merge. |

The refinement also settles these points:

- Which tool fills each role. The brief suggests `pytest`, `coverage`, `ruff`, `mypy`, and `markdownlint`.
- How skills and agent files are tested, given that they are prompts and not code.
- Which checks run on every pull request.
- Whether this repo runs Avalon's own `lint` on its own docs.

- **REQ-303** Before any code is written, the user and the agent refine the placeholders into standards.
  Each refined standard has its exact wording, says whether it is a law, an ADR, or a guideline, and says how it is checked.
- **REQ-304** A placeholder binds nothing until it is refined. The refined standards apply as working standards from the first line of code.
- **REQ-305** Once the round table exists, each refined standard that is a law or an ADR goes to it and is registered.
  A guideline is written into a design doc of this repo.
- **REQ-306** Dev-only tools may be dependencies. The shipped script has none.
- **REQ-307** This repo runs Avalon on itself: its own round tables ratify the core laws before they ship.

### Build order

- **REQ-308** The build follows this order.
  1. This repo's standards, refined from the placeholders by the user and the agent.
  2. Formats and templates: every file format in this spec, the core law text, and the writing standard.
  3. The script: `scaffold`, the `law` commands, `packet`, `vote`, `tally`, `index`, and `lint` with its checksum.
  4. The `law` skill, the chair, the six seats, the `prose-editor`, and the hook.
     Avalon is then set up in this repo. The core laws are ratified, with those of this repo's standards that are laws.
  5. `init`, the `tech-writer`, and the `adr` commands, tested on the fixture repos.
  6. `adr`, `design`, and `intake`. Those of this repo's standards that are ADRs are then ratified.
  7. `check`, `sync`, the `law-reviewer`, and the `status`, `stale`, `verify`, and `for` commands.
  8. Hardening: a CI check, `move-root`, and an upgrade path for plugin versions.

## 17. Acceptance scenarios

Each scenario is a demonstration that the system meets this spec. The script scenarios run as automated tests against a fixture repo.

### The script

| ID | Scenario | Expected |
|---|---|---|
| AC-01 | `scaffold` runs in a repo with no docs. | The tree, the config file, the nine core laws, and the `CLAUDE.md` block exist. `lint` passes. |
| AC-02 | `scaffold` runs a second time. | The install time and the install commit are unchanged. Content outside the block markers in `CLAUDE.md` is unchanged. |
| AC-03 | `law add` runs with five recorded votes. | The law is the last registry row, with the next ID in the sequence. The ledger has one more row. `lint` passes. |
| AC-04 | `law add` runs with four recorded votes and no user override. | The command refuses, and no file changes. |
| AC-05 | LAW-000013 is amended to LAW-000019, which is amended to LAW-000031. | Both archived rows name LAW-000031 as the law in effect. `Replaced by` on the first row still names LAW-000019. |
| AC-06 | LAW-000031 is then removed. | All three rows are archived, each shows `none` as the law in effect, and the registry holds none of the three. |
| AC-07 | A law that has a detail file is amended. | The detail file of the retired ID no longer exists. |
| AC-08 | A tracked file cites a retired law, and `lint` runs. | `lint` fails and names the file, the line, and the law in effect. The same ID in the archive and the ledger raises nothing. |
| AC-09 | `law amend` runs on a law that three files cite. | The command prints all three citations. |
| AC-10 | A law is registered by user override. | The ledger row shows `user override`, the registry row has origin `user`, and `Dissent` names each seat that voted against. |
| AC-11 | A ledger row holds the tally `4-1`. | `lint` fails on that row. |
| AC-12 | The registry is edited without the script, and `lint` runs. | `lint` fails on the checksum. |
| AC-13 | The install time in the config file is changed, and `lint` runs. | `lint` fails on the checksum. |
| AC-14 | A legacy ADR is recorded with a `covers` entry that matches no path at the install commit. | The command refuses. |
| AC-43 | A legacy ADR is recorded whose `covers` paths all existed at the install commit, with no `evidence` file or no confirmation from the user. | The command refuses. |
| AC-44 | A legacy ADR names an `evidence` file that did not exist at the install commit. | The command refuses. |
| AC-15 | A path under a design doc's `covers` changes in a commit after the one in which the doc's stamp landed. | `stale` lists the doc. After `verify`, `stale` does not list it. |
| AC-33 | A design doc, its stamp, and a change to a covered path land in one commit. | `stale` does not list the doc. |
| AC-34 | A covered path has an uncommitted change, and the doc's stamp is committed. | `stale` lists the doc. |
| AC-35 | `stale` runs on a shallow clone. | The command refuses and says why. |
| AC-16 | A document is added, and `index` runs. | The index lists it with its `summary`. Before `index` runs, `lint` fails on the missing entry. |
| AC-17 | A document has six `covers` entries, or one that matches nothing. | `lint` fails. |
| AC-18 | `for` runs on a path that one ADR and one design doc cover. | It lists both and nothing else. |
| AC-19 | `move-root` moves the root to `docs/avalon/`. | The tree, the config file, the `CLAUDE.md` block, and every link use the new root. `lint` passes. |
| AC-20 | Any script command runs. | The git index, `HEAD`, and every ref are the same before and after. |
| AC-36 | `adr retire` runs with no recorded votes and no user override. | The command refuses, and no file changes. |
| AC-37 | `adr retire` runs with five recorded votes on an ADR that two files cite. | The ADR file no longer exists, the ledger has one more row, and the command prints both citations. |
| AC-38 | A tracked file cites a retired ADR as `ADR-0003`, and `lint` runs. | `lint` fails and names the file and the line. The same number in the archive and the ledger raises nothing. |
| AC-39 | The install record of ADR `0002` is written, and a second one is attempted. | The first is accepted with origin `user` and no ledger row. The second is refused. |
| AC-40 | `law confirm` runs on a law of origin `agent`. | The registry row has origin `user` and the same text. The ledger has one more row, decided by `user`, with `none` for rounds, tally, and dissent. `lint` passes. |
| AC-41 | `adr confirm` runs on an ADR of origin `agent`. | The ADR has origin `user` and a `(user)` changelog line. The ledger has one more row, decided by `user`. |
| AC-42 | A design doc holds the word "previously" outside a changelog, and `lint` runs. | `lint` flags the line and does not fail. |
| AC-45 | The ledger and the archive are each longer than the document size cap, and `lint` runs. | `lint` passes. |

### The plugin

| ID | Scenario | Expected |
|---|---|---|
| AC-21 | A session or a subagent calls Edit or Write on the registry, the archive, or the ledger. | The hook denies the call. |
| AC-22 | A session without the plugin opens a target repo. | The registry is in its context through the `@` import. |
| AC-23 | A subagent starts in a target repo. | The registry is in its context. |
| AC-24 | Avalon runs in the decoy fixture. | Each agent is spawned as `avalon:<agent>` and runs Avalon's prompt, not the decoy's. `init` proposes another root and writes nothing into the decoy `docs/adr/`. |
| AC-25 | A law proposal reaches a table. | Five seats vote, and the Enforcer is among them. No seat sees another's vote in round 1. |
| AC-26 | A decision reaches a table. | Five seats vote, and the Scout takes the Enforcer's place. |
| AC-27 | Round 1 is not unanimous. | Round 2 goes to the same five seat agents by message. No table runs a fourth round. |
| AC-28 | An agent convenes a table to amend a law of origin `user`. | Nothing is registered. The chair returns the recommendation for the user to confirm. |
| AC-29 | A table would reword the user's proposal. | Nothing is registered until the user accepts, counters, or overrides. |
| AC-30 | A table finishes. | The chair returns the outcome and the list of changed files, and has made no commit. |
| AC-31 | `init` runs on the story bible fixture. | The overview has no section that does not apply. The core ADRs mark unknown reasons as unknown. |
| AC-32 | `claude plugin validate .` runs in this repo. | It passes. |

## 18. Not settled by the brief

The build needs each item below, and the brief does not decide it.
The last column is a suggestion from the author of this spec, not a decision. Each is for the user to set.

### Values

| Item | Suggestion |
|---|---|
| Length cap for a law | 200 characters. |
| Soft cap on the registry | 100 laws in effect, about 3,500 tokens per session. |
| Size cap for a document | 400 lines. |
| Node cap for a diagram | Exactly 15. The brief says "about fifteen", and a lint needs one number. |
| Size cap and formats for an image | 500 KB. PNG, JPEG, SVG, and WebP. |
| Length at which a sentence is flagged | 40 words. |
| The list of time words | "previously", "formerly", "new", "now", "currently", "recently", and "no longer", refined against the fixtures. |
| The default scope list | `all`, `laws`, `adr`, `design`, and `docs`, which the core laws use. Each repo adds its own. |
| The list of repo profiles | `application`, `service`, `library`, `story-bible`, and `other`. |

### Mechanisms

| Item | What is missing | Suggestion |
|---|---|---|
| Config and frontmatter parsing | The script uses the standard library only, and that library has no YAML parser. | Limit both to flat keys, scalar values, and inline lists, and parse that subset in the script. Every example in the brief already fits. |
| Where packets and recorded votes live | The brief names the commands and not the location. | A `.avalon/` folder at the top of the repo that git ignores. |
| Where the checksum lives | It must be tracked, so that a clone and a CI job can verify it. | A field in `.avalon.yml`. |
| How a user's confirmation or override reaches the script | No command or flag is named. Nothing mechanical stops an agent from claiming one. | A flag on the law and ADR commands. The skill requires the user's answer in the session before it passes the flag. |
| Where a recommendation waits for the user | A table's recommendation on a `user` or `core` law must survive until the user answers. | The chair returns it to the session, and the recorded votes stay in `.avalon/` until a law command uses them. |
| Recording an ADR decision in the ledger | The ADR commands do not say that they append a ledger row. No command logs a rejected decision. | `adr new` and `adr log` append the row for a table decision, and an `adr reject` command is added. |
| Who may change the scope list | It is a fixed list in the config file, and no process changes it. | The user edits it. An agent asks first. |
| Script output and exit codes | Not specified. | Exit 0 on success, 1 on lint findings, and 2 on a refusal or a usage error. |
| The `AGENTS.md` block | The brief says the block can go there and not whether `init` writes it. | `init` offers it and writes it only when the user accepts. |
| The CI check and the upgrade path | Build step 8 names both and defines neither. | Define them when step 8 starts. |
| The writing standard as a detail file | It ships as the detail file of LAW-000009. A detail file has a fixed four-part body, changes only by amendment, and is deleted when its law is amended. None of the three suits the standard. | Exempt it from the four-part body, accept that a change to the standard is an amendment, and carry the file to the new ID. |
| `0001-architecture.md` in an empty repo | A repo with no work at the install commit has no legacy structure, so `0001` cannot pass the legacy test. | `init` skips `0001`, and the first architecture decision goes to a table. |
| A repo with no commits | `scaffold` records the commit it ran on, and a repo with no commits has none. | `scaffold` refuses until the repo has a first commit. |
