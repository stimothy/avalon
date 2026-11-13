# Avalon: design brief

This brief proposes Avalon, the docs system this repo will hold.
It is a design to react to, not a finished product.
Section 14 lists where it departs from the original description, and section 15 lists what is settled and what is still open.

## 1. Purpose

The system gives any repo three kinds of governed document: laws, ADRs, and design docs.
AI agents use them to orient themselves and to work correctly in the repo.
Humans can read every one of them without help.

The system must work for any repo: an application, a service, a library, a story bible, or this repo itself.
For that reason the brief says "the work" where a code-only system would say "the code".
The work is whatever the repo exists to hold: source, manuscript, configuration, or prompts.

## 2. The model

| | Laws | ADRs | Design docs |
|---|---|---|---|
| Answers | What must always hold? | What did we choose, and why? | What is this, and how does it work? |
| Voice | Prescriptive | Decisional | Descriptive |
| Changed by | Round table only | Round table for a decision, then an edit in place with a changelog entry | Edit in place |
| History kept in | The law archive and the ledger | The changelog at the bottom of the ADR, and the ledger | Git only |
| How agents read it | Always, in full | The index, then the ADR for the area being changed | The overview first, then by index |

### Precedence

**Laws > ADRs > the work > design docs.**

- Nothing may contradict a law.
- An ADR may not contradict a law.
- The work may not contradict a law or an ADR.
- A design doc may not contradict the work, an ADR, or a law.

When two levels disagree, the lower one is wrong.
Either the lower one is fixed, or the higher one is changed through its own process.
Design docs rank last because they describe the other three: a design doc that disagrees with the work is stale.

Other agent instructions in the repo, such as `CLAUDE.md`, rank below laws.

### Law or ADR

The two are easy to confuse, so the system defines both by a test.

An **ADR** records a choice. It is warranted when both of these hold:

- The choice is costly to reverse.
- There were real alternatives, and a future reader would ask why this one won.

A **law** is a standing rule. It is warranted when all of these hold:

- It is stated as "must" or "never".
- A reviewer can look at any piece of work and say whether it complies.
- It applies to a class of work across the repo, not to one place.
- It is expected to hold indefinitely.
- It is worth its cost: every agent reads every law in every session.

| Repo | ADR | Law |
|---|---|---|
| Web app | End-to-end tests use Playwright and run on every pull request. | Every test is structured as Arrange, Act, Assert. |
| Story bible | The story is told in first person, past tense. | No chapter reveals the narrator's name. |

A law may come from an ADR, and then it names that ADR as its source.
A law may also stand alone.

## 3. Principles

These apply to all three kinds of document.

1. **The docs hold only what is true now.**
   Replaced content is removed, not kept beside its replacement.
   History lives in ADR changelogs, the law archive, the ledger, and git.
2. **Every line is true on its own.**
   Agents find things with grep and often read one matching line.
   A line that states something no longer true, or never chosen, carries its marker on the same line.
   This extends the reason for living ADRs to every document.
3. **Each fact has one home.**
   Other documents link to it and do not restate it.
4. **Unknown is written as unknown.**
   An agent can recover what a repo does, but often not why.
   The docs never invent a rationale, a history, or an intent.
5. **Always-loaded content is kept small.**
   Only the law registry and a short orientation block load in every session.
   Everything else is reached through an index, on demand.
6. **The docs are plain markdown and explain themselves.**
   An agent without the plugin can still read and obey them.
   The plugin is needed only to author and audit.
7. **Scripts do the mechanical work, and agents do the judgment.**
   Anything repeatable that needs no reasoning is a script command: allocating an ID, moving a row, building an index.
   A skill tells the agent which command to run.
   This saves tokens and removes a class of mistakes.

## 4. Laws

### The registry

`docs/laws/LAWS.md` is one table of every law in effect.
Every agent reads the whole table before it does any work.
The file holds nothing that is not in effect, so the table needs no status column.

```markdown
# Laws

Every law in this table is in effect and binding. Read the whole table before doing any work.
Open a detail file only when the one-line law is not enough to act on.

| ID | Scope | Origin | Law | Detail |
|---|---|---|---|---|
| LAW-000001 | all | core | Nothing in this repo may contradict a law in this table. | |
| LAW-000010 | tests | user | Every test is structured as Arrange, Act, Assert. | [more](LAW-000010.md) |
| LAW-000011 | api | agent | Every public endpoint carries its version in its path. | |
```

- The law is one sentence, with a length cap that the lint enforces.
- There is one registry file, and it is never split.
- Rows are in ID order. The table reads the same way every time, and a new law is always the last row.
- Scope is a one-word tag from a fixed list in the config file.
  It helps a reader scan for the laws that touch the task at hand.
  It never changes where a law lives or how the table is ordered.

### Origin

Origin records who stands behind a law. All three values bind equally.

| Origin | Meaning |
|---|---|
| `core` | Shipped with the system and seeded at install. |
| `user` | Proposed by the user, or confirmed by the user after an agent proposed it. This includes a law registered by user override. |
| `agent` | Proposed by an agent and adopted by the round table without the user. |

Origin is in the registry for two reasons:

- The user can scan for `agent` laws and review them at any time.
- It sets what a table convened by an agent may change. The round table section gives the rule.

The user turns an `agent` law into a `user` law by confirming it. The text does not change, so no round table is needed.
The full record of each decision is in the ledger: who proposed it, who decided it, the tally, and any dissent.

### Law IDs

Every law has one key of the form `LAW-000001`, drawn from a single sequence for the whole repo.

- **The ID is permanent and carries no meaning.** It is never reused and never changes.
- **The category lives in the Scope column, not in the key.**
  A law about testing database migrations belongs to two categories, and a law can move between categories as the repo changes.
  A key such as `T-1` or `DB-456` would then be wrong, or it would have to change along with every citation of it.
- **The key is unmistakable in a search.**
  `DB-456` has the shape of an issue-tracker key, and a search for `T-1` also matches `T-10` and `GPT-1`.
  `LAW-000012` matches only itself.
- **Six digits allow 999,999 laws over the life of a repo.**
  The count includes archived laws, because an amendment takes a new ID.
  Frequent amendment cannot exhaust it.

### Detail files

A law gets a detail file only when one sentence cannot carry it.
The file is named for the law: `docs/laws/LAW-000010.md`.
Agents are told to open it only when they cannot act on the one-line law alone.

A detail file is part of its law.
The chair drafts it before round 1, and the seats vote on the law and its detail file together.
After a law is adopted, its wording and its detail file change only by amendment.

Its frontmatter names the law, and the source ADR if there is one.
It does not name the law it replaced. The archive holds that, and a detail file never cites a retired law.

The body contains:

- **Meaning:** what the law requires, in plain terms.
- **Applies to:** where it applies, and any exceptions.
- **Examples:** one that complies and one that violates.
- **Enforcement:** how a violation is detected, such as a lint rule, a test, or review.

### The archive

`docs/laws/archive.md` holds every law that was amended or removed.
It is never loaded automatically.
Its first line says that nothing in the file is in effect.

```markdown
| ID | Status | Text | Date | Replaced by | Now in effect | Reason |
|---|---|---|---|---|---|---|
| LAW-000012 | Removed | Every module has a README. | 2027-01-14 | none | none | Design docs made it redundant. |
| LAW-000013 | Amended | Unit tests are structured as Arrange, Act, Assert. | 2026-12-01 | LAW-000019 | LAW-000031 | Widened to all tests. |
| LAW-000019 | Amended | All tests are structured as Arrange, Act, Assert. | 2027-03-10 | LAW-000031 | LAW-000031 | Exempted generated tests. |
```

- **Amendment** creates a new law with a new ID. The old row moves to the archive.
- **Removal** moves the row to the archive with the reason.
- Each row carries its status on the same line as its text, so a grep hit cannot be mistaken for a law in effect.

An archived law carries two pointers:

- **Replaced by** is the law that amended it. It is history and never changes.
- **Now in effect** is the law at the end of the chain. It is updated on every later amendment.

In the example, LAW-000013 was amended to LAW-000019, which was later amended to LAW-000031.
Both archived rows name LAW-000031 as the law now in effect, so one lookup finds it from any old ID.

The chair updates the column when it registers an amendment.
The lint walks each chain and fails if a row does not point to its end.

**Removing an amended law.** Removal ends the whole chain. It does not bring back the law that came before.

- If LAW-000031 is removed, LAW-000013 and LAW-000019 stay archived.
  Every row in the chain then shows `none` as the law now in effect.
- A law comes into effect only by a round table's decision, and no table decided to restore the earlier text.
- To go back to an earlier wording, the proposal is an amendment that restates that wording. It takes a new ID.
- When a removal targets a law that has earlier versions, the chair shows the chain and confirms which of the two is meant.

When a law is amended or removed, its detail file is deleted.
The archive row is the whole record, and git keeps the rest.
This answers the question of whether to keep old law files: no, because a stale detail file is exactly what grep would find.

### No citation of a retired law

Nothing in the repo may cite an amended or removed law by its ID. The lint enforces this.

- **The lint scans every tracked text file:** the work, ADRs, design docs, law detail files, `CLAUDE.md`, and code comments.
- **Two files are exempt:** the archive and the ledger. They are the record of retired laws, and neither is loaded automatically.
- **Nothing else is exempt,** including ADR changelogs. A changelog line that cites a law cites the law in effect.
- **The error names the file, the line, and the law now in effect.** For a removed law it says that none is.
- **An agent fixes each citation, not the script.**
  An amendment changes what the law requires, so each place that relied on the old law is rechecked against the new one.
  A citation of a removed law is deleted.
- **The law commands list the citations.** `law amend` and `law remove` print every citation of the retired ID.
  The change is not complete until the lint passes.

This is the benefit of giving an amended law a new ID: everything that relied on the old law is found and rechecked.

The same rule holds for a retired ADR. Nothing may cite its number except the archive and the ledger.
The lint matches the form `ADR-0003` and the ADR's file name, and it reads the retired numbers from the ledger.

### The ledger

`docs/laws/ledger.md` records every decision a round table makes, one row per decision.
That covers every decision on a law and every decision on an ADR.
It also records each confirmation by the user, where no table sits.
It is never loaded automatically.
The script appends to it, and nothing else writes it.

```markdown
| Date | Decision | Proposed by | Decided by | Rounds | Tally | Dissent |
|---|---|---|---|---|---|---|
| 2026-12-01 | Amended LAW-000013 to LAW-000019 | agent | table | 1 | 5 approve, 0 amend, 0 reject | none |
| 2027-01-20 | Added LAW-000024 | user | user override | 3 | 2 approve, 0 amend, 3 reject | Skeptic, Jurist, Steward: it overlaps LAW-000010. |
| 2027-02-02 | Rejected: functions are at most 20 lines | agent | table | 3 | 1 approve, 0 amend, 4 reject | Practitioner: wanted a softer cap. |
| 2027-03-02 | Reversed ADR-0003: Vitest replaces Jest | user | table | 1 | 4 approve, 0 amend, 1 reject | Steward: the migration cost is not justified. |
```

**The tally has one format everywhere.** It names each count: `4 approve, 0 amend, 1 reject`.

- The order is always approve, amend, reject.
- Every count is written, including a zero.
- The counts are the votes of the last round held, and they add up to five.
- A bare pair of numbers, such as `4-1`, is never used. It does not say which side is which.
- The script writes the tally from the recorded votes, so no agent types it by hand.
- The lint rejects any other form in the ledger, apart from `none` in a confirmation row.

Dissent names each seat that voted against the decision that was made, with its reason.

`Decided by` takes one of three values:

- `table`: the table's outcome stands.
- `user override`: the user directed the outcome over the table's objection.
- `user`: the user confirmed an `agent` law or an `agent` ADR, and no table sat.

A confirmation row has `none` for rounds, tally, and dissent, and it keeps the original proposer.
A legacy record and the install record of ADR `0002` get no ledger row.

- The ledger is the user's review tool. One read shows what agents decided on their own.
- A rejection is logged so the same proposal is not argued again without a new argument.
- The record lives in the docs and not in commit messages, because commit conventions differ from repo to repo.

### The law budget

The number of IDs is not what limits a repo with many laws.
The limit is that every agent reads every active law in every session.
One row costs roughly 30 to 40 tokens.
At that rate, 100 active laws cost about 3,500 tokens per session and 1,000 would cost about 35,000.

The registry stays one file, so the count of active laws is what must be managed.
The system sets a soft cap on the size of the registry.
When a proposal would exceed the cap, the round table must also name laws to merge or remove, or state why none can go.
The cap is a pressure, not a block: a law the table adopts is registered either way.

### The round table

A law is created, amended, or removed only through a round table.
The same process decides every new ADR, and every reversal or retirement of one, with one seat changed. Section 5 gives those rules.

**Who may propose.** The user or any agent.
An agent convenes a table by invoking the `law` skill, and it does not wait for the user.
The existing laws bind the agent until the table decides.

**Chair.** A dedicated chair agent runs the table and spawns the seats.
Whoever proposes a law never chairs it, so no one judges their own proposal.
The chair works in its own context and returns only the outcome.
This keeps up to fifteen votes out of the session that asked for the law.

**Seats.** Five subagents sit at every table, each with one perspective.
Four seats sit on both kinds of matter. The fifth depends on the matter.

| Seat | Sits on | Asks about a law | Asks about a decision |
|---|---|---|---|
| Practitioner | Both | Can an agent follow this in daily work? What does it cost? | What is it like to build on this choice every day? |
| Skeptic | Both | Is this needed? Is it a law at all, or an ADR, a design note, or a lint rule? | Is a decision needed now? It argues for the strongest alternative, including doing nothing. |
| Jurist | Both | Does it conflict with, duplicate, or leave a loophole in existing laws and ADRs? | Does it conflict with a law or with another ADR? |
| Steward | Both | What does this lock in? Who pays for it a year from now? | What does this lock in? Who pays for it a year from now? |
| Enforcer | Laws | Can a violation be detected? Would two readers reach the same verdict? | Does not sit. |
| Scout | Decisions | Does not sit. | Were the real alternatives considered? What would it take to undo this choice? |

The Steward takes the lens of the repo's domain: an architect for a service, a continuity editor for a story bible.

The Enforcer gives way to the Scout because the two matters fail in different ways.
A law fails when it cannot be checked. A decision fails when a better option was never looked at.

**Process.**

1. **Screening.** The chair applies the law test and checks for duplicates and conflicts.
   It frames the proposal as new, as an amendment of a named law, or as a removal of a named law.
   The prose editor reviews the wording, and any draft detail file, before each round, so the seats never vote on an unclear sentence.
2. **Round 1.** The seats vote in parallel, without seeing each other.
   A vote is approve, amend with proposed wording, or reject. Each vote carries a short reason.
   The chair records the votes through the script, which tallies the round.
3. **Rounds 2 and 3.** If the vote is not unanimous, the chair revises the text and circulates every vote and reason.
   The chair sends this to the same five seat agents by message. It does not start new ones.
   The seats vote again. There are at most three rounds.
4. **Decision.** On a unanimous vote, or after round 3, the chair decides: adopt, adopt with final edits, or reject.
   The chair weighs the arguments and does not simply count votes.
5. **Registration.** The chair runs the script's law command.
   The command writes the registry row, any archive rows, and the ledger row.
   The chair writes the detail file that the seats approved, if the law has one.
6. **Hand-back.** The chair returns the outcome and the list of files that changed.
   The chair does not commit. It works in its own context and does not know the state of the branch.
   The session that asked for the table commits the files, following the conventions of the repo and its own instructions.
   Where the conventions allow, a law change is a commit of its own.

**The user's authority.** The user has the final say on every law.

- The table still sits on a proposal from the user, because it sharpens the wording and surfaces objections.
- If the table would reject or reword the user's proposal, the chair registers nothing.
  It returns its objection, with a counter-proposal if it has one, and asks the user to confirm.
- The user then chooses one of three things: accept the outcome, make a counter-proposal that goes back to the table, or direct that the law be registered as proposed.
- A law registered over the table's objection is marked as a user override in the ledger.

**Agent proposals.** Agents govern themselves, and the user steps in only when the user wants to.

- The chair's decision on an agent's proposal is registered at once, with origin `agent`.
- The agent names every law change and every decision it caused in its final report.
- An agent cannot override the table. Only the user can.
- A rejected proposal is logged in the ledger. The chair turns away a repeat that brings no new argument.
- A table convened by an agent may create a law, and may amend or remove a law of origin `agent`.
- For a law of origin `user` or `core`, the chair registers nothing.
  It returns the table's recommendation and waits for the user to confirm.
- The user reverses any agent law by proposing an amendment or a removal, with the final say.

**Seats keep their context between rounds.**

- A resumed seat still holds what it read and how it voted. It can judge whether the revision answers its own objection.
- It does not read the registry and the ADRs again, which saves tokens.
- A new seat in each round could raise new objections every time, and the table would not converge.
- The risk is that a seat defends its first vote out of habit.
  The chair's message therefore asks each seat whether the revision resolves its objection.
  The message says that changing a vote is expected when it does.
- The first round stays blind. A seat sees the other votes only from round 2.
- If a seat cannot be resumed, the chair starts a new one. The packet gives the new seat that seat's earlier votes and reasons.

**Cost.** One proposal uses five seat agents, each for up to three rounds.
Related proposals are heard together as a slate in one sitting, with a separate vote on each.

**A known limit.** The seats run on related models, so their opinions are correlated.
The fixed perspectives, a blind first round, a standing Skeptic, and a mix of models reduce this but do not remove it.

## 5. ADRs

An ADR is a living document about one decision topic.
It is edited in place, so it always states the decision in effect.
No ADR is ever marked superseded, because no superseded ADR exists to be found.

- The file name is a number and a topic: `docs/adr/0003-test-framework.md`.
- Numbers are sequential and are never reused.
- Every ADR in the directory is in effect. Proposals live in branches, not in the docs.

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

- `summary` states the decision in effect. The index is built from it.
- `covers` lists the paths the decision governs. The script uses it to answer "which ADRs apply to this file?".
- `origin` names who stands behind the decision in effect: `user` or `agent`.
  A legacy decision has origin `user`.
- Each changelog line names who decided the change.

| Changelog marker | Meaning |
|---|---|
| `(legacy)` | The decision predates the system. It was recorded with no table. |
| `(user)` | The user added detail, confirmed an agent's decision, or adopted the system at install. No table was needed. |
| `(agent)` | An agent added detail. No table was needed. |
| `(user, table)` | The user proposed or confirmed a decision, and the table agreed. |
| `(agent, table)` | An agent proposed a decision, and the table adopted it. |
| `(user override)` | The user directed a decision over the table's objection. |

**When a decision changes,** the body is rewritten to state the new decision.
The old choice moves into "Alternatives rejected", with the reason it was left.
The changelog gets one dated line that summarizes the change.

**When a decision stops applying,** the ADR is retired and the file is deleted.
Retiring an ADR follows the rules for a reversal, so a table sits first.
The ledger row of that decision is the record of the retirement. It names the number, the title, and the reason.
The index keeps no list of retired ADRs, so it stays fully generated and history stays in its homes.

**Who may change an ADR.**

The rule turns on whether a decision is being made or only recorded.

- **A decision that is being made goes to the round table before it is carried out.**
  That covers a new decision, the reversal of a decision in effect, and the retirement of one, whoever proposes it.
  A decision that is costly to reverse is worth five views before it is built.
- **A legacy decision is only recorded.**
  It gets origin `user`, and no table sits. The table cannot unmake what was built before the system existed.
- **Anyone may add detail** to an ADR without changing the decision in effect. No table sits.
- **The ADR binds every agent** until a reversal is decided.

Before a table sits on a new decision, the ADR skill applies the merit test.
A new decision that fails the test gets no table and no ADR.
A reversal or a retirement of an ADR in effect always gets a table.
The skill also prefers revising an existing ADR to creating one.

**Legacy has one meaning: in the repo before the system was installed.**

- `scaffold` writes the install time, and the commit it ran on, into the config file. It writes them once.
- The checksum covers both values, so the lint fails if either is changed.
- A decision is legacy only when the decision itself was already in effect in the repo at that commit.
  A covered area that existed at install does not make a decision about it legacy.
  Replacing the test framework inside an old `tests/` folder is a decision made after install, and it goes to the table.
- Three things must all hold before a decision is recorded as legacy:
  - Every `covers` entry of the ADR matches a path that existed then. The script checks this. It shows only that the area existed.
  - The ADR's frontmatter holds `evidence`: at least one file that shows the decision in effect at that commit.
    The script checks that each file existed then.
  - The user confirms that the decision predates the install.
- When the evidence or the confirmation is missing, the decision is not legacy. It goes to the table as a late decision.
- A decision that landed after the install time is never legacy, even if it landed without an ADR.
  That is a breach of the law on decisions. It goes to the table late, and the ledger row says so.
- A legacy decision can be recorded at any time, during `init` or years later, because the test is the same.
- Its changelog line carries the marker `(legacy)`.
- Its reasons are often lost. They are written as unknown, not guessed.

**Decisions follow the same authority rules as laws.**

- The user has the final say. The table still sits on a decision the user proposes, to give its view.
- If the table would reject or reword the user's decision, the chair changes nothing.
  It returns its objection, with a counter-proposal if it has one, and asks the user to confirm.
- The user then accepts the outcome, makes a counter-proposal, or directs that the decision stand as proposed.
- A table convened by an agent may adopt a new decision, which takes origin `agent`.
  It may also reverse an ADR of origin `agent`.
- For an ADR of origin `user`, the chair changes nothing. It returns the table's recommendation and waits for the user to confirm.
- The user turns an `agent` ADR into a `user` ADR by confirming it.
  The decision does not change, so no table sits, and the changelog gets a `(user)` line.
- A rejected decision is logged in the ledger and leaves no line in any ADR.
- The script refuses to record, reverse, or retire a decision without a complete round of recorded votes, a user override, or a pass on the legacy test.
  The install record of ADR `0002` is the one exception, and the script accepts it once.

After a decision is adopted, the skill asks whether it implies a law.
If it does, that law goes to the table as a proposal of its own.

## 6. Design docs

Design docs describe the repo as it is: what it is, what it does, and how its parts fit together.
They are living documents with no changelog.
They describe the present only. Planned work lives in specs or briefs, outside this system.

Each design doc opens with frontmatter:

```markdown
---
summary: How users sign in and how sessions are kept. Read it before changing login or tokens.
covers: [src/auth/**]
verified: 2026-11-10
verified_commit: 3f9c2ab
---
# Authentication
```

- `summary` says what the doc covers and when to read it. The index is built from it.
- `covers` lists the paths in the work that the doc describes.
- `verified` is the date the doc was last checked against those paths.
- `verified_commit` is the commit that was checked out when the doc was verified.

The `covers` field and the stamp make staleness detectable without an agent.
The stamp is the `verified` and `verified_commit` pair.
A doc is stale when a covered path changed after its stamp landed.
That covers every commit that is reachable from `HEAD` and not from the commit in which the stamp landed, and every uncommitted change to a covered path.
A doc whose stamp is not yet committed is not stale.
On a shallow clone, `stale` and the legacy test refuse to run and say why.
`verified_commit` records what was checked and makes each stamp distinct. The staleness rule does not compute from it.
The script lists every stale doc. An agent then reviews only those docs, updates them if needed, and resets the stamp.

Staleness is counted in commits and not in dates, so a change made later on the same day is not missed.
A doc that is updated and stamped in the same commit as the work is not stale, which is what the law on design docs asks for.

### The glossary

`docs/design/glossary.md` defines the terms a reader needs to follow the repo.
It is a design doc: it is living, it has no changelog, and it may not contradict a law, an ADR, or the work.

```markdown
| Term | Meaning |
|---|---|
| Ledger | The record of every round-table decision and every confirmation by the user. See `docs/laws/ledger.md`. |
| Tenant | One customer organisation and all of its data. Also called an account in older code. |
| The work | Whatever this repo exists to hold. Here it is the service's source code. |
```

- **One term per row, in alphabetical order.**
  The term and its meaning are on one line, so one search finds both.
- **It is the one home for a definition.**
  Other documents link to the glossary and do not define the term again.
- **It holds terms that are specific to the repo, or used in a special sense.**
  It does not define general vocabulary.
- **A meaning is one or two sentences.** A longer explanation belongs in a design doc, and the row links to it.
- **A known synonym is named in the row,** so a search for either word finds the entry.
- **It is not loaded automatically.** An agent looks a term up when it meets one it does not know.
- **It is read by lookup, not from top to bottom,** so the document size cap does not apply to it.
- **It never holds a rule.** A definition that tells an agent what it must do is a law, and goes to the round table.

`init` seeds the glossary with the system's own terms and with the terms it finds in the repo.

## 7. Frontmatter and indexes

Frontmatter holds the facts about a document that a script needs: its summary, the paths it covers, and its dates.
The script reads and writes these fields, so an agent spends no tokens on them.
Frontmatter holds nothing that the body also states.

`docs/adr/README.md` and `docs/design/README.md` are the indexes.
Each lists every document with one line: the decision in effect for an ADR, or "read this when" for a design doc.

The script generates the indexes from each document's `summary` field. They are never written by hand.
This keeps them complete and stops them from drifting.

### Keeping `covers` small

A growing repo must not turn `covers` into a long list of paths.

- **An entry is a glob at folder level,** such as `src/auth/**`.
  A single file is listed only when it stands alone, such as a config file.
- **A document has at most five entries.** The lint enforces the cap.
- **A document that needs more covers more than one subject.**
  The writing standard already says to split it.
- **A broad document uses a shallow glob.**
  The overview matches only the top level of the repo.
  It goes stale when a top-level folder is added, removed, or renamed, and not on every change.
- **The lint fails on an entry that matches nothing.**
  A moved or deleted folder is therefore noticed at once.
- **Coarse entries are fine.**
  A false alarm costs one review of the document. A miss leaves a stale document.

`covers` is a routing hint and a staleness trigger. It is not a complete map of the repo.
A folder that no document covers is not an error.

## 8. Writing standard

The standard applies to every document in the system.
It ships as the detail file of a core law, so the doc-writing skills load it and other sessions do not.

Two things enforce it.
The lint checks what can be measured: document size.
The size cap applies to ADRs, design docs, and law detail files only.
The registry, the archive, the ledger, and the two indexes are exempt, because each is a table that grows by design and cannot be split.
The registry has its own soft cap, the law budget.
It flags a very long sentence, and a time word outside a changelog, for the prose editor to judge. It does not fail on either.
It does not measure paragraphs at all.
The prose editor agent judges the rest: clarity, audience, flow, and paragraph structure.

- **One subject per document.** The title names it and the summary states it.
- **Extend before creating.** New material goes into the document that owns the subject.
  A new document is created only when no document owns it.
- **Split when a document outgrows its subject.** It covers more than one subject, or it passes the size cap.
  A split leaves no stub. Links and the index are updated.
- **One idea per sentence.** Parallel items become a list, and comparisons become a table.
- **A paragraph holds one point and breaks where a reader would expect.**
  It is as long as its point needs, and there is no cap on its length.
  Sentences that belong together stay together, and a new point starts a new paragraph.
- **An edit is woven in, not tacked on.**
  New material is never just appended to the nearest paragraph.
  The writer rewrites the paragraph, splits it, or adds one, so that the passage reads as if it were written in one sitting.
  This is what stops a paragraph from growing by one sentence with every change.
- **Present tense, current state.** A word that places something in time, such as "previously", "new", or "now", appears only in a changelog.
  The prose editor judges whether a word is used in that sense, because "a new document" is not a statement about time.
  The registry, the archive, and the ledger are exempt, because the script writes them.
- **Every line is true on its own.**
- **Unknown is written as unknown.**
- **A reader who has never seen the repo can follow it.** A term is defined once, in the glossary, and linked after that.

### Diagrams

ADRs and design docs may hold diagrams. A diagram helps a human take in a structure faster than prose does.

- **Diagrams are written in Mermaid,** in a fenced block inside the document.
  The source is text, so an agent can read it, search it, and edit it in the same change as the prose.
- **A sentence before the diagram says what it shows.**
  The sentence serves an agent, and it serves a reader whose viewer does not render Mermaid.
- **The diagram shows the shape, and the prose explains it.**
  The diagram is the home for what connects to what. The prose says why, and what each part does.
- **A diagram shows only the present.**
  It never draws a rejected alternative or an earlier design, because one line of it could be read as current.
- **A diagram stays small.** It has at most about fifteen nodes. A larger one is split, or the document is.
- **The syntax stays plain.** Allowed types are flowchart, sequence, state, and entity-relationship.
  Plain syntax renders on older Mermaid versions, such as the one a code host ships.

Mermaid has known limits, and the user has accepted them:

- The lint cannot check full Mermaid syntax in a target repo, so a broken diagram can go unnoticed until a person views it.
- Layout is automatic and cannot be adjusted by hand.
- A terminal or a plain viewer shows the source instead of the drawing.

### Images

Design docs may also hold images. ADRs may not.

- **An image is for what Mermaid cannot draw:** a screenshot, an interface mock-up, a map, a sketch, or artwork.
  Anything that can be a Mermaid diagram is one.
- **Images live in `docs/design/assets/`.** A file is named for its document and its subject, such as `overview-site-map.png`.
- **Every image has alt text that says what it shows.**
- **An image never carries a fact that the text lacks.**
  An agent cannot search an image, so an agent works from the text and does not need to open the image.
- **An image is checked with its document.**
  When a design doc is reviewed as stale, the reviewer opens its images too.
- **Images stay light.** The lint enforces a size cap and a short list of formats.

## 9. Layout and loading

### In a target repo

```text
docs/
  laws/
    LAWS.md        registry, always read in full
    archive.md     amended and removed laws; never loaded automatically
    ledger.md      every round-table decision and confirmation; never loaded automatically
    LAW-000010.md     detail file, only for laws that need one
  adr/
    README.md      generated index
    0001-architecture.md
    0002-documentation-system.md
  design/
    README.md      generated index
    overview.md
    glossary.md    terms and their meanings, one per row
    assets/        images used by design docs
.avalon.yml   at the top of the repo: root path, repo profile, system version, install time and commit, caps, scope list
```

### Choosing the root

Setup has two steps with two scopes.
The plugin is installed once, for the user.
The system is then set up in each repo by `init`.
The root is chosen in the second step, so it is a per-repo setting from the start.

The root is resolved in this order:

1. The repo's config file.
2. The plugin's `default_root` option, which the user sets once as the default for every new repo.
3. `docs/`, because that is where people and agents look first.

The config file sits at a fixed path at the top of the repo, so every script finds it without knowing the root.
The three folders sit beside any docs that are already in the root.
`init` warns when a site generator publishes the whole of `docs/`, and suggests another root.

**An environment variable is not used.**
The root is a fact about the repo, and every agent, teammate, and CI job must agree on it.
An environment variable differs by machine and by session, so two sessions could disagree about where the laws are.

**Changing the root later** is one script command.
It moves the tree and rewrites the config file, the `CLAUDE.md` block, and every link.

### How agents load it

Install writes a managed block into `CLAUDE.md`, between markers, so it can be rewritten safely.

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

The `@` import loads the registry into every session without a hook and without the plugin.
The same block, with a "read this file in full" instruction in place of the import, can go in `AGENTS.md` for other agents.

Subagents receive `CLAUDE.md` as the main session does, so the chair, the seats, and any working subagent see the laws.
The built-in Explore and Plan agents do not receive it. They only read and plan, and the session that acts on their output has the laws.
An `@` import expands for a subagent as well. A live test confirmed it: a subagent quoted a phrase from an imported file without reading any file.
The block still tells the reader to open the file when the table is missing.
That line covers an agent or tool that does not expand imports.

## 10. When things conflict

| Conflict | What the agent does |
|---|---|
| A design doc disagrees with the work | Updates the design doc. |
| The work disagrees with an ADR | Reports it. Either the work is fixed, or the decision really changed and the ADR is revised. |
| An ADR disagrees with a law | Reports it. Either the ADR is revised, or an amendment goes to a round table. |
| A task requires breaking a law | Stops that part of the task and names the ID. It may take an amendment to a round table. The law binds until the table decides. |
| A task requires breaking an ADR | Stops that part of the task and names the ID. It may take a reversal to a round table. The ADR binds until the table decides. |
| The work already violates a law when it is found | Reports it. Fixes it only if that is inside the task. |

An agent never resolves a conflict silently and never works around a law.

## 11. The core set

Every repo gets the same starting set.
Laws are copied verbatim by the script. ADRs and design docs are written during `init` by an agent that reads the repo.

### Core laws (draft)

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

Each core law is seeded with origin `core`. LAW-000009 links to its detail file, which holds the writing standard.

These are drafts.
This repo will run its own system, and its first round tables will ratify the core laws before they ship.

### Core ADRs

- **`0001-architecture.md`:** the load-bearing structure of the repo.
  It covers what form the repo takes, its major parts and their boundaries, and its primary technologies or formats.
  Reasons are given where they are known and marked unknown where they are not.
- **`0002-documentation-system.md`:** the decision to adopt this system, with the root path and any local settings.
  The plugin fills in most of it.
  It is the user's decision, made by running `init`. `init` records it with origin `user` and the marker `(user)`, and no table sits.
  The decision is made at install, and the law on decisions applies after install.

Install also lists the other decisions it found in the repo that pass the ADR test but have no record.
The user chooses which to write, because the reasons usually have to come from the user.

### Core design docs

- **`overview.md`:** required. It contains:
  - what the repo is, in one paragraph
  - its purpose and audience
  - what it does or contains
  - its main parts and how they relate
  - a map of the repo
  - how to work in it

  A section that does not apply is left out, not left empty.

- **`glossary.md`:** required. It starts with the system's own terms, such as law, ADR, round table, ledger, legacy, and the work.
  `init` adds the terms it finds in the repo. The overview links to it and does not keep a term list of its own.

Other design docs are created when the overview outgrows its subject.
Install suggests likely ones from the repo profile: interfaces and data for a service, characters and timeline for a story bible.

## 12. What gets built in this repo

The system ships as a Claude Code plugin, and this repo is its marketplace.
A target repo holds only its generated docs, the config file, and the `CLAUDE.md` block.

**Skills**

| Skill | Does |
|---|---|
| `init` | Surveys the repo, sets its profile, seeds the core set, writes the `CLAUDE.md` block. Safe to run again. |
| `intake` | Takes a design, spec, or conversation and sorts it: law candidates and decisions to a round table, description to design docs. |
| `law` | Frames a proposal to create, amend, or remove a law, hands it to the chair, and reports the outcome. Records the user's confirmation of an `agent` law. |
| `adr` | Applies the merit test, takes a decision to the chair, and records the outcome. Adds detail to an existing ADR without a table. Records the user's confirmation of an `agent` ADR. |
| `design` | Writes, updates, splits, and merges design docs. |
| `check` | Reports problems. Runs the lint, then an agent audit for contradictions between levels, then a prose review of every document. |
| `sync` | After work is done, reviews the changes and updates stale design docs. Flags unrecorded decisions and law violations. |

**Agents**

A skill is a procedure that runs in the main session.
An agent is a role with its own system prompt and a fresh context.
Skills call agents. The plugin ships ten agent files.

| Agent | Role | Called by | Writes files |
|---|---|---|---|
| `chair` | Runs the round table, decides, and registers the outcome | `law`, `adr`, `intake`, `init` | Yes, law files only |
| `seat-practitioner` | Round-table seat, for laws and decisions | The chair | No |
| `seat-skeptic` | Round-table seat, for laws and decisions | The chair | No |
| `seat-jurist` | Round-table seat, for laws and decisions | The chair | No |
| `seat-steward` | Round-table seat, for laws and decisions | The chair | No |
| `seat-enforcer` | Round-table seat, for laws only | The chair | No |
| `seat-scout` | Round-table seat, for decisions only | The chair | No |
| `law-reviewer` | Checks work against the laws and ADRs | `check`, `sync`, or the user directly | No |
| `tech-writer` | Writes and edits ADRs and design docs to the writing standard | `adr`, `design`, `init`, `sync` | Yes, docs only |
| `prose-editor` | Reviews the prose of laws, ADRs, and design docs as a human reader would | The chair, `adr`, `design`, `init`, `sync`, `check` | Yes, ADRs and design docs only, and nothing under `docs/laws/` |

**The chair.** Its file holds the round-table procedure, the voting rules, and the vote format.
It is impartial: it weighs the arguments and does not argue for the proposal.
It is the only agent that writes law files.
Its file lists the `Agent` tool, which it needs to spawn the seats, and the `SendMessage` tool, which it needs to resume them.

The chain is session, then chair, then seats, which is two layers of subagent.
Claude Code allows three layers below the main session by default.
A first-layer subagent can therefore invoke the `law` skill and still seat a full table, with the seats at the third layer.
A subagent at the second layer or deeper cannot, so it hands its proposal up to the agent that spawned it.
The setting `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` can lower the limit.
The round table needs it to be at least 2 when the session convenes the table, and at least 3 when a first-layer subagent does.

**The seats.** Each seat file holds only its perspective: what it cares about and what it asks.
A seat that sits on both kinds of matter holds its questions for each.
The chair seats five of the six files, by the kind of matter.
For an ADR, the chair decides and records the ledger row, and the `tech-writer` then writes the ADR.
The voting rules and the vote format live once, in the chair's file, and the chair passes them in.
A seat's file lists only read and search tools, so a seat cannot write a file or spawn an agent.
Separate files are preferred over one generic seat because an agent file becomes the system prompt.
That makes each perspective a separate persona, not a paragraph inside a shared prompt.

**The law reviewer.** It receives a diff or a path and reports each violation with the ID, the location, and its confidence.
It never fixes what it finds.
Its value is its fresh context: it has not seen the reasoning that produced the work, so it does not explain violations away.
Unlike a working agent, it opens the detail file of every law in scope.

**The tech writer.** It always loads the writing standard.
It owns the choices the standard describes: extend or create, when to split, and how to word a line so it is true on its own.
It writes the Mermaid diagrams.
It words the content it is given and does not make decisions or invent reasons.
It never writes law files, because only the chair registers a law.

**The prose editor.** It owns whether a person can read the docs.
It reads a document cold, as a reader who has never seen the repo, and it is given the document and not the conversation behind it.
A writer knows what it meant, so it cannot see what is unclear. A separate reader can.

- **What it checks:** audience, clarity, flow, sentence structure, paragraph structure, punctuation, grammar, defined terms, and whether each line is true on its own.
- **Paragraphs:** it checks that each one holds one point and that the latest edit was woven in.
  It restructures a paragraph that has grown by one addition after another.
- **Terms:** it flags a repo-specific term that the glossary does not define, and a term that a document defines for itself.
  The `tech-writer` adds or moves the entry.
- **ADRs and design docs:** it fixes the prose directly and lists what it changed.
- **Law files:** it never edits a file under `docs/laws/`, because the chair is the only agent that writes them.
  For the wording of a law, it returns suggested wording to the chair before the seats vote.
  For a law detail file, it returns its suggestions to the chair before the seats vote.
  After a law is adopted, its wording and its detail file change only by amendment, so the editor only reports on them.
- **Meaning:** it changes wording and never meaning.
  When a fix would change what a sentence says, or the meaning is unclear, it reports the passage instead of editing it.
- **One pass:** the writer writes, the editor edits, and the lint runs. There is no back and forth between the two agents.
- **Audit mode:** under `check` it reviews every document and only reports.

The lint does the measurable part first, so the editor spends its tokens on judgment.

**Models and effort**

Each agent file sets its own model and effort, so an agent behaves the same whatever model the session runs.
No file names Fable.

| Agent | Model | Effort | Why |
|---|---|---|---|
| `chair` | Opus | high | It makes a binding decision and writes the final text. It runs once per table. |
| `seat-jurist` | Opus | high | It must catch a conflict with any existing law or ADR. A miss becomes a contradiction in binding law. |
| `seat-skeptic` | Sonnet | high | Arguing the case against takes more reasoning than judging from one viewpoint. |
| `seat-scout` | Sonnet | high | Finding the option nobody raised takes more reasoning than judging the one on the table. |
| `seat-practitioner`, `seat-enforcer`, `seat-steward` | Sonnet | medium | Each makes a bounded judgment from one perspective. |
| `law-reviewer` | Sonnet | high | It runs often, and both a missed violation and a false alarm are costly. `check` can raise it to Opus for a full audit. |
| `tech-writer` | Sonnet | medium | It words content it is given, to a written standard. |
| `prose-editor` | Sonnet | medium | It judges prose against a written standard, one document at a time. |

- Haiku is not used. The mechanical work lives in the script, and every agent task here is a judgment.
- The mix of Opus and Sonnet at the table also makes the votes less correlated.
- These are starting values, to be tuned against the fixture repos.
- The `model` and `effort` fields of an agent file set these values, and the `tools` field limits what the agent can call.
- A plugin's agent files ignore the `hooks`, `mcpServers`, and `permissionMode` fields. This design uses none of them.

**Names**

The plugin is named `avalon`.
In the legend, Avalon is the isle of the Round Table's king, and the round table is the heart of this system.

- A skill is invoked as `/avalon:<skill>`, such as `/avalon:init` and `/avalon:law`.
- An agent is addressed as `avalon:<agent>`, such as `avalon:chair`.
- The config file is `.avalon.yml`, at the top of the repo.
- The `CLAUDE.md` block sits between `<!-- avalon:start -->` and `<!-- avalon:end -->`.

**Every name is scoped to Avalon,** so nothing collides with another plugin or with a repo's own files.

- Claude Code prefixes every plugin skill and agent with the plugin name. The docs confirm both forms.
- Agents are always spawned by their full name, such as `avalon:tech-writer`, and never by the bare name.
- The script is one file named `avalon`, called by its path inside the plugin. It is not put on the PATH.
- Plugin options are stored per plugin.
- `init` never writes into a folder that holds content it did not create. On a clash it proposes another root, such as `docs/avalon/`.
- A skill file sets no `name` field, so the skill has no bare command.
  `/avalon:init` therefore cannot clash with the built-in `/init`, with a project skill, or with another plugin's skill.
- When two agents share a bare name, a project or user agent outranks a plugin's agent.
  A repo's own `tech-writer` would win over Avalon's if Avalon spawned by bare name, which is why it never does.
- The docs show the full agent name working on the command line and in a mention.
  They do not state it for the Agent tool, so a fixture repo with decoy agents proves it.

The skill and agent names are settled as the suggested column:

| Kind | Suggested | Alternatives |
|---|---|---|
| Skills | `init`, `intake`, `law`, `adr`, `design`, `check`, `sync` | `distill` for `intake`, `audit` for `check`, `refresh` for `sync` |
| Agents | `chair`, `seat-practitioner`, `seat-skeptic`, `seat-jurist`, `seat-steward`, `seat-enforcer`, `seat-scout`, `law-reviewer`, `tech-writer`, `prose-editor` | `auditor` for `law-reviewer`, `scribe` for `tech-writer`, `editor` for `prose-editor` |

**The script**

One command-line script does every mechanical step.
Skills direct agents to it, and agents never do these steps by hand.
It runs on Python 3 with the standard library only, so it has no dependencies beyond its runtime.

| Command | Does |
|---|---|
| `scaffold` | Creates the tree, copies the templates and core laws, writes the config file, and writes or refreshes the `CLAUDE.md` block. |
| `status` | Prints a short summary: the law count against the budget, stale design docs, and the lint result. An agent reads this instead of the files. |
| `law add`, `law amend`, `law remove`, `law reject`, `law confirm` | Allocates the ID and writes the registry row. Moves retired rows to the archive and updates every "now in effect" pointer in the chain. Deletes retired detail files. Appends the ledger row. `law confirm` changes the origin of an `agent` law to `user`. |
| `packet` | Assembles what a seat needs to vote into one file: the proposal with any draft detail file, the registry, and the related ADRs. For a later round it adds the earlier votes and reasons. |
| `vote`, `tally` | Records the votes of a round. Prints the result in the one tally format. |
| `for` | Lists the ADRs and design docs that cover a path. An agent runs it before it changes a file. |
| `adr new`, `adr log`, `adr retire`, `adr confirm` | Allocates the number, creates the file from the template, and appends a dated changelog line. `adr retire` deletes the file, appends the ledger row, and prints every citation of the retired number. `adr confirm` changes the origin of an `agent` ADR to `user`. |
| `index` | Regenerates both indexes from the `summary` fields. |
| `stale`, `verify` | Lists the design docs that are stale under the stamp rule. Stamps a doc with the date and the current commit. |
| `lint` | Checks registry and archive format, unique IDs, law length, the scope list, chain pointers, index completeness, broken links, citations of retired laws and retired ADRs anywhere outside the archive and the ledger, ADR changelogs, `covers` entries, and size caps. For diagrams it checks the type, the lead-in sentence, and the node count. For images it checks that each file exists, is referenced, has alt text, and is within the size cap. For prose it flags time words outside changelogs, and very long sentences, for review without failing. It does not scan the registry, the archive, or the ledger for time words. For the glossary it checks one term per row, alphabetical order, and no duplicate terms. |
| `move-root` | Moves the tree and rewrites the config file, the `CLAUDE.md` block, and every link. |

These stay with agents, because they need judgment:

- whether something is a law, an ADR, or neither
- the wording of every law and every document
- the votes and the chair's decision
- whether a design doc is still true
- whether the work contradicts a law or an ADR

**The script never writes to git.**
It does not stage, commit, branch, tag, or push, and it takes no commit message as an argument.
It only reads git, for four things:

- history, for the staleness check
- the install commit, for the legacy test
- the current commit, when it records an install or stamps a design doc
- the list of tracked files, for the lint

A commit depends on things the script cannot know:

- the branch the work is on, and whether that branch may take a commit
- the repo's conventions for messages, and for what one commit may hold
- commit hooks and signing
- whether the user has kept git for themselves in that repo

The script changes files and prints the list of files it changed.
The session that owns the work decides when and how they are committed.

**How it is called.** Skills and agent files name the script by its path inside the plugin, through the `${CLAUDE_PLUGIN_ROOT}` reference.
The plugin has no `bin/` directory, because claude.ai and Cowork do not install a plugin that has one.

**Blocking direct writes.** The script is the only writer of the registry, the archive, and the ledger.
Four guards protect those files:

- A `PreToolUse` hook denies any Edit or Write call that targets them. The hook also runs inside subagents.
- The same hook inspects Bash commands that write to those files.
  This check is best-effort, because a shell command can be written in many ways.
- The script records a checksum of the three files each time it writes them.
  `lint` fails when a file no longer matches, so an edit that got past the hook is still caught.
- The law and ADR commands refuse to register a law, or to record, reverse, or retire a decision, without a complete round of five recorded votes or a user override.
  A legacy decision must pass the legacy test instead. The install record of ADR `0002` needs neither.

These guards turn "never edit law files by hand" from an instruction into a mechanism.
They stop shortcuts and accidents. They do not stop an agent that sets out to forge a record.
The hook is the blocking mechanism the plugin relies on. Whether a plugin can also ship permission rules is not checked.

**Other parts**

- **Templates:** the registry, archive, law detail file, ADR, design doc, `CLAUDE.md` block, core laws, and writing standard.
- **Fixture repos:** a small code repo, a library, and a story bible, for testing `init` and `check`.
  `claude plugin eval` can run scored cases against them.
  One fixture holds decoy project agents named `chair` and `tech-writer`, and a decoy `docs/adr/` folder, to prove that nothing collides.

**Installing it**

The plugin installs from this repo on GitHub. It needs no official marketplace listing.

- **Installed for every session:** `claude plugin marketplace add <owner>/<repo>`, then `claude plugin install <plugin>@<marketplace>`.
  This repo is both the marketplace and the plugin. Its marketplace file lists one plugin whose source is the repo root.
- **For one session:** `claude --plugin-dir <path to the plugin>`. This is the loop for developing the plugin from a local checkout.
- **Before a release:** `claude plugin validate .` checks the manifests.

**Build order**

1. This repo's standards: the user and the agent refine the placeholders in section 13 and adopt them as working standards.
2. Formats and templates: every file format in this brief, the core law text, and the writing standard.
3. The script: `scaffold`, the `law` commands, `packet`, `vote`, `tally`, `index`, and `lint` with its checksum.
4. The `law` skill, the chair agent, the six seat agents, the `prose-editor` agent, and the hook that blocks direct edits to the law files.
   Set the system up in this repo, then ratify the core laws and those of this repo's standards that are laws.
5. `init`, the `tech-writer` agent, and the `adr` commands. Test on the fixture repos.
6. `adr`, `design`, and `intake`. Ratify those of this repo's standards that are ADRs.
7. `check`, `sync`, the `law-reviewer` agent, and the `status`, `stale`, `verify`, and `for` commands.
8. Hardening: a CI check, `move-root`, and an upgrade path for new plugin versions.

## 13. Engineering standards for this repo

This section is a list of rough placeholders, not a set of decisions.
The user and the agent refine them together before any code is written.
The user named these standards in passing while the design was discussed.
None of them is a law or an ADR yet, and the wording below is not final.

| Standard | What it means here |
|---|---|
| Test-driven | A failing test is written before the code that makes it pass. |
| Arrange, Act, Assert | Every test has those three parts, in that order. |
| Tests separated by kind | Unit tests and integration tests live apart and run apart. A unit test exercises one unit, with no git and no network. An integration test runs the script against a fixture repo. |
| Separation of concerns | Parsing, decisions, and file writes are separate units. The logic is pure, and the input and output layer is thin. |
| 80% coverage | Tests cover at least 80% of the code written in this repo. Coverage is measured on every test run. |
| Efficiency | CPU time and memory are weighed in each design. They never outrank correctness or clarity. |
| Linted | A linter, a formatter, and a type checker run on all code. A markdown linter runs on the skills, agent files, and docs. A change that raises a warning does not merge. |

**How the placeholders become decisions**

1. Before any code is written, the user and the agent refine the placeholders into standards.
   Each refined standard has its exact wording, says whether it is a law, an ADR, or a guideline, and says how it is checked.
   The refinement also makes the choices that are still open, such as how coverage is measured and which tools are used.
2. A placeholder binds nothing until it is refined.
3. The refined standards apply as working standards from the first line of code.
4. Once the round table exists, each refined standard that is a law or an ADR goes to it and is registered.
   A guideline is written into a design doc of this repo.

**Points for the refinement to settle**

- Coverage is expected to apply to code: the script and the hooks.
- Skills and agent files are prompts, not code. They are expected to be tested against the fixture repos with `claude plugin eval`.
- Which dev-only tools this repo depends on. A test runner, a coverage tool, and the linters are expected.
- The tests, the coverage measure, and the linters are expected to run on every pull request.
- This repo is expected to run Avalon's own `lint` on its own docs.
- Which tool fills each role is an ADR.
  Suggested: `pytest` and `coverage` for tests, `ruff` to lint and format, `mypy` for types, and `markdownlint` for markdown.
- A standard that cannot be checked from the work, such as efficiency, may become a guideline in a design doc instead of a law.

## 14. Where this departs from the original description

| Original | Proposed | Why |
|---|---|---|
| One law file holds all laws, with status and amendment links | Active laws in `LAWS.md`; amended and removed laws in `archive.md` | The always-read file stays small, and no agent reads a dead law as live. |
| Decide whether to keep old law detail files | Delete them on amendment or removal | A stale detail file is what grep would find. The archive row and git keep the record. |
| Rejected proposals not mentioned | Logged in a ledger, with every other round-table decision | Stops the same proposal from being argued again, and gives the user one place to review what agents decided. |
| The parent agent chairs the round table | A dedicated chair agent | The proposer does not judge its own proposal, and the votes stay out of the working session. |
| An amended law points to the law that amended it | It also points to the law now in effect, at the end of the chain | One lookup from any old ID finds the current law. |
| Laws described by example | A five-part law test and a law budget | Keeps laws few, checkable, and worth their token cost. |
| ADRs edited in place | Also: one ADR per topic, old choices move to "Alternatives rejected", retired ADRs are deleted | Follows from living documents. |
| Grep concern raised for ADRs | "Every line is true on its own" for all docs | The same risk exists in every document. |
| "Code" in the precedence chain | "The work" | Covers story bibles and other repos that are not code. |
| Design docs must not contradict code | Also: `covers`, `verified`, and `verified_commit` headers | Makes staleness detectable by a script. |
| Indexes for ADRs and design docs | Generated, not hand-written | They cannot drift or miss a document. |
| Core ADR `0001-architecture.md` | Also `0002-documentation-system.md` | Adopting this system is itself a decision that is costly to reverse. |
| Not mentioned | Unknown is written as unknown | An agent filling in core docs will otherwise invent reasons. |
| Not mentioned | A conflict table | Agents need to know what to do when levels disagree. |

## 15. Open decisions

Three items are open.

- **This repo's engineering standards.** They are rough placeholders, and section 13 says how they are refined.
- **The writing standard as a detail file.** It ships as the detail file of LAW-000009.
  A detail file has a fixed four-part body, changes only by amendment, and is deleted when its law is amended. None of the three suits the standard.
  Suggested: exempt it from the four-part body, accept that a change to the standard is an amendment, and carry the file to the new ID.
- **A repo that is empty at install.** `0001-architecture.md` cannot pass the legacy test when nothing is in the repo at the install commit.
  A repo with no commits has no install commit to record.
  Suggested: `scaffold` refuses until the repo has a first commit, `init` skips `0001`, and the first architecture decision goes to a table.

The skill names, agent names, models, and effort levels in section 12 are settled as suggested.

### Checked against the Claude Code docs

- A subagent can spawn subagents, up to three layers below the main session by default.
- An agent file sets its model, effort, and tools in frontmatter.
- A subagent that has the `SendMessage` tool can resume a subagent it spawned. The resumed agent keeps its full history and reports back to the agent that resumed it.
- The docs state this for interactive sessions only. For a headless session, the packet fallback covers a seat that cannot be resumed.
- A subagent receives `CLAUDE.md`. The built-in Explore and Plan agents do not.
- A plugin can declare options that the user sets once, and skills and hooks can read them.
- A plugin's hook can deny Edit, Write, and Bash calls by path or command, in the main session and in subagents.
- One GitHub repo can be both the marketplace and the plugin.
- Plugin skills and agents are prefixed with the plugin name. A plugin skill with no `name` field has no bare command.
- On a shared bare name, a project or user agent outranks a plugin agent.
- Not checked: that a plugin cannot ship permission rules. The hook is the blocking mechanism either way.
- Not stated in the docs: that the full `avalon:<agent>` name works as the Agent tool's agent type. A fixture test covers it.
- An `@` import in `CLAUDE.md` expands for a subagent. The docs imply it, and a live test with a general-purpose subagent confirmed it.
- An import that points outside the repo needs a one-time approval. The registry is inside the repo, so it needs none.

### Settled

- The plugin is named `avalon`.
- The user or any agent may propose a law, and an agent may convene a round table itself.
- Every law is marked with its origin: `core`, `user`, or `agent`.
- A table convened by an agent cannot change a `user` or `core` law without the user's confirmation.
- Every decision that is being made goes to the round table: a new ADR, a reversal, or a retirement. The user has the final say.
- Core ADR `0002` is recorded at install as the user's decision, with no table.
- The user confirms an `agent` law or an `agent` ADR without a table, and the ledger records it as decided by `user`.
- A legacy decision is only recorded, with no table. Legacy means the decision was in effect at the install commit.
  The script checks the covered paths and the named evidence, and the user confirms it.
- The document size cap applies to ADRs, design docs, and law detail files. The registry, the archive, the ledger, the indexes, and the glossary are exempt.
- Five seats sit at every table. The Enforcer sits on laws, and the Scout takes its place on decisions.
- A table convened by an agent cannot reverse an ADR of origin `user` without the user's confirmation.
- Every round-table decision is recorded in the ledger file.
- The script never writes to git, and the chair does not commit. The session that owns the work commits, to the conventions of the repo.
- Frontmatter carries each document's metadata.
- Direct writes to the law files are blocked by a hook and detected by a checksum.
- The script runs on Python 3 with the standard library only.
- This repo's engineering standards are rough placeholders. The user and the agent refine them before any code is written.
- Dev-only tools may be dependencies, and the shipped script has none.
- Seats are read-only, and the chair records their votes.
- A document's `covers` list is capped at five folder-level globs.
- ADRs and design docs may hold Mermaid diagrams. Design docs may also hold images, stored in `docs/design/assets/`.
- The lint fails on any citation of a retired law or a retired ADR outside the archive and the ledger.
- The ADR index keeps no list of retired ADRs. The ledger row of a retirement is its record.
- A detail file is part of its law. The seats vote on it, and it changes only by amendment.
- A guideline of this repo lives in a design doc. Only laws and ADRs go to the round table.
- Seats are resumed across rounds, so each keeps its context.
- A prose editor agent owns whether a person can read the docs. It fixes prose in ADRs and design docs. It never changes meaning and never edits a law file.
- Paragraphs have no length cap. Each holds one point, and an edit is woven in instead of appended.
- A glossary at `docs/design/glossary.md` is the one home for definitions. It is a core design doc.
- A tally is always written as labelled counts in the order approve, amend, reject.
- The root is a per-repo setting in the config file, and it defaults to `docs/`. No environment variable is used.
- Mechanical steps are script commands that the skills point to.
- The user has the final say on every law. The table can object and ask for confirmation.
- Removing an amended law ends its chain. It does not restore the earlier law.
- Design docs describe the present only.
- Staleness is counted in commits. A design doc carries the date and the commit of its last check.
- The lint flags a time word for the prose editor and does not fail on one. It does not scan the registry, the archive, or the ledger for them.
- Laws use one key sequence, `LAW-000001`, with six digits. The category is a Scope tag.
- The registry is one file in ID order and is never split.
- Amended and removed laws live in a separate archive file.
- An archived law points to the law now in effect.
- The plugin installs from this repo on GitHub.
- A dedicated chair agent runs the round table, and subagents may spawn subagents.
