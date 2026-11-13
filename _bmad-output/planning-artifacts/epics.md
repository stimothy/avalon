---
stepsCompleted: [1, 2, 3, 4]
status: draft
created: '2026-11-11'
updated: '2026-11-11'
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-avalon-2026-11-11/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-avalon-2026-11-11/addendum.md'
  - '_bmad-output/planning-artifacts/architecture/architecture-avalon-2026-11-11/ARCHITECTURE-SPINE.md'
  - 'tmp/SPEC.md'
---

# Avalon - Epic Breakdown

## Overview

This document breaks the Avalon PRD and architecture spine into epics and stories that a developer agent can build one at a time.

It is a plan file. Like every file under `_bmad-output/`, it is removed after the work has landed.
It may name plan IDs such as `FR-12`, `AD-5`, and `AC-03`. Nothing that a story builds may name them, or name this file (AD-1).
Each story therefore states its acceptance criteria in full, so that a test can be named for the behaviour it proves.

**How to read an ID here:**

- `FR-n` and `NFR-n` are requirements in the PRD.
- `AD-n` is a decision in the architecture spine.
- `AC-nn` is an acceptance scenario in `tmp/SPEC.md` section 17, and `REQ-nnn` is a requirement there.
- `SM-n` is a success metric in PRD section 10.

**Which document governs.** The four inputs were written in order: `tmp/SPEC.md`, the PRD, the spine, and this file.
Where a later one changes an earlier one on purpose, it says so, and the later one is what the build follows. The PRD's addendum, section 6, lists each change to `tmp/SPEC.md`. The spine marks each of its changes `[ASSUMPTION]`. "Assumptions made at each gate" lists this file's.
Where two of them disagree and neither says so, that is a defect. The developer reports it and does not pick a side.
The PRD says its changes govern once the user signs it off. The user has not marked it final, so this order is a working rule until the user does.

**Gates taken without the user.** This breakdown was produced in one unattended run.
The workflow stops for the user after each of its four steps, and this run took the default at each stop.
"Assumptions made at each gate", near the end of this file, lists what was assumed, and "Answers to the open points" gives the reasoned answer to each point the first draft left open. Each one stands until the user changes it.

## Requirements Inventory

### Functional Requirements

Each line is the capability the PRD states. The PRD holds the testable consequences, and `tmp/SPEC.md` holds the requirement text.

**The document model**

- FR-1: A target repo holds exactly three kinds of governed document, and precedence runs laws, then ADRs, then the work, then design docs.
- FR-2: The user can set Avalon up in any kind of repo. No format, template, or check assumes that the work is code.
- FR-3: The chair applies the five-part law test to a proposed law, and the `adr` skill applies the two-part ADR test to a new decision.
- FR-4: Every document holds only present truth, each fact has one home, and an unknown is written as unknown.
- FR-5: Only the registry and the block load in every session. Everything else is reached through an index, and every document works without the plugin.

**Laws**

- FR-6: One registry file holds one table of every law in effect, with the columns `ID`, `Scope`, `Origin`, `Law`, `Detail`, in ID order.
- FR-7: A law ID is `LAW-` plus six digits from one sequence. It is never reused and never changes.
- FR-8: Every law carries an origin of `core`, `user`, or `agent`. The user confirms an `agent` law with `law confirm`, which adds one ledger row.
- FR-9: A law has a detail file only when one sentence cannot carry it. The chair drafts it, the seats vote on it with the law, and the script writes it.
- FR-10: An amendment creates a law with a new ID. The amended or removed row moves to the archive, with `Replaced by` and `Now in effect`, and its detail file is deleted.
- FR-11: No tracked text file outside the archive and the ledger cites a retired law or ADR. The lint fails on one, and `law amend` and `law remove` print every citation.
- FR-12: The config file sets a soft cap on the registry (default 100). It presses and never blocks.

**The ledger**

- FR-13: The script appends one ledger row for every round-table decision and every confirmation by the user, in seven fixed columns.
- FR-14: A tally is labelled counts in the order approve, amend, reject, or `none`. The script writes it from the recorded votes.

**The round table**

- FR-15: A law changes only through a round table, and a decision goes to one before it is carried out, with three named exceptions. Related proposals may be heard as a slate.
- FR-16: A dedicated chair runs every round table in its own context. The proposer never chairs. The chair changes law files only through the script.
- FR-17: Five seats sit with fixed perspectives. The Enforcer is the fifth seat on a law matter and the Scout on a decision matter. A seat only reads.
- FR-18: The chair screens a proposal, the `prose-editor` reviews the wording, and the seats vote in at most three rounds. Round 1 is blind and parallel, and later rounds go to the same seats by message.
- FR-19: On a unanimous vote, or after round 3, the chair adopts, adopts with final edits, or rejects, and registers through the script. The chair never commits.
- FR-20: The user has the final say. Nothing is registered over the user's proposal until the user answers, and a command that claims the user's authority becomes a permission prompt.
- FR-21: A round table that an agent convenes registers only where the origin allows, and a daily cap (default 5) limits how many agents convene on their own.
- FR-22: A skill stops before it convenes when the nesting depth setting is too low. A round table that fails part-way registers nothing.

**ADRs**

- FR-23: An ADR is one living document for one decision topic, with a numbered file name, fixed frontmatter, five body sections, and a changelog.
- FR-24: A reversal or a retirement goes to a round table, and adding detail does not. The user confirms an `agent` ADR with no round table.
- FR-25: A decision in effect before Avalon was installed is recorded without a round table when it passes the three-part legacy test.

**Design docs, the glossary, and indexes**

- FR-26: A design doc describes the present only, and the script lists every design doc that is stale under the stamp rule.
- FR-27: The glossary is one alphabetical table, the one home for a definition, and it never holds a rule.
- FR-28: The script reads and writes frontmatter, generates both indexes, checks `covers`, and `for` lists the documents that cover a path.

**The writing standard**

- FR-29: Every document follows the prose rules of the writing standard, which ships as the detail file of a core law.
- FR-30: ADRs and design docs may hold Mermaid diagrams of four types within a node cap. Design docs may hold images, and ADRs may not.

**Setup, layout, loading, and conflict handling**

- FR-31: The user installs Avalon from its GitHub repo, which is the marketplace. The plugin has no `bin/` folder and declares the `default_root` option.
- FR-32: `init` gives every target repo the same core set and is safe to run again. It handles an empty repo, a repo with no commit, existing ADRs, and the `AGENTS.md` offer.
- FR-33: The root is resolved from the config file, then the `default_root` option, then `docs/`. Working files live in a `.avalon/` folder that ignores itself, and `move-root` moves the tree.
- FR-34: `init` writes the block into `CLAUDE.md` between two fixed comment lines, and the block imports the registry.
- FR-35: A working agent never resolves a conflict silently. Each of six kinds of conflict has one response.

**Skills and supporting agents**

- FR-36: The user invokes seven skills as `/avalon:<skill>`, and every agent is spawned by its full name.
- FR-37: `check` audits the docs and changes nothing. `sync` brings the docs back in line after work.
- FR-38: The `law-reviewer` reports each violation with the ID, the location, and one of three confidence levels. It never fixes.
- FR-39: The `tech-writer` writes and edits ADRs and design docs to the writing standard. It invents no reason and never writes law files.
- FR-40: The `prose-editor` reads each document as a newcomer, fixes prose in ADRs and design docs, and only suggests for a law.
- FR-41: Each of the ten agent files sets its own model, effort, and tools. None names Fable or Haiku.

**The script**

- FR-42: One script does every mechanical step and prints the files it changed. An agent runs `for` before a change and reads `status`.
- FR-43: The script reads git and never writes to it.
- FR-44: The hook and a checksum guard the laws folder. The script refuses to register what the round table has not decided. The hook asks on a flagged command and approves the plugin's own everyday commands.
- FR-45: `lint` checks the structure of every document. It fails on each structural error and only flags a time word or a very long sentence.

**Building and proving Avalon in this repo**

- FR-46: The plugin ships eight templates, and the repo holds three fixtures, one with decoy agents and a decoy `docs/adr/` folder.
- FR-47: The user and the agent refine the repo's engineering standards into working standards before any code is written.
- FR-48: The Avalon repo runs Avalon in a fixed build order. Its documents follow the Avalon process from build step 1, and no permanent file cites a plan.

**The public repo and its releases**

- FR-49: Avalon is released under the MIT licence, and the templates carry the MIT No Attribution licence.
- FR-50: The README lets a person who has never seen Avalon decide whether to use it and install it without help.
- FR-51: The repo carries the community files that GitHub's community standards checklist names.
- FR-52: A user receives numbered releases. `master` installs at every commit, the plugin lives in a subfolder, and the manifest sets no version.
- FR-53: No tracked file and no governed document publishes a secret or a person's private details.
- FR-54: The shipped script needs Python 3.9 or later and nothing else, on macOS and Linux, and it fails plainly when the interpreter is missing or too old.

**Standards, gates, and releases**

- FR-55: Code is written test-first. Tests are unit, integration, or end-to-end, in Arrange, Act, Assert form, with no git and no network. Contract tests and plugin evals are a fourth and a fifth suite.
- FR-56: Code meets an 80% coverage floor, passes a linter, a formatter, and a type checker, and follows DRY and SOLID. The unit run has a time budget.
- FR-57: No directory is a grab bag, with two exceptions: the docs tree, and the layout Claude Code fixes for a plugin.
- FR-58: The gates run on a pull request into `master` that is ready for review, and nowhere else. A newer push cancels an older run.
- FR-59: A release workflow runs on a merge into `master` and publishes the next semantic version, chosen by a `major`, `minor`, or `patch` label.

**Merges, upgrades, and CI in a target repo**

- FR-60: One script command joins law and ADR changes from two branches after a git merge.
- FR-61: A later plugin version works in a repo an earlier one set up. `migrate` changes the layout of a tree and never what it says.
- FR-62: The Avalon docs give a target repo a recipe for running the lint in CI.

### NonFunctional Requirements

- NFR-1: Context cost. Only the registry and the block load in every session. At the default cap of 100 laws the registry costs about 3,500 tokens, and the block does not grow with the repo.
- NFR-2: Bounded deliberation. A matter takes at most three rounds of five votes.
- NFR-3: No dependencies in the shipped script. It runs on Python 3 with the standard library only, with no virtual environment.
- NFR-4: No collisions. Every name is scoped to Avalon, and `init` never writes into a folder that holds content it did not create.
- NFR-5: No data collection. The script opens no network connection, and Avalon collects no usage data.

The PRD sets no latency or throughput target.

### Additional Requirements

These come from the architecture spine. Each one shapes at least one story.

**Starting point**

- There is no starter template. The repo is greenfield, and the spine's Structural Seed gives the starting layout. The first story creates this repo's own docs tree by hand (AD-19), not a code skeleton.
- The spine names eight build steps, taken from the PRD. The epics follow that order.

**Rules that bind every story**

- AD-1: Plans are temporary. No tracked file outside `_bmad-output/`, `tmp/`, and `_bmad/` names a plan file or a plan ID. A gate scans tracked files, and the pull request title and body.
- AD-2: Judgment lives in prompts, and mechanics live in the script. A skill or agent file names a command and never restates it.
- AD-19: This repo follows the Avalon process from its first document. Every law and ADR of this repo goes to a round table before it is written, with stand-in subagents until the plugin's agents exist, and hand-written records until the script exists.
- Consistency conventions: names, test names, text encoding, dates, config keys, the cap defaults, and no folder named `utils`, `helpers`, `misc`, or `common`.

**The script**

- AD-3: One entry file, `plugin/script/avalon`, with the code in the `avalonlib` package beside it. It exits 2 below Python 3.9, and silently exits 0 for `hook`.
- AD-4: `rules`, `formats`, and `model` are pure. Files, git, and the clock sit behind ports. A gate checks the layer imports and a denylist of network modules.
- AD-5: A writing command is one all-or-nothing change set, under a lock, with a journal. The checksum is verified before a write and recorded last. Path rules limit where the script writes.
- AD-6: Each file format has one home in `formats`, one template for its fixed text, one parser for config and frontmatter, one `covers` matcher, a fixed checksum recipe, and one integer `system_version`.
- AD-7: Each file has one writer. A table names the writer of every path in a target repo and what holds the rule.
- AD-10: Work in progress is a matter, with one folder under `.avalon/matters/`, three states, and one function that decides whether anything may be registered, by four routes.
- AD-11: One adapter reads git through a fixed list of read-only commands. Nothing writes git. No rule computes from a commit ID that a file stores: the legacy test finds the install in the history.
- AD-12: One resolver finds the config file and the root. A fixture is always copied out of this repo before use.
- AD-13: The command table is closed. Exit codes are 0, 1 for a lint failure, and 2. Output is `key: value` lines and a `changed:` block. A test parses every command line that a prompt quotes.

**The hook and the user's authority**

- AD-8: The hook is the script's `hook` command. It denies writes to protected paths, approves a Bash call only when six tests pass, and always exits 0.
- AD-9: The user's authority is the leading flag `--as-user`, on a closed list of commands. The hook answers `ask` in proven permission modes and `deny` elsewhere and in any subagent. The chair never runs a flagged command.

**Prompts**

- AD-14: Each piece of prompt text has one home. The spine fixes each agent's tool set and what each agent returns.

**Tests, the repo, and delivery**

- AD-15: Five suites with a fixed reach: unit, integration, end-to-end, contract, and plugin evals. One shared guard fails any process start or network connection in the first three. Coverage floor 80. The first four also run on Python 3.9.
- AD-16: `plugin/` holds what a user installs and nothing else. The marketplace file names `./plugin`.
- AD-17: Workflows hold no logic. Anything that computes or branches is tested Python under `devtools/`. Actions are pinned by commit SHA.
- AD-18: `gates.yml` and `pr.yml` gate a pull request, and one final job gives the verdict. A ruleset on `master` requires a pull request, both checks, an up-to-date branch, and squash merges.
- AD-20: `release.yml` catches up every unreleased commit, makes the tag and the GitHub release in one call, and refuses `major` below `v1.0.0` unless the owner allows it.
- Stack: the spine's Stack table pins every tool version. A story that adds a tool uses that version.
- The owner applies the repository settings in build step 1, in stages. The parts that need no workflow are on before the first pull request. Each job becomes a required check when its workflow lands. The secret for the evals is stored last, and only the owner enters its value.

**Done, for every story**

A story is done when all of these hold. No story repeats them in its own criteria.

- Every file the story adds or changes names no plan file and no plan ID, and neither does the pull request's title or body (AD-1). A test is named for the behaviour it proves.
- Code is written test-first, in the suite that fits, with Arrange, Act, and Assert in that order. Each new test proves something no other test proves (FR-55).
- Code sits in the layer and the folder the architecture names, and no folder becomes a grab bag (AD-4, FR-57).
- The pull request passes every gate that exists at that time, and carries exactly one version label (FR-58, FR-59). Where a gate does not exist yet, the pull request says which of that gate's checks its author ran by hand.
- A story that needs the user prepares everything else first, and then stops at one named ask. An unattended run starts no story that waits on that ask.
- A law or an ADR that this repo needs goes to a round table before it is written. A design doc that the change makes untrue is updated in the same change (AD-19).
- A script command a skill or agent file quotes exists, and is written on one line in the form the parse test reads (AD-13).
- The session commits. No agent and no script command writes to git.

**What the spine defers, and the build step that settles it**

- Step 1: the secret-scan tool; whether the macOS runner's system Python is 3.9; whether Dependabot handles `uv.lock`; what the release notes hold beyond the generated list.
- Step 3: module names inside each script layer; the format of a matter ID; how this repo's hand-written tree gets its first checksum.
- Step 4: the hook's rules for spotting a write inside a Bash command; proof by plugin eval of each permission-mode row, of the hook's approval inside a subagent, and that a script command reaches Bash with the plugin root filled in; the lowest supported Claude Code version.
- Steps 4 to 7: the model and effort of each agent, and the eval cases with their scoring.
- Step 8: how the CI recipe fetches `plugin/script/`.
- The first release that changes a format: the steps inside `migrate`.
- Each command's own build step: its arguments and flags beyond AD-9 and AD-13.

**Release gates for `v1.0.0`**

- SM-1: All 45 acceptance scenarios pass.
- SM-2: `claude plugin validate .` passes.
- SM-3: This repo's own round tables have ratified the nine core laws.
- SM-11: A person who follows only the README reaches a passing lint after `init`, once on each supported operating system.
- SM-12: GitHub's community standards checklist is complete, and the secret scan finds nothing.

### UX Design Requirements

None. No UX design contract exists, and none is needed.
Avalon has no screens. A user meets it through slash commands, permission prompts, and the text a skill or the script prints.
The spine fixes the script's output (AD-13) and the wording duties of each prompt (AD-14), and the PRD fixes what each message must say.

### FR Coverage Map

Each FR names the epic that delivers most of it first, then every other epic that completes it.

- FR-1: Epic 2 - the core laws and the block state the three kinds and the precedence.
- FR-2: Epic 5 - `init` works on a code repo, a library, and a story bible. Epic 2 keeps every template free of code-only wording.
- FR-3: Epic 4 - the chair applies the law test. Epic 6 - the `adr` skill applies the ADR test.
- FR-4: Epic 2 - the core laws and the writing standard hold the rule. Epics 4 to 7 - each writing agent follows it.
- FR-5: Epic 3 - `scaffold` leaves the registry and the block loading in every session.
- FR-6: Epic 3 - the registry format and the law commands. Epic 2 - its template.
- FR-7: Epic 3 - ID allocation.
- FR-8: Epic 3 - origin and `law confirm`. Epic 4 - the `law` skill's confirmation flow.
- FR-9: Epic 3 - the script writes the adopted detail file. Epic 4 - the chair drafts it.
- FR-10: Epic 3 - `law amend`, `law remove`, and the archive.
- FR-11: Epic 3 - the lint check and the printed citations for laws. Epic 5 - the same for ADRs.
- FR-12: Epic 3 - the cap and the count. Epic 4 - the round table's duty past the cap.
- FR-13: Epic 3 - the ledger and its rows for laws. Epic 5 - the rows for ADRs.
- FR-14: Epic 3 - the tally format and its lint check.
- FR-15: Epic 4 - law matters. Epic 6 - decision matters. Epic 1 - this repo's stand-in tables.
- FR-16: Epic 4 - the chair.
- FR-17: Epic 4 - the six seat files and a law table. Epic 6 - the Scout sits on a decision.
- FR-18: Epic 4 - screening and the three rounds.
- FR-19: Epic 4 - the outcome for a law. Epic 6 - the outcome for a decision.
- FR-20: Epic 4 - the flag, the prompt, and the proof in each permission mode. Epic 3 - the script refuses a flagged command without the flag.
- FR-21: Epic 4 - the limits and the daily cap. Epic 3 - the count in `matter open`. Epic 6 - the limits for a `user` ADR.
- FR-22: Epic 4 - the depth check in the `law` skill. Epic 5 - the warning in `init`.
- FR-23: Epic 5 - the ADR format and `adr new`. Epic 2 - its template.
- FR-24: Epic 5 - the ADR commands. Epic 6 - the `adr` skill.
- FR-25: Epic 5 - the legacy test and `0001-architecture.md` at `init`. Epic 6 - a legacy record at any later time.
- FR-26: Epic 7 - `stale` and `verify`. Epic 2 - the design doc template.
- FR-27: Epic 3 - the glossary format and its lint check. Epic 5 - `init` seeds it. Epic 6 - the `design` skill keeps it.
- FR-28: Epic 3 - frontmatter, `index`, and the `covers` checks. Epic 7 - `for`.
- FR-29: Epic 2 - the writing standard. Epic 3 - the lint flags. Epic 4 - the `prose-editor`.
- FR-30: Epic 2 - the rules in the writing standard. Epic 3 - the lint checks.
- FR-31: Epic 1 - the marketplace file, the manifest, and `claude plugin validate`. Epic 5 - the `default_root` option reaches `scaffold`.
- FR-32: Epic 5 - `init` and the core set. Epic 3 - `scaffold`.
- FR-33: Epic 3 - the resolver, the config file, and `.avalon/`. Epic 5 - the root that `init` proposes. Epic 8 - `move-root`.
- FR-34: Epic 3 - `scaffold` writes the block. Epic 2 - its text.
- FR-35: Epic 4 - conflicts with a law. Epic 6 - conflicts with an ADR. Epic 2 - the block and the core law that state the rule.
- FR-36: Epic 4 - `law`. Epic 5 - `init`. Epic 6 - `adr`, `design`, `intake`. Epic 7 - `check`, `sync`.
- FR-37: Epic 7 - `check` and `sync`.
- FR-38: Epic 7 - the `law-reviewer`.
- FR-39: Epic 5 - the `tech-writer`.
- FR-40: Epic 4 - the `prose-editor`. Epic 7 - its report-only pass under `check`.
- FR-41: Epic 4 - eight agent files. Epic 5 - the `tech-writer`. Epic 7 - the `law-reviewer`.
- FR-42: Epic 3 - the command line and its output. Epic 7 - `status` and `for`.
- FR-43: Epic 3 - the git port and its read-only adapter.
- FR-44: Epic 3 - the checksum and the refusal to register. Epic 4 - the hook.
- FR-45: Epic 3 - the lint. Epic 5 - the ADR checks. Epic 8 - the checks for a merge and an older tree.
- FR-46: Epic 2 - the templates. Epic 4 - the first fixture. Epic 5 - the other two, and the decoys.
- FR-47: Epic 1 - the standards are refined before any code.
- FR-48: Epic 1 - the process starts. Epic 2 - the core laws are ratified. Epic 3 - the first checksum, and the Avalon lint joins the gates. Epic 4 - the plugin takes over from the stand-ins. Epic 8 - the plans are retired.
- FR-49: Epic 1 - the licence. Epic 2 - the licence line on the templates.
- FR-50: Epic 1 - the first README. Epic 4 - requirements and the hook. Epic 8 - the README a stranger can install from.
- FR-51: Epic 1 - the community files. Epic 4 - the security policy.
- FR-52: Epic 1 - the plugin subfolder and the release workflow. Epic 8 - `v1.0.0`.
- FR-53: Epic 1 - the ignore rules, the secret scan, and the scan of tracked files. Epic 3 - no format holds a name, an email, or an absolute path.
- FR-54: Epic 3 - the entry file and its plain failure. Epic 4 - the message in a skill and the lowest Claude Code version. Epic 1 - the gates on two Pythons and two operating systems.
- FR-55: Epic 1 - the five suites and the shared guard.
- FR-56: Epic 1 - coverage, the linter, the formatter, the type checker, and the unit time budget.
- FR-57: Epic 1 - the law and the layout. Every later epic follows it.
- FR-58: Epic 1 - the gates. Epic 3 - the Avalon lint and the import gates join them. Epic 4 - the plugin evals join them.
- FR-59: Epic 1 - the label gate and the release workflow.
- FR-60: Epic 8 - `merge`.
- FR-61: Epic 3 - the system version and the refusals. Epic 8 - `migrate` and the upgrade notes.
- FR-62: Epic 8 - the CI recipe.

The NFRs map the same way:

- NFR-1: Epic 3 - the registry and the block are all that load. Epic 2 - the block is fixed text.
- NFR-2: Epic 3 - `vote` refuses a fourth round. Epic 4 - the chair's procedure.
- NFR-3: Epic 3 - the import gate on the script.
- NFR-4: Epic 3 - `scaffold` refuses a foreign root. Epic 5 - `init` on the decoy fixture.
- NFR-5: Epic 3 - the network denylist. Epic 1 - the README says so.

## Epic List

The PRD fixes eight build steps and says the build follows them (FR-48). Section 9.3 of the PRD ties a release milestone to each.
So there are eight epics, one for each build step, and each is named for what a person can do when it lands.
An epic needs only the epics before it. Epics 1 to 4 are the first slice: after Epic 4, Avalon governs its own repo.

### Epic 1: A public repo that governs itself and gates every change

A contributor can clone the repo, set up the tools, and open a pull request that the gates check. Every merge releases a version below 1.0.
The repo holds its own docs tree from the first day. Its engineering standards are refined with the user, and a stand-in round table hears each one that is a law or an ADR, along with the architecture.
This is build step 1.

**FRs covered:** FR-15 (stand-in tables), FR-31, FR-47, FR-48, FR-49, FR-50, FR-51, FR-52, FR-53, FR-54 (the gate matrix), FR-55, FR-56, FR-57, FR-58, FR-59. NFR-5.

### Epic 2: The words every repo starts with

The text that Avalon will write into every target repo is settled. This repo's round tables ratify the writing standard and the nine core laws, and the plugin holds a template for every governed document.
This is build step 2.

**FRs covered:** FR-1, FR-2 (templates), FR-4, FR-29, FR-30, FR-34 (the block's text), FR-35 (the rule's text), FR-46 (templates), FR-48 (core laws ratified), FR-49 (templates). The template side of FR-6, FR-9, FR-10, FR-23, FR-26, FR-27.

### Epic 3: One script sets up a repo and keeps its law record

A person can run one script to set Avalon's tree up in a repo. From then on, every session in that repo loads the laws.
The script registers, amends, removes, and confirms laws from recorded votes. It keeps the archive and the ledger, guards the record with a checksum, and lints the tree.
This repo's hand-written tree passes the lint and gets its first checksum.
This is build step 3.

**FRs covered:** FR-5, FR-6 to FR-14, FR-20 (the script's side), FR-21 (the count), FR-27, FR-28, FR-29 and FR-30 (lint), FR-32 (`scaffold`), FR-33, FR-34, FR-42, FR-43, FR-44 (checksum and refusal), FR-45, FR-48 (first checksum), FR-53 (formats), FR-54, FR-58 (Avalon lint and import gates), FR-61 (the version check). NFR-1 to NFR-5.

### Epic 4: Laws change through a round table, and the user has the final say

The user, or a working agent, proposes a law with `/avalon:law`. A chair and five seats hear it, and the script registers the outcome.
The hook guards the record, lets a round table run without a prompt at every step, and puts every claim of the user's authority in front of the user.
Avalon then runs in this repo through the plugin. This is the first release that governs a repo.
This is build step 4.

**FRs covered:** FR-3 (law test), FR-8, FR-9, FR-12, FR-15 to FR-22, FR-35, FR-36 (`law`), FR-40, FR-41, FR-44 (the hook), FR-46 (first fixture), FR-48, FR-50, FR-51 (security policy), FR-54, FR-58 (plugin evals).

### Epic 5: Set Avalon up in any repo

The user runs `/avalon:init` in an application, a library, or a story bible, and gets the same core set: the laws, the block, an overview, a glossary, and the two core ADRs.
The script gains the ADR commands, and the three fixtures prove `init` on each profile.
This is build step 5.

**FRs covered:** FR-2, FR-11 (ADRs), FR-13 (ADR rows), FR-22 (`init` warning), FR-23, FR-24 (commands), FR-25, FR-31 (`default_root`), FR-32, FR-33 (root choice), FR-36 (`init`), FR-39, FR-41, FR-45 (ADR checks), FR-46 (fixtures). NFR-4.

### Epic 6: Record decisions and describe the repo

The user, or a working agent, takes a decision to a round table with `/avalon:adr`, and the `tech-writer` writes the ADR.
`/avalon:design` writes, updates, splits, and merges design docs. `/avalon:intake` sorts a design conversation into laws, decisions, and description.
This is build step 6.

**FRs covered:** FR-3 (ADR test), FR-15, FR-17 (Scout), FR-19, FR-21, FR-24, FR-25, FR-27, FR-35, FR-36 (`adr`, `design`, `intake`).

### Epic 7: Keep the docs true

A working agent finds what covers the path it is about to change. The user audits the docs with `/avalon:check`, and brings them back in line after work with `/avalon:sync`.
The script lists stale design docs, stamps a reviewed one, and prints one status summary.
This is build step 7.

**FRs covered:** FR-26, FR-28 (`for`), FR-36 (`check`, `sync`), FR-37, FR-38, FR-40 (report-only), FR-41, FR-42 (`status`, `for`).

### Epic 8: Ready for version 1.0

Two branches that each changed laws can be joined. A root can be moved. A tree in an older format can be brought up to date. A target repo can run the lint in CI.
Every release gate passes, a stranger can install from the README alone, and `v1.0.0` ships.
This is build step 8.

**FRs covered:** FR-33 (`move-root`), FR-45 (merge and upgrade checks), FR-48 (plans retired), FR-50, FR-52 (`v1.0.0`), FR-60, FR-61, FR-62.

## Epic 1: A public repo that governs itself and gates every change

A contributor can clone the repo, set up the tools, and open a pull request that the gates check. Every merge releases a version below 1.0.
The repo holds its own docs tree from the first day, and a stand-in round table hears its first laws and decisions.

Stories 1.1 to 1.6 write no code. FR-47 puts the standards before any code, and AD-19 puts the architecture's round table before the code that follows it.

### Story 1.1: The repo's public face

As a visitor to the repo,
I want a licence, a README that says where the project stands, a code of conduct, and ignore rules,
So that I know what Avalon is, on what terms I may use it, and that nothing private is published.

**Covers:** FR-49, FR-50, FR-51, FR-53, FR-58; NFR-5; AD-18.

**Acceptance Criteria:**

**Given** the repo on GitHub, before this story's pull request is opened
**When** the owner has applied the first settings, or has approved the session's commands for them
**Then** a change reaches `master` only through a pull request
**And** merges are squash only, with the pull request's title and description as the commit message
**And** the labels `major`, `minor`, and `patch` exist, and this pull request carries one
**And** private vulnerability reporting is on, so that the route in the code of conduct works.

**Given** the top of the repo
**When** a person opens `LICENSE`
**Then** it holds the MIT text, and its copyright line names "the Avalon contributors"
**And** no person's name and no email address appears in it.

**Given** the README
**When** a person reads it
**Then** it says what Avalon is, that it is a pre-release, and that it holds no working round table yet
**And** it says that Avalon collects no usage data, and that the licence is MIT
**And** it links to the licence and the code of conduct.

**Given** `CODE_OF_CONDUCT.md`
**When** a person looks for how to report a breach
**Then** the file is the Contributor Covenant, version 3.0
**And** it sends a conduct report to the repo's private vulnerability reporting form, marked as a conduct report
**And** it sends a report about a maintainer to GitHub's own abuse report
**And** it publishes no personal address.

**Given** the ignore rules
**When** a contributor creates local tool state, a virtual environment, a personal configuration file, or a working file such as a decision log
**Then** git does not track it.

### Story 1.2: This repo's own Avalon tree, created by hand

As the user,
I want this repo to hold an Avalon docs tree from its first day,
So that every rule, decision, and description has a lasting home before any code exists.

**Covers:** FR-32, FR-34, FR-48; AD-19. The formats are in `tmp/SPEC.md` sections 3, 5, 6, 7, 9, and 11.

**Acceptance Criteria:**

**Given** the top of the repo
**When** the story is done
**Then** `docs/laws/` holds `LAWS.md`, `archive.md`, `ledger.md`, and the detail file of LAW-000009
**And** `docs/adr/` holds `README.md` and `0002-documentation-system.md`
**And** `docs/design/` holds `README.md`, `overview.md`, and `glossary.md`
**And** each file is in its final format, as an install would create it.

**Given** the registry
**When** it is read
**Then** it holds the nine core laws as LAW-000001 to LAW-000009, each with origin `core` and its draft text
**And** LAW-000009 links to its detail file, which holds a draft of the writing standard
**And** the archive and the ledger hold no row.

**Given** `.avalon.yml` at the top of the repo
**When** it is read
**Then** it holds the root `docs`, a profile, the system version 1, the install time in UTC, the install commit, the caps at their defaults, and the scope list
**And** it holds no checksum
**And** the install commit is the commit the tree was created on, kept as a record.

**Given** `CLAUDE.md`
**When** a session opens in this repo
**Then** the block sits between the two marker lines and imports the registry
**And** the registry is in the session's context.

**Given** `0002-documentation-system.md`
**When** it is read
**Then** it records the decision to use Avalon in this repo, with the root path
**And** it has origin `user`, and its changelog line carries `(user)`
**And** no round table sat for it, and the ledger holds no row for it.

**Given** the overview and the glossary
**When** they are written
**Then** a stand-in writer wrote each, and a stand-in editor edited each against the draft writing standard
**And** the glossary starts with Avalon's own terms
**And** the overview leaves out every section that does not apply yet.

### Story 1.3: The engineering standards, refined with the user

As the user,
I want each engineering standard given exact wording, a kind, and a check, and to review each one,
So that the standards I stated bind the first line of code in the form I agreed to.

**Covers:** FR-47, FR-55, FR-56, FR-57; AD-1. The proposals are in `addendum.md` section 5.

**Acceptance Criteria:**

**Given** the ten standards the user stated, and the rule that a permanent file cites only this repo's own laws, ADRs, and design docs
**When** the agent presents them
**Then** each has proposed wording, a kind (law, ADR, or guideline), and a stated check
**And** each proposed law names its scope, and a scope that the scope list lacks is added only when the user agrees
**And** the user reviews each one, and accepts it or changes it.

**Given** a standard the user accepts as a guideline
**When** the story is done
**Then** a design doc of this repo holds it
**And** a stand-in writer wrote the doc, a stand-in editor edited it, and the design index lists it.

**Given** a standard the user accepts as a law or an ADR
**When** the story is done
**Then** its agreed wording is held as a proposal for a round table, in a matter folder under `.avalon/`
**And** nothing is registered yet.

**Given** the repo when this story is done
**When** its tracked files are listed
**Then** no code, no test, and no workflow exists yet.

### Story 1.4: A stand-in round table hears the standards that are laws

As the user,
I want a round table to hear each standard that is a law, before the plugin's own agents exist,
So that this repo's first laws were heard like every law after them.

**Covers:** FR-15 to FR-21, FR-48; AD-19. The procedure is in `tmp/SPEC.md` section 4.

**Acceptance Criteria:**

**Given** a law proposal from Story 1.3
**When** the table sits
**Then** a stand-in chair that did not propose it runs the table
**And** five stand-in seats sit: the Practitioner, the Skeptic, the Jurist, the Steward, and the Enforcer
**And** each is a subagent briefed for its one role, on its planned model: Opus for the chair and the Jurist, Sonnet for the rest.

**Given** round 1
**When** the seats vote
**Then** they vote in parallel, and no seat sees another's vote
**And** each vote is approve, amend with proposed wording, or reject, with a short reason.

**Given** a round that is not unanimous
**When** the chair continues
**Then** it revises the text, shows every seat every vote and reason, and asks the same five seats whether the revision resolves their objection
**And** no table runs a fourth round.

**Given** the table adopts a law
**When** the stand-in chair records it by hand
**Then** the law is the last registry row, with the next ID after LAW-000009 and the proposer's origin
**And** the ledger gains one row with the date, the decision, who proposed it, who decided it, the rounds, the tally, and the dissent
**And** the tally is labelled counts in the order approve, amend, reject, and the counts add up to five.

**Given** the table rejects a proposal
**When** the stand-in chair records it
**Then** the ledger gains one row for the rejection, and the registry does not change.

**Given** the table would reword or reject a proposal that the user made
**When** the chair decides
**Then** nothing is registered until the user accepts, counters, or directs that it be registered as written
**And** a law registered as written over the table's objection has `user override` in its ledger row, with each dissenting seat named.

**Given** the proposals of this story
**When** the table sits
**Then** it hears them as one slate, in one sitting, and each gets its own vote and its own ledger row
**And** the chair may split a slate that is too large for one packet.

**Given** the stand-in tables of Epics 1 and 2
**When** they are counted
**Then** five sittings are planned: the standards that are laws, the architecture, the tooling and delivery decisions, the writing standard, and the other eight core laws
**And** a sixth sitting, and each one after it, starts only after the user's go-ahead.

**Given** the briefs for the stand-in chair and seats
**When** the story is done
**Then** no tracked file holds them.

### Story 1.5: A stand-in round table hears the architecture

As the user,
I want the architecture heard by a round table and recorded as this repo's first ADR,
So that the code has a decision of record to follow, and no plan is the only home of that decision.

**Covers:** FR-23, FR-48; AD-1, AD-19. The ADR format is in `tmp/SPEC.md` section 5.

**Acceptance Criteria:**

**Given** the architecture decisions in the spine
**When** they are proposed to the table
**Then** each is stated in its own words, with no plan ID and no plan file name
**And** each carries the origin of whoever proposed it: `agent` for a call the planning work reasoned, and `user` for one the user stated.

**Given** a decision matter
**When** the table sits
**Then** the Scout sits in place of the Enforcer, and asks whether the real alternatives were considered
**And** the Skeptic argues for the strongest alternative, including doing nothing.

**Given** the table adopts the architecture
**When** it is recorded
**Then** a stand-in writer writes `docs/adr/0001-architecture.md`, and a stand-in editor edits it
**And** the file holds the keys `adr`, `summary`, `covers`, and `origin`, and the sections Context, Decision, Consequences, Alternatives rejected, and Changelog, in that order
**And** it records the repo's form, its major parts and their boundaries, and its primary technologies
**And** every line under Alternatives rejected carries the word "Rejected"
**And** the changelog line has a date, a marker, and a one-line summary
**And** the ledger gains one row for each decision the table made, and the ADR index lists the file.

**Given** an architecture call that fails the ADR test
**When** it is sorted
**Then** it gets no ADR, and a design doc describes it once the code it describes exists.

**Given** the table would reword or reject a decision that the user stated
**When** the chair decides
**Then** nothing is registered until the user answers.

**Given** an ADR recorded with origin `agent`
**When** the table has finished
**Then** the session shows the user the outcome, and offers to record the user's confirmation
**And** on a confirmation the origin becomes `user`, the changelog gains a `(user)` line, and the ledger gains one row decided by `user`, with `none` for the rounds, the tally, and the dissent
**And** without a confirmation the origin stays `agent`, and no later story waits for one.

### Story 1.6: A stand-in round table hears the tooling and delivery decisions

As the user,
I want the decisions behind the standards and the delivery path heard and recorded,
So that a later contributor can see why these tools, these suites, and this release path were chosen.

**Covers:** FR-47, FR-48, FR-55, FR-56, FR-58, FR-59; AD-15, AD-17, AD-18, AD-20.

**Acceptance Criteria:**

**Given** the decisions on the development tools, the five test suites and what each may reach, the two pull request workflows, and the release by label
**When** each is tested against the ADR test
**Then** one that passes goes to a decision table, by the procedure in Stories 1.4 and 1.5
**And** one that fails becomes a guideline in the design doc from Story 1.3.

**Given** each decision
**When** it is proposed
**Then** one that the user stated, such as gates only on a pull request that is ready for review, or a release chosen by a label, goes to the table as the user's proposal
**And** one that the planning work reasoned, such as a contract suite that starts git, goes as an agent's, and the user is offered the outcome to confirm, as in Story 1.5.

**Given** an adopted decision
**When** it is recorded
**Then** it extends an ADR that already owns its topic, or becomes an ADR with the next number when none does
**And** the ledger gains one row for it, and the ADR index lists every ADR.

**Given** the choice of each tool
**When** the ADR states it
**Then** the ADR names the tool and what it is for, and the lock file is the only home of its version.

**Given** the repo when this story is done
**When** its ledger is read
**Then** every law and every ADR in the repo, other than the nine draft core laws and `0002-documentation-system.md`, has a row that shows a table's decision or the user's.

### Story 1.7: A contributor can set up the tools and run each suite

As a contributor,
I want one command to set up the development tools and one command for each test suite,
So that I can work test-first from a fresh clone.

**Covers:** FR-54, FR-55, FR-56; AD-15, AD-16; the Stack.

**Acceptance Criteria:**

**Given** a fresh clone
**When** a contributor runs the documented setup command
**Then** a virtual environment that git ignores holds the development tools, at the versions in the lock file
**And** `pyproject.toml` requires Python 3.9 or later and builds no package
**And** nothing under `plugin/` needs those tools.

**Given** the `tests/` folder
**When** it is listed
**Then** it holds `unit/`, `integration/`, `e2e/`, `contract/`, and `fakes/`
**And** each of the four suites runs alone, with one command.

**Given** the top of the repo
**When** a contributor runs the test runner with no arguments
**Then** it collects tests only from `tests/`, and from no planning tool's folder.

**Given** a test in the unit, integration, or end-to-end suite
**When** it starts a process or opens a network connection
**Then** one shared guard fails it
**And** the guard has tests of its own
**And** the contract suite is outside the guard.

**Given** the unit suite
**When** its whole run takes longer than 10 seconds
**Then** a check fails.

**Given** the linter, the formatter, the type checker, and the markdown lint
**When** a contributor runs each
**Then** each runs with one command and passes on the repo
**And** the linter targets Python 3.9.

**Given** coverage
**When** it is measured
**Then** it counts the unit and integration runs together, over `plugin/script/` and `devtools/`
**And** a result below 80 fails.

**Given** Python 3.9 and the current Python release
**When** the four suites run on each
**Then** they pass on both.

### Story 1.8: A person can install the plugin from the repo

As a person who finds Avalon on GitHub,
I want to add the repo as a marketplace and install the plugin from it,
So that I receive only the plugin, and each later release reaches me through the same two commands.

**Covers:** FR-31, FR-49, FR-52; NFR-4; AD-16; AC-32; SM-2.

**Acceptance Criteria:**

**Given** the top of the repo
**When** `claude plugin validate .` runs
**Then** it passes
**And** the marketplace file lists one plugin, named `avalon`, whose source is `./plugin`.

**Given** the plugin manifest
**When** it is read
**Then** it names the plugin `avalon` and the licence `MIT`, and declares the option `default_root`
**And** it sets no version.

**Given** the `plugin/` folder
**When** it is listed
**Then** it holds its own copy of the licence, and no `bin/` folder
**And** nothing in it reads or imports a path outside it.

**Given** a machine that has never held Avalon
**When** a person runs the two install commands from the README
**Then** the plugin installs, and the installed copy holds no test, no fixture, no plan, and no workflow.

**Given** a local checkout
**When** a contributor starts Claude Code with the plugin folder as a plugin directory
**Then** the plugin loads for that session.

### Story 1.9: A gate scans tracked files for plan citations, home paths, and secrets

As a maintainer,
I want a gate that fails when a tracked file cites a plan, holds a path in someone's home folder, or holds a secret,
So that nothing temporary and nothing private reaches the public repo.

**Covers:** FR-48, FR-53, FR-58; AD-1, AD-17.

**Acceptance Criteria:**

**Given** a tracked text file outside the skipped folders
**When** it holds a plan ID as a whole, case-sensitive token of a plan prefix and digits, or names a plan file
**Then** the scan fails, and names the file and the line.

**Given** a tracked text file
**When** it holds the same letters inside a longer word, or in another case
**Then** the scan does not fail on it.

**Given** the folders the scan skips
**When** a contributor looks for the list
**Then** one file under `devtools/gates/` holds it
**And** the lock file is not scanned
**And** that file, the ignore file, `pyproject.toml`, and the markdown lint config are the only tracked files that name a plan folder.

**Given** the scan's own tests
**When** they need a sample ID
**Then** they build it at run time and store none.

**Given** a tracked file that holds a path inside a person's home folder
**When** the scan runs
**Then** it fails, and names the file and the line.

**Given** the title and the body of a pull request, passed in as text
**When** the scan runs on them
**Then** it applies the same check for plan citations.

**Given** the tracked files
**When** the secret scan runs
**Then** it fails on a finding
**And** this repo's docs record which tool does the scan.

### Story 1.10: Gate logic lives in tested code

As a maintainer,
I want everything in a workflow that computes or branches to be tested Python,
So that the standards reach the gates themselves.

**Covers:** FR-58; AD-17, AD-18.

**Acceptance Criteria:**

**Given** the list of paths a pull request changed
**When** the changed-path filter runs
**Then** it sets one output for each gate that applies only to some changes, saying whether that gate applies.

**Given** the results of every other job in the gates workflow
**When** the verdict runs
**Then** it passes only when each job succeeded, or was skipped because the filter said it did not apply
**And** it fails on a job that failed, was cancelled, or was skipped for any other reason.

**Given** a workflow file
**When** the workflow check runs
**Then** it fails on an action that is not pinned to a full commit SHA
**And** it fails on a workflow that does not state its permissions, and on a write permission outside the release job
**And** it fails on the `pull_request_target` trigger
**And** it fails on a job condition that is not one of the three allowed forms: the draft test, `always()` with the draft test on the final job, or a test of an output that a `devtools` command set.

**Given** the code under `devtools/`
**When** it reaches GitHub or git
**Then** it does so through one adapter that runs `gh` and one adapter of its own for git
**And** the tests replace both with fakes.

### Story 1.11: The gates run on a pull request that is ready for review

As a contributor,
I want the gates to run when my pull request is ready for review, and nowhere else,
So that a draft costs nothing and a merged change has been checked.

**Covers:** FR-54, FR-58; AD-17, AD-18. It settles two deferred items: the macOS interpreter, and Dependabot with the lock file.

**Acceptance Criteria:**

**Given** a pull request into `master` that is a draft
**When** it is opened or pushed to
**Then** every job of `gates.yml` is skipped.

**Given** a pull request into `master` that is ready for review
**When** it is opened, reopened, pushed to, or marked ready
**Then** the four suites run on Ubuntu and on macOS, each on Python 3.9 and on the current release
**And** the linter, the formatter, the type checker, and coverage run once, on Ubuntu and the current release
**And** the markdown lint, `claude plugin validate`, the secret scan, the scan of tracked files, and the workflow check run.

**Given** a run in progress for a pull request
**When** a newer push arrives
**Then** the older run is cancelled.

**Given** a push or a merge to `master`
**When** it lands
**Then** `gates.yml` does not run.

**Given** a job that runs on Python 3.9
**When** it starts
**Then** it first checks that its interpreter reports 3.9, and fails if it does not
**And** on macOS it uses the system interpreter, and `uv` is told not to download one.

**Given** the macOS runner's system interpreter is not 3.9
**When** this story finds that out
**Then** the job installs 3.9 on a macOS runner that has a build of it, and this repo's docs record the runner in use.

**Given** the final job of `gates.yml`
**When** a run is not a draft
**Then** it runs whatever the other jobs did, and gives the verdict from Story 1.10.

**Given** the Dependabot config
**When** an action or a locked tool has an update
**Then** Dependabot proposes it as a pull request with the `patch` label
**And** this repo's docs record whether Dependabot handles the lock file, and what is done by hand if it does not.

**Given** `gates.yml`
**When** it is read
**Then** it sets triggers, permissions, and steps that call a command, and holds no other logic
**And** every runner label is pinned, and every job installs the tools from the lock file.

**Given** this story's pull request has merged
**When** the owner updates the ruleset, or approves the session's command for it
**Then** the final job of `gates.yml` is a required check, and a branch must be up to date before it merges.

### Story 1.12: Release code works out the next version

As a maintainer,
I want tested code that turns merged pull requests and their labels into the next versions,
So that every merge gets exactly one release, in order, however the runs overlap.

**Covers:** FR-52, FR-59; AD-17, AD-20. It settles one deferred item: what the release notes hold.

**Acceptance Criteria:**

**Given** the tags in the repo
**When** the latest version is worked out
**Then** it is the highest tag of exactly the form `vMAJOR.MINOR.PATCH`, compared as numbers
**And** a tag of any other form is ignored.

**Given** the latest version and one of the labels `major`, `minor`, and `patch`
**When** the next version is worked out
**Then** the label raises its own part, and every part after it becomes zero
**And** with no version in the repo, the count starts from `v0.0.0`.

**Given** commits on `master` that are newer than the latest version
**When** a release run walks them
**Then** it takes them oldest first
**And** for each it finds the merged pull request, and reads the label that pull request carries at that moment
**And** a commit with no merged pull request gets no release of its own, and ships in the next one.

**Given** a pull request that carries none of the three labels, or more than one
**When** the run reaches it
**Then** the run stops and names the pull request.

**Given** a latest version below `v1.0.0`, and the label `major`
**When** the next version is worked out
**Then** the code refuses, unless a repository variable that the owner sets allows it.

**Given** a version to make
**When** the run makes it
**Then** one call creates the tag at that commit and the GitHub release with its notes
**And** a commit counts as released when a GitHub release exists for its tag
**And** a second run over the same commits makes nothing twice.

**Given** a repo with no version
**When** the first run happens
**Then** it releases only the newest commit.

**Given** the dry-run mode
**When** it runs for a pull request
**Then** it prints the version that pull request would get, or the refusal, and creates nothing.

**Given** the release notes
**When** a release is made
**Then** they hold the generated list of changes, and a place for what a user must do in a target repo on upgrade.

**Given** the release code
**When** it runs
**Then** it never pushes a commit
**And** the contract suite proves its git adapter against real git, in a throwaway repo.

### Story 1.13: A pull request needs one version label, and a merge releases

As a maintainer,
I want a check on each pull request's label and text, and a workflow that releases on merge,
So that every merged pull request becomes a numbered release with no step by hand.

**Covers:** FR-58, FR-59; AD-18, AD-20.

**Acceptance Criteria:**

**Given** a pull request into `master` that is ready for review
**When** it is opened, pushed to, labelled, unlabelled, or has its title or body edited
**Then** `pr.yml` runs
**And** it fails unless the pull request carries exactly one of `major`, `minor`, and `patch`
**And** it scans the title and the body for plan citations
**And** it runs the release code in dry-run mode and shows the version the pull request would get.

**Given** a run of `pr.yml` in progress
**When** a newer event arrives for the same pull request
**Then** the older run is cancelled, without touching a run of `gates.yml`.

**Given** a push to `master`
**When** it lands
**Then** `release.yml` runs, and no other workflow does
**And** its runs share one group, and a later run never cancels one in progress
**And** it is the only job in any workflow with a write permission.

**Given** either workflow
**When** the workflow check from Story 1.10 reads it
**Then** it passes.

**Given** this story's pull request has merged
**When** the owner updates the ruleset, or approves the session's command for it
**Then** the job of `pr.yml` is a required check.

### Story 1.14: The owner turns the rules on, and a drill proves them

As the owner of the repo,
I want the repository settings applied, the contributor guide written, and one pull request walked through every rule,
So that the gates and the release path are proven before the first line of plugin code.

**Covers:** FR-50, FR-51, FR-58, FR-59; AD-18. The drill is in `addendum.md` section 2.

**Acceptance Criteria:**

**Given** the repository settings from Stories 1.1, 1.11, and 1.13
**When** they are checked against the repo
**Then** a ruleset on `master` requires a pull request, the final job of `gates.yml`, the job of `pr.yml`, and a branch that is up to date
**And** it allows squash merges only, with the pull request's title and description as the commit message
**And** the three version labels exist, and private vulnerability reporting is on.

**Given** the credential for the plugin evals
**When** the owner stores it as a repository secret
**Then** only the owner has entered its value, and no session and no file has held it.

**Given** a design doc of this repo
**When** a maintainer reads it
**Then** it records each setting and the command that applies it
**And** it says that an agent runs such a command only after the owner approves it.

**Given** `CONTRIBUTING.md`
**When** a contributor reads it
**Then** it says how to set up, run each suite and each check, and propose a change
**And** it explains the gates and the version labels, and says that a maintainer sets the label
**And** it says how a change to this repo's own laws and ADRs is proposed: a round table hears it in the contributor's session, the pull request carries the ledger row, and a maintainer's merge decides whether it stands
**And** it says that a contribution is accepted under the MIT licence
**And** it points to this repo's laws and design docs, and restates none of them.

**Given** the repo on GitHub
**When** a person opens an issue or a pull request
**Then** there is a template for a bug, a template for a proposal, and a template for a pull request.

**Given** one pull request used as a drill
**When** it is walked through each rule
**Then** no gate runs while it is a draft, and the gates run when it is marked ready
**And** a second push cancels the run in progress
**And** the label check fails while it carries no version label
**And** its merge makes exactly one release
**And** the pull request records each of these results.

**Given** the README
**When** a person reads it after this story
**Then** it says where the latest release is, and links to the contributor guide.

## Epic 2: The words every repo starts with

The text that Avalon will write into every target repo is settled. This repo's round tables ratify the writing standard and the nine core laws, and the plugin holds a template for every governed document.

The round tables here are stand-in tables, held as in Stories 1.4 and 1.5. The user is the proposer of each core law, so a table that would reword one registers nothing until the user accepts (AD-19).

### Story 2.1: The writing standard is ratified

As the user,
I want the writing standard heard by a round table, together with the law that carries it,
So that every document written after it follows one agreed standard.

**Covers:** FR-4, FR-29, FR-30, FR-48; AD-19. The draft is `tmp/SPEC.md` section 8.

**Acceptance Criteria:**

**Given** the draft of the writing standard
**When** it goes to the table
**Then** it holds the prose rules: one subject to a document, one idea to a sentence, parallel items as a list, a comparison as a table, one point to a paragraph, an edit woven in and not appended, and a word that places something in time only in a changelog
**And** it holds the newcomer test: a reader who has never seen the repo can follow each document, and a term is defined once, in the glossary
**And** it holds the diagram rules: Mermaid, one of four types, a sentence before it that says what it shows, only the present, and a node cap
**And** it holds the image rules: design docs only, only what Mermaid cannot draw, alt text, no fact the text lacks, a size cap, and the allowed formats
**And** no rule in it assumes that the work is code.

**Given** the draft
**When** the table prepares to vote
**Then** a stand-in editor reviews the wording first, and returns its suggestions to the chair
**And** the seats vote on LAW-000009 and its detail file together.

**Given** the table's outcome differs from the user's draft
**When** the chair decides
**Then** nothing is registered until the user accepts, counters, or directs that it be registered as written.

**Given** the table and the user have decided
**When** the outcome is recorded
**Then** the ratified wording replaces the draft under the same ID, once
**And** the ledger gains one row, whose decision says that the law was ratified and names its ID
**And** from then on, a change to the law or to the standard is an amendment.

**Given** the ratified detail file
**When** it is compared with the rules for a detail file
**Then** it need not have the four-part body, and that exemption is stated where the rules for a detail file are stated.

### Story 2.2: The other eight core laws are ratified

As the user,
I want a round table to hear each of the other eight core laws,
So that the laws Avalon ships to every repo were tested by the process they establish.

**Covers:** FR-1, FR-3, FR-4, FR-35, FR-48; AD-19; SM-3. The drafts are `tmp/SPEC.md` section 11.

**Acceptance Criteria:**

**Given** LAW-000001 to LAW-000008 as drafts
**When** the table hears them
**Then** they are heard as a slate, with a separate vote and a separate ledger row for each
**And** the chair screens each one against the law test: it is stated as "must" or "never", a reviewer can say whether any piece of work complies, it applies to a class of work across the repo, it is expected to hold indefinitely, and it is worth its context cost.

**Given** a ratified law
**When** it is recorded
**Then** its wording replaces the draft under the same ID, once
**And** its ledger row says that the law was ratified and names its ID
**And** it is one sentence of at most 200 characters, with its scope from the scope list and origin `core`.

**Given** the table would reword or reject a core law
**When** the chair decides
**Then** nothing is registered until the user answers.

**Given** the nine core laws after this story
**When** the ledger is read
**Then** it shows a decision for each of the nine
**And** together the nine state the precedence of the three kinds, that a law changes only through a round table, that a conflict is reported and never resolved silently, that docs state only what is true and known, that a decision goes to a round table first, that a change updates the design doc it makes untrue, and that every doc follows the writing standard.

### Story 2.3: Templates for the laws folder

As a user who sets Avalon up in a repo,
I want the laws folder to start from fixed, ratified text,
So that every repo gets the same registry, archive, ledger, and core laws.

**Covers:** FR-6, FR-9, FR-10, FR-13, FR-46, FR-49, FR-53; AD-6, AD-16.

**Acceptance Criteria:**

**Given** `plugin/templates/`
**When** it is listed
**Then** it holds a template for the registry, the archive, the ledger, the law detail file, the core laws, and the writing standard.

**Given** the registry template
**When** it is read
**Then** it opens with the statement that every law in the table is binding and that the whole table is read before any work
**And** it says to open a detail file only when the one-line law is not enough to act on
**And** its table has the columns `ID`, `Scope`, `Origin`, `Law`, and `Detail`, in that order.

**Given** the archive template and the ledger template
**When** they are read
**Then** the archive's first line says that nothing in the file is in effect
**And** the archive has the columns `ID`, `Status`, `Text`, `Date`, `Replaced by`, `Now in effect`, and `Reason`
**And** the ledger has the columns `Date`, `Decision`, `Proposed by`, `Decided by`, `Rounds`, `Tally`, and `Dissent`.

**Given** the detail file template
**When** it is read
**Then** its frontmatter names the law, and the source ADR when there is one
**And** its body has the four parts Meaning, Applies to, Examples, and Enforcement.

**Given** the core laws template and the writing standard template
**When** they are compared with this repo's own laws folder
**Then** the text is the ratified text, word for word.

**Given** any template
**When** it is read
**Then** it is the only home of that format's fixed text, and it uses one placeholder form
**And** it has no field for a person's name, an email address, or an absolute path
**And** no wording in it assumes that the work is code.

**Given** the templates folder
**When** a person looks for the terms
**Then** a licence file there carries the MIT No Attribution licence, so that a target repo keeps the text with no notice.

### Story 2.4: Templates for ADRs and design docs

As a user who sets Avalon up in a repo,
I want every ADR and design doc to start from one fixed shape,
So that an agent and a person find the same parts in the same place in every repo.

**Covers:** FR-2, FR-23, FR-26, FR-27, FR-28, FR-46; AD-6.

**Acceptance Criteria:**

**Given** `plugin/templates/`
**When** it is listed
**Then** it also holds a template for the ADR, the design doc, the overview, the glossary, and each of the two indexes.

**Given** the ADR template
**When** it is read
**Then** its frontmatter holds `adr`, `summary`, `covers`, and `origin`
**And** its body holds Context, Decision, Consequences, Alternatives rejected, and Changelog, in that order, with the changelog last.

**Given** the design doc template
**When** it is read
**Then** its frontmatter holds `summary`, `covers`, `verified`, and `verified_commit`
**And** it has no changelog.

**Given** the overview template
**When** it is read
**Then** it names six sections: what the repo is, its purpose and audience, what it does or contains, its main parts and how they relate, a map of the repo, and how to work in it
**And** it says that a section that does not apply is left out, not left empty
**And** it links to the glossary and keeps no term list of its own.

**Given** the glossary template
**When** it is read
**Then** it is one table of `Term` and `Meaning`, in alphabetical order
**And** it starts with Avalon's own terms, such as law, ADR, round table, ledger, legacy, and the work.

**Given** this repo's own ADRs, overview, glossary, and indexes
**When** they are compared with the templates
**Then** each matches its template's shape.

### Story 2.5: The block template

As a working agent,
I want the same short block at the top of every target repo's instructions,
So that I load the laws and know what to read and what to do on a conflict, with or without the plugin.

**Covers:** FR-1, FR-5, FR-34, FR-35, FR-46; NFR-1; AD-6. The text is `tmp/SPEC.md` section 9.

**Acceptance Criteria:**

**Given** the block template
**When** it is read
**Then** it sits between the marker lines `<!-- avalon:start -->` and `<!-- avalon:end -->`
**And** it imports the registry with an `@` import
**And** it tells a tool that shows no table of laws to read the registry in full before anything else.

**Given** the block's text
**When** it is read
**Then** it states the precedence: laws, then ADRs, then the work, then design docs
**And** it says to read the overview before a first change, and the ADR for an area before changing that area
**And** it says where to look up an unknown term
**And** it says to stop and report, with the ID, on a contradiction or on a request to break a law or an ADR
**And** it says that laws change only through the `law` skill.

**Given** the block
**When** it is rendered for a repo
**Then** the only part that varies is the root path
**And** its size does not grow with the repo.

**Given** the variant for `AGENTS.md`
**When** it is read
**Then** it holds the same text, with an instruction to read the registry in full in place of the import.

**Given** this repo's own `CLAUDE.md`
**When** its block is compared with the template rendered for the root `docs`
**Then** the two are the same.

## Epic 3: One script sets up a repo and keeps its law record

A person can run one script to set Avalon's tree up in a repo. From then on, every session in that repo loads the laws.
The script registers, amends, removes, and confirms laws from recorded votes. It keeps the archive and the ledger, guards the record with a checksum, and lints the tree.

Each story adds only the commands, formats, and git reads it needs. The module names inside each layer, and the form of a matter ID, are settled in the stories that first need them.

### Story 3.1: One entry file and a closed command line

As a user,
I want one script with one way in, which says plainly when my Python is too old,
So that I never guess how to run it or why it failed.

**Covers:** FR-42, FR-54; NFR-3; AD-3, AD-9, AD-13.

**Acceptance Criteria:**

**Given** a Python below 3.9
**When** any command but `hook` runs
**Then** the script prints one message that names the version needed, changes no file, and exits 2.

**Given** a Python below 3.9
**When** the `hook` command runs
**Then** the script prints nothing and exits 0.

**Given** `plugin/script/avalon`
**When** it is read
**Then** it holds no logic of its own: it checks the Python version in syntax every Python 3 can parse, puts its own folder on the import path, turns off bytecode files, and hands over to the `avalonlib` package
**And** `avalonlib` holds the packages `cli`, `commands`, `rules`, `formats`, `model`, `ports`, and `adapters`.

**Given** a command word that is not in the command table, or a wrong argument
**When** the script runs
**Then** it exits 2
**And** the error goes to standard error, says what was refused and why, and names the next command to run.

**Given** the argument parser
**When** it is given a shortened flag or an argument file
**Then** it refuses both
**And** it accepts `--as-user` only straight after the entry file and before the command word
**And** it refuses `--as-user` on a command that does not need it.

**Given** any command that succeeds
**When** it prints its result
**Then** the output is lines of `key: value`, then a block headed `changed:` with one path on each line, marked `+`, `~`, or `-`
**And** each path is relative to the top of the repo, and no path under `.avalon/` is listed
**And** the command does not prompt, page, or colour its output.

**Given** the linter, the type checker, and coverage
**When** they run
**Then** each includes the entry file by name.

### Story 3.2: Gates keep the script free of dependencies and its layers apart

As a maintainer,
I want a gate that fails when the script imports what it must not,
So that the shipped script needs nothing but Python, and its core stays testable without a file system.

**Covers:** FR-58; NFR-3, NFR-5; AD-3, AD-4, AD-17.

**Acceptance Criteria:**

**Given** a module under `plugin/script/`
**When** it imports anything but the standard library and `avalonlib` itself
**Then** the import gate fails, and names the module and the import.

**Given** a module under `plugin/script/`
**When** it imports `socket`, `ssl`, `http`, `urllib`, `ftplib`, `smtplib`, or `asyncio`
**Then** the gate fails.

**Given** the layers of the script
**When** a module imports a layer that its own layer may not reach
**Then** the gate fails
**And** the allowed reaches are: `cli` to `commands`, `adapters`, and `ports`; `commands` to `rules`, `formats`, `ports`, and `model`; `rules`, `formats`, and `ports` to `model`; `adapters` to `ports` and `model`.

**Given** `gates.yml`
**When** a pull request is ready for review
**Then** the import gate runs as one of its jobs
**And** the gate's logic is tested Python under `devtools/gates/`.

### Story 3.3: Files, the clock, and git sit behind ports

As a maintainer,
I want every touch of the file system, the clock, and git to go through one small interface each,
So that the script's logic is tested with fakes, and the script can never write to git.

**Covers:** FR-43, FR-55; AD-4, AD-11, AD-15; AC-20.

**Acceptance Criteria:**

**Given** the `ports` package
**When** it is read
**Then** it holds one interface for files, one for git, and one for the clock
**And** only the files adapter touches the file system, and only the git adapter starts a process.

**Given** the git adapter
**When** it is asked a question
**Then** it runs one of a fixed list of read-only git commands, with optional locks off
**And** in this story it answers: the top of the repo, the current commit, whether the repo has any commit, and the tracked files.

**Given** the clock port
**When** it is asked for a date or a time
**Then** it gives the local date as `YYYY-MM-DD`, and the time in UTC as ISO 8601 with a `Z`.

**Given** `tests/fakes/`
**When** a unit test needs a port
**Then** a fake for each port is there.

**Given** the contract suite
**When** it runs
**Then** it runs the git fake and the real git adapter through the same cases, in a throwaway repo, with no network
**And** after every call it checks that the index, `HEAD`, and every ref are unchanged
**And** it is the only test code that runs the real git adapter.

### Story 3.4: The script finds the config file, the root, and the tree's version

As a user,
I want the script to find my repo's Avalon settings from any folder inside the repo,
So that every command works on the same tree, and an old or a new tree is never misread.

**Covers:** FR-33, FR-61; NFR-4; AD-6, AD-12.

**Acceptance Criteria:**

**Given** a working directory inside a target repo
**When** the script resolves the repo
**Then** the top of the repo is the nearest folder, walking up, that holds `.avalon.yml`
**And** the root comes from that file
**And** the script reads no environment variable and no plugin option to find either.

**Given** the config file or any frontmatter
**When** it is parsed
**Then** one parser reads flat keys, scalar values, and inline lists
**And** a file outside that subset is refused, and the error names the line.

**Given** a root in the config file
**When** it is checked
**Then** it must be a relative path inside the top of the repo, with no `..` in it, and outside `.git/`, `.github/`, and `.claude/`.

**Given** a config file that holds git conflict markers
**When** it is read
**Then** one splitter in `formats` separates the two sides
**And** the script reports the file as conflicted and does not treat it as an ordinary parse error.

**Given** a tree whose `system_version` is lower than the script's
**When** the command line checks the tree, before it hands over to any command but `hook`
**Then** it refuses, parses nothing more, and says that the tree needs to be migrated.

**Given** a tree whose `system_version` is higher than the script's
**When** the command line checks the tree, before it hands over to any command but `hook`
**Then** it refuses and tells the user to update the plugin.

**Given** the docs format
**When** its version is looked up
**Then** it is one integer, held as a constant in `formats`, and the first version is 1.

### Story 3.5: A command writes all of its changes, or none

As a user,
I want a script command to finish every write or leave the repo as it was,
So that a refusal, a crash, or two commands at once never leaves a half-written record.

**Covers:** FR-12, FR-33, FR-44; AD-5, AD-7, AD-9. `config set` is the first writing command, and it proves the mechanism.

**Acceptance Criteria:**

**Given** `config set` with `--as-user`, a cap or the scope list, and a value
**When** it runs
**Then** it changes that value and keeps every other line of the config file as it found it
**And** it prints the changed path.

**Given** `config set` without `--as-user`, or for a key the script owns, or for an unknown key
**When** it runs
**Then** it refuses, exits 2, and changes no file.

**Given** a tree in an older or a newer format than the script's
**When** `config set` runs
**Then** it refuses, and changes no file.

**Given** any writing command
**When** it runs
**Then** it builds its whole change set in memory, checks it, and only then applies it
**And** it holds an exclusive lock on `.avalon/lock` from its first read to its last write
**And** it creates `.avalon/` and the ignore file inside it when they are missing.

**Given** a change set that is about to be applied
**When** the command applies it
**Then** it first saves it to `.avalon/journal`, replaces each file atomically, and removes the journal after the last write
**And** files under the laws folder go first, and the config file goes last.

**Given** a journal left by a command that stopped part-way
**When** the next writing command starts
**Then** it checks every path in the journal against the path rules, and then applies the journal first, under the lock.

**Given** a change set with a target outside the root's tree, `.avalon.yml`, `.avalon/`, and the block
**When** the command checks it, after resolving symbolic links
**Then** it refuses, and changes no file.

**Given** the caps
**When** the config file sets none
**Then** the defaults apply: 100 laws, 200 characters for a law, 400 lines for a document, 15 nodes for a diagram, 500 KB for an image, 40 words for a flagged sentence, and 5 tables a day that agents convene.

### Story 3.6: The law record's formats and its checksum have one home

As a user,
I want the registry, the archive, the ledger, and the checksum each defined in one place,
So that every command and the lint agree on what a valid law record is.

**Covers:** FR-6, FR-9, FR-10, FR-13, FR-14, FR-44, FR-53; AD-4, AD-6.

**Acceptance Criteria:**

**Given** the registry, the archive, the ledger, and a law detail file
**When** `formats` parses or renders one
**Then** it does no input or output
**And** it copies the fixed text from the template and holds none of its own.

**Given** each of those formats rendered with no rows
**When** it is compared with its template
**Then** the two are the same.

**Given** a tally
**When** it is rendered
**Then** it is labelled counts in the order approve, amend, reject, with every count written, including a zero
**And** a row with no vote holds `none`.

**Given** the checksum
**When** it is computed
**Then** it is SHA-256 over every regular file under the laws folder whose name does not start with a dot, in byte order of its path relative to the laws folder
**And** each file adds its path, a NUL, its bytes with every CRLF made LF, and a NUL
**And** the `installed_at` and `install_commit` values follow, as stored, each followed by a NUL
**And** the result is 64 lower-case hex digits
**And** a unit test holds a fixed example and its digest.

**Given** a sample of every format, kept with the tests
**When** a sample changes and the version constant does not
**Then** a test fails.

**Given** any format
**When** its fields are listed
**Then** none holds a person's name, an email address, or an absolute path.

### Story 3.7: `scaffold` sets Avalon's tree up in a repo

As a user,
I want one command that creates the tree, the config file, the core laws, and the block,
So that every later session in my repo loads the laws.

**Covers:** FR-5, FR-32, FR-33, FR-34; NFR-1, NFR-4; AD-5, AD-10, AD-12; AC-01, AC-02.

**Acceptance Criteria:**

**Given** a repo with at least one commit and no docs
**When** `scaffold` runs
**Then** the tree exists under the root, with the registry, the archive, the ledger, the two indexes, the overview, the glossary, and the writing standard
**And** the registry holds the nine core laws, copied from the template, with origin `core`
**And** `.avalon.yml` holds the root, the profile, the system version, the install time, the install commit, the default caps, the default scope list, and the checksum
**And** `CLAUDE.md` holds the block between its marker lines
**And** the command prints every path it created.

**Given** a `CLAUDE.md` that already holds other content
**When** `scaffold` runs
**Then** only the text between the marker lines is written, and everything outside them is unchanged.

**Given** a repo that `scaffold` has already set up
**When** it runs a second time
**Then** the install time and the install commit are unchanged
**And** it changes only the block and what is missing.

**Given** a folder that is not a git repo, or a repo with no commit
**When** `scaffold` runs
**Then** it refuses, changes nothing, and says that a first commit is needed.

**Given** a root folder that holds content `scaffold` did not create
**When** `scaffold` runs
**Then** it refuses, writes nothing into that folder, and names another root.

**Given** a root passed as an argument
**When** `scaffold` runs with no config file present
**Then** it uses that root, and `docs/` when no root is passed.

**Given** the option to write the block into `AGENTS.md`
**When** `scaffold` runs with it
**Then** `AGENTS.md` holds the block, with an instruction to read the registry in full in place of the import.

**Given** any run of `scaffold`
**When** it ends
**Then** the git index, `HEAD`, and every ref are as they were.

### Story 3.8: `lint` checks the law record

As a user,
I want one command that fails when the law record is malformed or was changed outside the script,
So that I, a clone, and a CI job can all trust what the registry says.

**Covers:** FR-6, FR-7, FR-14, FR-44, FR-45, FR-61; AD-5, AD-6, AD-13; AC-01, AC-11, AC-12, AC-13, AC-45.

**Acceptance Criteria:**

**Given** a repo straight after `scaffold`
**When** `lint` runs
**Then** it passes and exits 0.

**Given** a registry or an archive that does not match its table format, a law ID that is repeated or is not `LAW-` and six digits, a law longer than the length cap, or a scope that is not in the scope list
**When** `lint` runs
**Then** it fails on each, names the file and the line, and exits 1.

**Given** an archived row in a chain that does not name the end of its chain as the law in effect
**When** `lint` runs
**Then** it fails on that row.

**Given** a ledger row whose tally is a bare pair such as `4-1`
**When** `lint` runs
**Then** it fails on that row
**And** a confirmation row, which holds `none`, raises nothing.

**Given** a file under the laws folder that was edited without the script, or an install time or install commit that was changed
**When** `lint` runs
**Then** it fails on the checksum.

**Given** a ledger and an archive that are each longer than the document size cap
**When** `lint` runs
**Then** it passes.

**Given** a config file or frontmatter outside the parsed subset
**When** `lint` runs
**Then** it fails and names the line.

**Given** a journal left in `.avalon/`
**When** `lint` runs
**Then** it reports the journal and does not apply it.

**Given** a tree in an older format
**When** `lint` runs
**Then** it parses nothing, says the tree needs to be migrated, and exits 1.

**Given** a finding that only flags
**When** `lint` reports it
**Then** the exit code does not change.

### Story 3.9: A matter has one folder and one record

As a chair,
I want the script to open, hold, and close the working folder of a matter,
So that the proposal, the votes, and the state of a round table are always in one known place.

**Covers:** FR-21, FR-33; NFR-2; AD-4, AD-9, AD-10. It settles the form of a matter ID.

**Acceptance Criteria:**

**Given** a kind (law or decision), who proposed, who convened, and a target when there is one
**When** `matter open` runs
**Then** it creates `.avalon/matters/<id>/` with a record that holds those values and the state `open`
**And** it prints the matter ID and the absolute path of each file the chair may write
**And** the ID is the highest one in use plus one, allocated under the lock, with no randomness.

**Given** a table that an agent convenes
**When** `matter open` runs
**Then** it appends one line to `.avalon/tables.log`
**And** when the count for the local calendar day has reached the daily cap, it refuses unless the command carries `--as-user`.

**Given** a table that the user convenes
**When** `matter open` runs
**Then** it adds nothing to the count.

**Given** an open matter
**When** `matter wait` runs
**Then** the state is `waiting`.

**Given** a matter that is finished or abandoned
**When** `matter close` runs
**Then** its folder no longer exists.

**Given** any of the three commands
**When** it runs
**Then** it writes only under `.avalon/`, and no governed document refers to a path there.

### Story 3.10: `packet`, `vote`, and `tally` record a round

As a chair,
I want the script to build each seat's packet, record a round of votes, and count it,
So that no vote is retyped by hand and no table runs a fourth round.

**Covers:** FR-14, FR-18; NFR-2; AD-10.

**Acceptance Criteria:**

**Given** an open matter with a proposal
**When** `packet` runs for round 1
**Then** it writes one packet file that holds the proposal, any draft detail file, the registry, and each ADR the chair names as related.

**Given** a recorded round that was not unanimous, and a revision
**When** `packet` runs for the next round
**Then** the packet holds the latest revision, and every earlier vote with its reason.

**Given** the previous round's votes are not recorded
**When** `packet` runs for a later round
**Then** it refuses.

**Given** the chair's input file for a round
**When** `vote` runs
**Then** it records the round only when the file holds five votes, one from each seat that sits on that kind of matter, each with a reason
**And** each vote is approve, amend with proposed wording, or reject
**And** the script numbers the round.

**Given** an input file with four votes, a seat that does not sit on that kind of matter, or a missing reason
**When** `vote` runs
**Then** it refuses and records nothing.

**Given** a matter with three recorded rounds
**When** `vote` runs again
**Then** it refuses.

**Given** a recorded round
**When** `tally` runs
**Then** it prints the counts in the one tally format
**And** it says the round is unanimous only when all five approve or all five reject.

### Story 3.11: `law add` and `law reject` register a round table's outcome

As a user,
I want a law to enter the registry only when a round table or I have decided,
So that the registry never holds a rule that nobody heard.

**Covers:** FR-6, FR-7, FR-8, FR-9, FR-12, FR-13, FR-20, FR-44; AD-5, AD-9, AD-10; AC-03, AC-04, AC-10.

**Acceptance Criteria:**

**Given** a law matter whose last round holds five recorded votes, and an outcome the table may register
**When** `law add` runs with the matter ID
**Then** the law is the last registry row, with the next ID in the sequence and the proposer's origin
**And** the text comes from the latest revision in the matter folder, and never from an argument
**And** the ledger has one more row, decided by `table`, with the rounds, the tally, and each seat that voted against the decision, with its reason
**And** the checksum is recorded, the matter folder is removed, and `lint` passes.

**Given** a matter with four recorded votes and no override
**When** `law add` runs
**Then** it refuses, and no file changes.

**Given** a matter that holds a draft detail file the seats voted on
**When** `law add` runs
**Then** the detail file is written under the laws folder, named for the new ID, and the `Detail` column links to it.

**Given** `--as-user` and `--override`
**When** `law add` runs
**Then** the law is registered as the proposer wrote it, with origin `user`
**And** the ledger row shows `user override`, and names each seat that voted against.

**Given** a matter whose record shows that the table reworded the user's proposal
**When** `law add` runs without `--as-user` and `--accept`
**Then** it refuses
**And** with both, it registers the table's wording, and the ledger row shows `table`.

**Given** a matter whose last round holds five reject votes
**When** a registering command runs
**Then** only `law reject` succeeds
**And** `law reject` adds one ledger row and leaves the registry unchanged.

**Given** a registry at its cap
**When** `law add` registers one more law
**Then** it registers the law, and its output states the count against the cap.

**Given** the next ID
**When** it is allocated
**Then** the sequence counts every archived law, and no ID is ever reused.

### Story 3.12: `law amend` and `law remove` retire a law into the archive

As a user,
I want an amended or removed law to leave the registry and keep its history in the archive,
So that the registry holds only what binds, and nothing lost its record.

**Covers:** FR-10, FR-11, FR-13, FR-21, FR-29, FR-44; AD-9, AD-10; AC-05, AC-06, AC-07, AC-09.

**Acceptance Criteria:**

**Given** an adopted amendment to a law
**When** `law amend` runs
**Then** the amending law is the last registry row, with a new ID
**And** the amended row moves to the archive with the status `Amended`, its text, the date, and the reason
**And** `Replaced by` names the amending law
**And** the ledger has one more row.

**Given** a law that was amended, and whose amending law is amended again
**When** the second `law amend` runs
**Then** both archived rows name the latest law as the law in effect
**And** `Replaced by` on the first row still names the law that first amended it.

**Given** an adopted removal
**When** `law remove` runs
**Then** the row moves to the archive with the status `Removed` and its reason
**And** every row in its chain shows `none` as the law in effect
**And** no earlier law returns to the registry.

**Given** a law that has a detail file
**When** it is amended or removed
**Then** the detail file of the retired ID no longer exists.

**Given** the law that carries the writing standard
**When** it is amended
**Then** its detail file is carried to the new ID and is not deleted.

**Given** a law that three tracked files cite
**When** `law amend` or `law remove` runs on it
**Then** the command prints all three citations.

**Given** a table that an agent convened, and a law of origin `user` or `core`
**When** `law amend` or `law remove` runs without `--as-user` and `--accept`
**Then** it refuses, and no file changes.

### Story 3.13: No file cites a retired law

As a user,
I want the lint to fail on a citation of a retired law, and a way to fix one inside a file only the script may write,
So that no reader meets a rule that no longer exists.

**Covers:** FR-11, FR-45; AD-7, AD-13; AC-08.

**Acceptance Criteria:**

**Given** a tracked text file outside the archive and the ledger that cites an amended law by its ID
**When** `lint` runs
**Then** it fails, and names the file, the line, and the law in effect.

**Given** a tracked text file that cites a removed law
**When** `lint` runs
**Then** it fails, names the file and the line, and says that no law is in effect.

**Given** the same ID in the archive and in the ledger
**When** `lint` runs
**Then** it raises nothing for them.

**Given** a citation of a retired ID inside a file under the laws folder
**When** `cite fix` runs with the file, the retired ID, and either a replacement ID or a removal
**Then** the script writes the change, records the checksum, and prints the changed path.

**Given** a citation inside a file that an agent may edit
**When** `cite fix` runs on it
**Then** it refuses, and says that an agent fixes that file.

### Story 3.14: The user confirms an agent's law

As a user,
I want to turn a law that agents adopted into my own with one command,
So that I stand behind it without calling another round table.

**Covers:** FR-8, FR-13, FR-20; AD-9, AD-10; AC-40.

**Acceptance Criteria:**

**Given** a law of origin `agent`
**When** `law confirm` runs with `--as-user`
**Then** the registry row has origin `user` and the same text
**And** the ledger has one more row, decided by `user`, with `none` for the rounds, the tally, and the dissent
**And** `Proposed by` on that row keeps the original proposer
**And** `lint` passes.

**Given** `law confirm` without `--as-user`
**When** it runs
**Then** it refuses, and no file changes.

**Given** a law whose origin is not `agent`
**When** `law confirm` runs
**Then** it refuses.

### Story 3.15: Frontmatter, the two indexes, and the lint for documents

As a working agent,
I want an index of every ADR and design doc, generated from the documents themselves,
So that I find the document for an area without reading them all.

**Covers:** FR-27, FR-28, FR-45; AD-6; AC-16, AC-17, AC-45.

**Acceptance Criteria:**

**Given** a document added to the ADR folder or the design folder
**When** `index` runs
**Then** the index of that folder lists the document on one line, with its `summary`.

**Given** an index that is missing a document, or that lists one that does not exist
**When** `lint` runs
**Then** it fails.

**Given** a link in a governed document that points to nothing
**When** `lint` runs
**Then** it fails, and names the file and the line.

**Given** a document with six `covers` entries, or with an entry that matches no path
**When** `lint` runs
**Then** it fails.

**Given** a `covers` entry
**When** the one matcher reads it
**Then** `*` matches inside one path segment, `**` matches any number of whole segments, and an entry with neither is an exact path
**And** the matcher works on a list of paths, and git is never given a pattern.

**Given** an ADR, a design doc other than the glossary, or a law detail file that is longer than the document size cap
**When** `lint` runs
**Then** it fails
**And** it checks no other file against that cap.

**Given** a glossary with two terms in one row, a repeated term, or terms out of alphabetical order
**When** `lint` runs
**Then** it fails.

### Story 3.16: The lint checks what the writing standard can measure

As a writer of documents,
I want the lint to catch a malformed diagram or image, and to flag a time word or a very long sentence,
So that the parts of the writing standard a machine can check are never left to chance.

**Covers:** FR-29, FR-30, FR-45; AC-42.

**Acceptance Criteria:**

**Given** a design doc that holds a word that places something in time, such as "previously", outside a changelog
**When** `lint` runs
**Then** it flags the line and does not fail.

**Given** the registry, the archive, and the ledger
**When** `lint` runs
**Then** it does not scan them for time words.

**Given** a sentence longer than the flag length
**When** `lint` runs
**Then** it flags the sentence and does not fail.

**Given** a diagram that is not a flowchart, sequence, state, or entity-relationship diagram, that has no sentence before it, or that has more nodes than the cap
**When** `lint` runs
**Then** it fails.

**Given** an image that is missing, that no document refers to, that has no alt text, that is larger than the size cap, or that is not PNG, JPEG, SVG, or WebP
**When** `lint` runs
**Then** it fails.

**Given** any paragraph
**When** `lint` runs
**Then** it does not measure it.

### Story 3.17: This repo's own tree passes the lint and gets its first checksum

As the user,
I want the script to check the tree that was written by hand, and to seal it once with my approval,
So that from here on, nothing under this repo's laws folder is written by hand.

**Covers:** FR-48, FR-58; AD-18, AD-19. It settles one deferred item: how the hand-written tree gets its first checksum.

**Acceptance Criteria:**

**Given** this repo's hand-written tree
**When** `lint` runs on it
**Then** every finding other than the missing checksum is fixed before the tree is sealed.

**Given** a tree with no other finding
**When** the user approves
**Then** the checksum is recorded once, through the script's own checksum code
**And** no shipped command does it, and no tracked code is left behind for it.

**Given** the sealed tree
**When** `lint` runs
**Then** it passes.

**Given** `gates.yml`
**When** a pull request is ready for review
**Then** one job runs the Avalon lint on this repo's own docs.

**Given** a law change in this repo after this story
**When** a stand-in chair records it
**Then** it runs the script's commands, and writes no file under the laws folder by hand.

## Epic 4: Laws change through a round table, and the user has the final say

The user, or a working agent, proposes a law with `/avalon:law`. A chair and five seats hear it, and the script registers the outcome.
The hook guards the record, lets a round table run without a prompt at every step, and puts every claim of the user's authority in front of the user.

The model and the effort of each agent start from the values in `tmp/SPEC.md` section 14, and are tuned on the evals in this epic.

### Story 4.1: The hook denies a direct write to the record

As a user,
I want every direct edit of the laws folder, the config file, and the script's working files to be denied,
So that an agent's shortcut or accident cannot change the record.

**Covers:** FR-20, FR-44; NFR-4; AD-7, AD-8. It settles one deferred item: the rules for spotting a write inside a Bash command.

**Acceptance Criteria:**

**Given** `plugin/hooks/hooks.json`
**When** it is read
**Then** it holds one `PreToolUse` entry for the Bash, Write, Edit, MultiEdit, and NotebookEdit tools
**And** the entry runs `python3` with the entry file and `hook` as arguments, with no shell, and with a timeout of 10 seconds.

**Given** a Write or an Edit whose target is under the laws folder, is `.avalon.yml`, or is a path under `.avalon/` that the chair does not own
**When** the hook runs
**Then** it answers `deny`, and the reason names the skill or the command to use.

**Given** a Write to a matter's proposal, a revision, the draft detail file, or a round's vote input
**When** the hook runs
**Then** it does not deny it.

**Given** a Write or an Edit
**When** the hook looks for the config file
**Then** it looks from the nearest existing folder above the target, and from the call's working directory, and applies both.

**Given** a target reached through a symbolic link, or written in another case on a volume that ignores case
**When** the hook compares paths
**Then** it still finds that the target is protected.

**Given** a repo with no config file
**When** the hook runs
**Then** it guards nothing and answers nothing.

**Given** a config file that cannot be parsed
**When** the hook runs
**Then** it protects the laws folder under every root the file names, and under `docs/`.

**Given** a Bash command that writes to a protected path
**When** the hook runs
**Then** it denies the command where its rules can spot the write
**And** it never denies a command that only reads.

**Given** any call
**When** the hook ends
**Then** it exits 0, and its answer is in the JSON it prints
**And** it has read no git and taken no lock.

**Given** the hook fails after a call matched a protected path
**When** it ends
**Then** it answers `deny`
**And** on any other failure it lets the call through.

### Story 4.2: The hook approves the plugin's own everyday commands

As a user,
I want a round table to run its script steps without stopping for me at each one,
So that I am asked only when my authority is claimed.

**Covers:** FR-44; AD-8, AD-13.

**Acceptance Criteria:**

**Given** a Bash command
**When** the hook checks it for approval
**Then** it answers `allow` only when all six of these hold: the command is one line with no unquoted shell operator, substitution, redirect, or variable; its first word is exactly `python3`; its second word equals the entry file's path under the hook's own plugin root; its third word starts a command in the law, table, ADR, docs, or read groups; no word starts with `--as`; and a config file is found above the call's working directory.

**Given** a command that fails any one of the six
**When** the hook runs
**Then** it answers nothing for approval, and the call takes the normal permission flow.

**Given** `scaffold`, `move-root`, `migrate`, `merge`, `config set`, either confirm command, or `hook`
**When** the hook checks the command
**Then** it never answers `allow`.

**Given** a third word that names no command the script has
**When** the hook checks the command
**Then** it does not answer `allow`.

**Given** a copy of the script at any other path
**When** a command runs that copy
**Then** the hook does not approve it.

**Given** the hook fails inside the approval check
**When** it ends
**Then** it answers nothing.

### Story 4.3: A claim of the user's authority becomes a prompt, or is denied

As a user,
I want every command that claims my confirmation, my override, or my acceptance to reach me as a prompt,
So that nothing is registered in my name unless I saw the exact command.

**Covers:** FR-20, FR-44; AD-9, AD-14.

**Acceptance Criteria:**

**Given** a Bash command that names a file called `avalon` and holds a word that starts with `--as`, anywhere in it
**When** the hook runs
**Then** it treats the command as flagged.

**Given** a flagged command in the default permission mode or the auto mode
**When** the hook runs
**Then** it answers `ask`, and the prompt shows the command.

**Given** a flagged command in any other permission mode, in a mode the hook does not know, or in any subagent
**When** the hook runs
**Then** it answers `deny`, and the reason tells the user to switch to the default mode.

**Given** a command that names such a file and cannot be split into words
**When** the hook runs
**Then** it answers `deny`.

**Given** the permission modes
**When** the hook's code is read
**Then** one table holds the answer for each mode.

**Given** every skill file and agent file in the plugin
**When** a static check reads them
**Then** none pre-approves a tool
**And** no skill file sets a `name` key, so that no skill has a bare command.

### Story 4.4: Plugin evals prove the guards inside Claude Code

As a maintainer,
I want scored cases that run the real plugin in a real session,
So that the behaviours the Claude Code docs leave unstated are proven and not assumed.

**Covers:** FR-5, FR-20, FR-34, FR-44, FR-46, FR-54, FR-55, FR-58; AD-8, AD-9, AD-12, AD-15, AD-18; AC-21, AC-22, AC-23. It settles the step 4 proofs and the lowest supported Claude Code version.

**Acceptance Criteria:**

**Given** `evals/` and `fixtures/code-repo`
**When** an eval case runs
**Then** it copies the fixture to a temporary folder outside this repo, gives the copy a git repo, and never uses the fixture in place
**And** the fixture holds invented content only.

**Given** a session or a subagent in a target repo
**When** it calls Write or Edit on the registry, the archive, or the ledger
**Then** the hook denies the call.

**Given** a session without the plugin, and a subagent with it
**When** each starts in a target repo
**Then** the registry is in its context.

**Given** a subagent that runs an everyday script command, written with the plugin root placeholder
**When** the command reaches Bash
**Then** the placeholder is filled in, and the command runs with no prompt.

**Given** a flagged command in each permission mode
**When** the case runs
**Then** the result shows whether that mode prompts
**And** a row of the hook's mode table is `ask` only when a case shows that the mode prompts, and `deny` otherwise.

**Given** a scored case
**When** it is run
**Then** it runs three times, and passes when two runs pass.

**Given** a pull request that changes a skill, an agent file, the hook, or a template
**When** it is ready for review
**Then** the plugin evals run as a job of `gates.yml`, with a cost limit, and with the credential from the repository secret
**And** on any other pull request the job is skipped, and the final job still passes.

**Given** a pull request from a fork that needs the evals
**When** the gates run
**Then** the final job fails until a maintainer moves the change to a branch of this repo.

**Given** the cases in this story
**When** they are run on earlier Claude Code versions
**Then** the lowest version on which they pass is recorded in this repo's docs.

### Story 4.5: Six seats, each with one fixed perspective

As a user,
I want each seat at the round table to argue from one fixed point of view,
So that a proposal is tested from five different sides.

**Covers:** FR-17, FR-41; NFR-4; AD-14.

**Acceptance Criteria:**

**Given** `plugin/agents/`
**When** it is listed
**Then** it holds `seat-practitioner`, `seat-skeptic`, `seat-jurist`, `seat-steward`, `seat-enforcer`, and `seat-scout`, flat in that folder.

**Given** a seat file
**When** it is read
**Then** it holds its perspective and its questions, and nothing else
**And** it holds no voting rule and no vote format
**And** a seat that sits on both kinds of matter holds its questions for each.

**Given** the six perspectives
**When** the files are read
**Then** the Practitioner asks whether an agent can follow this in daily work, and what it costs
**And** the Skeptic asks whether this is needed at all, and on a decision argues for the strongest alternative, including doing nothing
**And** the Jurist asks whether it conflicts with, duplicates, or leaves a loophole in a law or an ADR
**And** the Steward asks what this locks in and who pays a year later, through the lens of the repo's domain
**And** the Enforcer asks whether a violation can be detected
**And** the Scout asks whether the real alternatives were considered.

**Given** a seat file's tools
**When** they are listed
**Then** they are Read, Grep, and Glob only.

**Given** every agent file in the plugin
**When** a static check reads it
**Then** it sets its own model, effort, and tools
**And** it names neither Fable nor Haiku as its model.

### Story 4.6: The prose editor reads as a newcomer

As a user,
I want an editor that reads each text as someone who has never seen my repo,
So that a law's wording is clear before the seats vote, and a document is clear before it is kept.

**Covers:** FR-18, FR-29, FR-40, FR-41; AD-7, AD-14.

**Acceptance Criteria:**

**Given** a document to review
**When** the `prose-editor` is called
**Then** it is given the document, and not the conversation behind it.

**Given** the wording of a proposed law, or a draft detail file
**When** the `prose-editor` reviews it
**Then** it returns suggestions to the chair, and edits no file under the laws folder.

**Given** an ADR or a design doc
**When** the `prose-editor` edits it
**Then** it fixes the prose with the Edit tool, and lists what it changed
**And** it changes wording and never meaning
**And** where a fix would change what a sentence says, it reports the passage instead.

**Given** the writing standard
**When** the `prose-editor` needs it
**Then** it reads it from the target repo's laws folder, and its own file holds no copy.

**Given** a term specific to the repo that the glossary does not define, or a term a document defines for itself
**When** the `prose-editor` meets it
**Then** it flags the term.

**Given** the agent file
**When** its tools are listed
**Then** they are Read, Grep, Glob, and Edit
**And** the agent returns its outcome and the paths it changed, and never commits.

### Story 4.7: The chair runs a law matter from screening to registration

As a user,
I want an impartial chair to run each round table in its own context,
So that the proposer never judges its own proposal, and my session receives only the outcome.

**Covers:** FR-3, FR-9, FR-12, FR-15, FR-16, FR-18, FR-19, FR-22; NFR-2; AD-2, AD-10, AD-13, AD-14; AC-25, AC-27, AC-30.

**Acceptance Criteria:**

**Given** the chair's file
**When** it is read
**Then** it is the only home of the round-table procedure, the voting rules, and what a seat returns
**And** its tools are Read, Grep, Glob, Write, Bash, Agent, and SendMessage.

**Given** a proposed law
**When** the chair screens it, before it opens a matter
**Then** it applies the five parts of the law test
**And** it turns away a repeat of a rejected proposal that brings no new argument.

**Given** a proposal that passes screening
**When** the chair prepares round 1
**Then** it opens a matter, writes the proposal, and drafts a detail file when one sentence cannot carry the law
**And** it has the `prose-editor` review the wording before the seats see it.

**Given** round 1 of a law matter
**When** the chair seats the table
**Then** it spawns five seats in parallel by their full names, with the Enforcer as the fifth
**And** each seat reads only its packet, and no seat sees another's vote.

**Given** a round that is not unanimous
**When** the chair continues
**Then** it writes its revision as a new file, has the `prose-editor` review that wording, and records the round through the script
**And** it sends the same five seat agents a message that asks whether the revision resolves their objection
**And** it never runs a fourth round.

**Given** a seat that cannot be resumed
**When** the chair continues
**Then** it starts another seat of the same kind, and the packet gives that seat the earlier votes and reasons.

**Given** a unanimous round, or the end of round 3
**When** the chair decides
**Then** it adopts, adopts with final edits, or rejects, by the weight of the arguments and not the count of votes
**And** it registers the outcome through the script, a rejection included.

**Given** an adoption that would take the registry over its cap
**When** the table decides
**Then** it names laws to merge or remove, or states why none can go.

**Given** a step of the round table fails
**When** the chair notices
**Then** it stops, registers nothing, and reports the failure
**And** it never decides on an incomplete round, and never seats a smaller table.

**Given** a table that has finished
**When** the chair returns
**Then** it returns the outcome, the matter ID, and the paths that changed, and it has made no commit.

### Story 4.8: The `law` skill takes a proposal to the round table

As a user,
I want one skill that frames a law proposal, hands it to the chair, and reports what happened,
So that I can create, amend, remove, or confirm a law from my session.

**Covers:** FR-8, FR-11, FR-15, FR-19, FR-21, FR-22, FR-36, FR-54; AD-2, AD-3, AD-12, AD-13.

**Acceptance Criteria:**

**Given** the plugin
**When** the user types `/avalon:law`
**Then** the skill runs, and it has no bare command.

**Given** a machine with no `python3`, or one below 3.9
**When** the skill reaches its first script command
**Then** the user sees one message that names the version needed, and no file changes.

**Given** a nesting depth setting below 2 in a session, or below 3 in a subagent
**When** the skill is about to convene
**Then** it stops, changes nothing, and tells the user which setting to change
**And** an unset setting does not stop it.

**Given** a proposal to create, amend, or remove a law
**When** the skill runs
**Then** it frames the proposal and spawns the chair by its full name, so that the proposer never chairs.

**Given** an agent that invokes the skill on its own, past the daily cap
**When** the skill is about to convene
**Then** it asks the user first.

**Given** an amendment or a removal that the chair registered
**When** the skill continues
**Then** an agent rechecks each printed citation against the law in effect, or deletes a citation of a removed law
**And** the change is complete only when `lint` passes.

**Given** a law of origin `agent` that the user wants to confirm
**When** the user says so in the session
**Then** the skill runs `law confirm` with `--as-user`, and only after the user has answered.

**Given** a finished law change
**When** the skill reports
**Then** the session commits it, as a commit of its own where the repo's conventions allow
**And** a working agent that caused the change names it in its final report.

**Given** the skill file
**When** it is read
**Then** it is under 500 lines, holds no root path, and names each script command without restating what the command does.

### Story 4.9: The user's final say at a law table

As a user,
I want the round table to hear my proposal and still leave the last word with me,
So that I get a second opinion I can overrule, and agents cannot overrule me.

**Covers:** FR-20, FR-21; AD-9, AD-10, AD-14; AC-10, AC-28, AC-29.

**Acceptance Criteria:**

**Given** a table that would reword or reject the user's proposal
**When** the chair decides
**Then** it registers nothing, sets the matter to `waiting`, and returns its objection, its counter-proposal, and the exact command line for each choice the user has.

**Given** the chair's return
**When** the user accepts, counters, or directs that the law be registered as written
**Then** the session runs the matching command only after the user has answered in that session
**And** the user sees that exact command at a permission prompt before it runs.

**Given** the user directs registration over the table's objection
**When** the command has run
**Then** the ledger row shows `user override`, the law has origin `user`, and each dissenting seat is named.

**Given** a table that an agent convened to amend or remove a law of origin `user` or `core`
**When** the table recommends the change
**Then** nothing is registered, and the chair returns the recommendation for the user
**And** the law binds every agent until the user answers.

**Given** a subagent that convened the table
**When** the chair returns a command for the session
**Then** the subagent passes the return up unchanged, and neither it nor the chair runs the command.

**Given** a session that no human prompts
**When** a matter needs the user
**Then** the command does not run, and the matter stays `waiting`.

**Given** the scored cases for this story
**When** the evals run
**Then** every one of them passes.

### Story 4.10: A working agent obeys the laws and may propose one

As a user,
I want an agent that meets a law in its way to stop and say so, and an agent that sees a rule worth keeping to propose it,
So that laws are neither worked around nor lost.

**Covers:** FR-15, FR-21, FR-35, FR-36; AC-28. Related journeys: UJ-2, UJ-4, UJ-5.

**Acceptance Criteria:**

**Given** a task that requires breaking a law
**When** a working agent reaches that part
**Then** it stops that part, and names the law's ID
**And** it may take an amendment to a round table, and the law binds until the table decides.

**Given** work that already violates a law
**When** a working agent finds it
**Then** it reports the violation, and fixes it only if that is inside its task.

**Given** a contradiction between two levels of document
**When** a working agent finds it
**Then** it reports it with the ID, and never resolves it silently.

**Given** an agent that sees a rule worth keeping during a task
**When** it invokes the `law` skill
**Then** it does not wait for the user, within the daily cap
**And** an adopted law has origin `agent`, and the agent names the change in its final report.

**Given** the scored cases for conflicts with a law
**When** the evals run
**Then** every one of them passes.

### Story 4.11: Avalon governs this repo through the plugin

As the user,
I want this repo's round tables run by the plugin's own chair, seats, and script,
So that Avalon meets real use before the rest is built, and a stranger knows what this release does.

**Covers:** FR-48, FR-50, FR-51, FR-54; AD-19. This is the first release that governs a repo.

**Acceptance Criteria:**

**Given** this repo with the plugin loaded
**When** a law matter is heard
**Then** the plugin's chair and seats hear it, the script registers it, and the stand-in briefs are no longer used for a law.

**Given** the README after this story
**When** a person reads it
**Then** it states the lowest Claude Code version, the lowest Python version, and the supported systems: macOS, and Linux including Linux under WSL, and not native Windows
**And** it states what the hook approves, what it denies, and how to turn the approval off with an ask rule
**And** it warns against a broad allow rule for the script, which could cover a flagged command
**And** it states that the guards stop shortcuts and accidents and not forgery, and that a round table costs up to 15 seat votes
**And** it says that this release governs laws, and what is not built yet.

**Given** `SECURITY.md`
**When** a person reads it
**Then** it says how to report a vulnerability in private, and which versions get fixes
**And** it says that the stated limits of the guards are known limits and not vulnerabilities.

**Given** the release that carries this story
**When** its notes are read
**Then** they say what a user can now do, and what to do in a repo that was set up with an earlier release.

## Epic 5: Set Avalon up in any repo

The user runs `/avalon:init` in an application, a library, or a story bible, and gets the same core set: the laws, the block, an overview, a glossary, and the two core ADRs.
The script gains the ADR commands, and the three fixtures prove `init` on each profile.

### Story 5.1: `adr new` records an adopted decision

As a user,
I want a decision that a round table adopted to get a numbered ADR file and a ledger row from the script,
So that every decision has one record in one fixed shape.

**Covers:** FR-13, FR-23, FR-24, FR-44, FR-45; AD-6, AD-7, AD-10.

**Acceptance Criteria:**

**Given** a decision matter whose last round holds five recorded votes, and an outcome the table may register
**When** `adr new` runs with the matter ID and a topic
**Then** it creates the whole ADR file from the template, named with the next four-digit number and the topic
**And** the file holds the `adr` and `origin` keys, and a first changelog line with the date and the marker `(user, table)` or `(agent, table)`
**And** the ledger has one more row for the decision
**And** the matter folder is kept, and its state is `adopted`.

**Given** a matter with no complete round and no override
**When** `adr new` runs
**Then** it refuses, and no file changes.

**Given** `--as-user` and `--override`
**When** `adr new` runs
**Then** the ADR has origin `user` and the marker `(user override)`, and the ledger row shows `user override`.

**Given** the next ADR number
**When** it is allocated
**Then** it is the highest number ever used plus one, and a retired number is never reused
**And** the numbers 0001 and 0002 are held for the two core ADRs in every repo.

**Given** an ADR whose changelog is missing, is not the last section, or has a line without a date and a marker
**When** `lint` runs
**Then** it fails.

**Given** the ADR format rendered empty
**When** it is compared with its template
**Then** the two are the same.

### Story 5.2: `adr log` and `adr reject` record a change and a rejection

As a user,
I want a reversal, an added detail, and a rejected decision each recorded by the script,
So that the changelog and the ledger show how each decision got where it is.

**Covers:** FR-13, FR-21, FR-24; AD-7, AD-9, AD-10.

**Acceptance Criteria:**

**Given** a decision matter that adopted a reversal of an ADR
**When** `adr log` runs with the matter ID and a one-line summary
**Then** the ADR's changelog gains one dated line with its marker and that summary
**And** the ledger has one more row that names the reversed ADR.

**Given** detail added to an ADR without changing its decision
**When** `adr log` runs with no matter
**Then** the changelog gains one line marked `(user)` or `(agent)`
**And** the ledger does not change.

**Given** an ADR file that an agent has edited
**When** `adr log` runs
**Then** it reads the file again under the lock, changes only the changelog section, and keeps the rest as it found it.

**Given** a decision that the table rejected
**When** `adr reject` runs with the matter ID
**Then** the ledger has one more row for the rejection
**And** no ADR gains a line.

**Given** a table that an agent convened, and an ADR of origin `user`
**When** `adr log` runs for a reversal without `--as-user` and `--accept`
**Then** it refuses.

**Given** a decision that reached the table after its effect landed
**When** it is registered
**Then** its ledger row says that it was a late decision.

### Story 5.3: `adr retire` deletes an ADR, and no file may cite it

As a user,
I want a decision that stopped applying to be retired through a round table, and its citations found,
So that the ADR folder holds only decisions in effect.

**Covers:** FR-11, FR-24, FR-45; AD-7, AD-9; AC-36, AC-37, AC-38.

**Acceptance Criteria:**

**Given** an ADR, with no recorded votes and no override
**When** `adr retire` runs
**Then** it refuses, and no file changes.

**Given** a matter with five recorded votes to retire an ADR that two files cite
**When** `adr retire` runs
**Then** the ADR file no longer exists
**And** the ledger has one more row that names the number, the title, and the reason
**And** the command prints both citations.

**Given** a tracked file outside the archive and the ledger that cites a retired ADR, as `ADR-` and its number or by its file name
**When** `lint` runs
**Then** it fails, and names the file and the line
**And** the script reads the retired numbers from the ledger.

**Given** the same number in the archive and in the ledger
**When** `lint` runs
**Then** it raises nothing for them.

**Given** a citation of a retired ID inside an ADR's changelog
**When** `cite fix` runs on it
**Then** the script writes the replacement or the removal.

**Given** a table that an agent convened, and an ADR of origin `user`
**When** `adr retire` runs without `--as-user` and `--accept`
**Then** it refuses.

### Story 5.4: The user confirms an agent's ADR

As a user,
I want to turn a decision that agents adopted into my own with one command,
So that I stand behind it without calling another round table.

**Covers:** FR-13, FR-24; AD-9; AC-41.

**Acceptance Criteria:**

**Given** an ADR of origin `agent`
**When** `adr confirm` runs with `--as-user`
**Then** the ADR has origin `user`, and its decision is unchanged
**And** its changelog gains a `(user)` line
**And** the ledger has one more row, decided by `user`, with `none` for the rounds, the tally, and the dissent.

**Given** `adr confirm` without `--as-user`, or on an ADR whose origin is not `agent`
**When** it runs
**Then** it refuses, and no file changes.

### Story 5.5: A decision that predates Avalon is recorded without a round table

As a user,
I want a decision that was already in effect when Avalon was installed to be recorded as it stands,
So that old choices get a record without a vote on what is already done.

**Covers:** FR-13, FR-25, FR-32, FR-44; AD-9, AD-10, AD-11; AC-14, AC-39, AC-43, AC-44.

**Acceptance Criteria:**

**Given** a legacy record with `--as-user`, whose `covers` entries all match a path that existed before the install landed, and whose `evidence` files all existed then
**When** `adr new` runs for it
**Then** the ADR is created with origin `user`, the `evidence` key, and a changelog line marked `(legacy)`
**And** the ledger gains no row.

**Given** a legacy record with a `covers` entry that matches no path from before the install
**When** `adr new` runs
**Then** it refuses.

**Given** a legacy record with no `evidence` file, with one that did not exist before the install, or without `--as-user`
**When** `adr new` runs
**Then** it refuses.

**Given** a repo whose install is committed
**When** the legacy test looks for the repo as it stood before the install
**Then** it reads the first parent of the oldest commit, reachable from `HEAD`, that added the config file
**And** it does not compute from the install commit that the config file records.

**Given** a repo whose install was squash-merged or rebased, so that the recorded install commit is not in the history
**When** the legacy test runs
**Then** it still finds the repo as it stood before the install, and gives the same answers.

**Given** a config file that is not committed yet
**When** the legacy test runs
**Then** it reads the repo at `HEAD`.

**Given** the commit that added the config file has no parent
**When** the legacy test runs
**Then** it refuses, and says that nothing in the repo predates the install.

**Given** a shallow clone
**When** a legacy record is attempted
**Then** the command refuses and says why.

**Given** the git adapter
**When** this story extends it
**Then** it also answers which paths existed at a commit, which commit added a path and what its first parent is, and whether the clone is shallow
**And** the contract suite proves each against real git, on a plain history, a squash-merged history, and a rebased one.

**Given** `scaffold` in a repo
**When** it records the install decision
**Then** `0002-documentation-system.md` is created once, with origin `user`, the marker `(user)`, and no ledger row
**And** the ADR index lists it, and `lint` still passes straight after `scaffold`
**And** a second attempt to record it is refused.

### Story 5.6: The tech writer words what it is given

As a user,
I want one agent that writes every ADR and design doc to the writing standard,
So that documents read alike, and none holds a reason nobody gave.

**Covers:** FR-4, FR-39, FR-41; AD-7, AD-14.

**Acceptance Criteria:**

**Given** the `tech-writer` file
**When** it is read
**Then** its tools are Read, Grep, Glob, Write, Edit, and Bash
**And** it tells the agent to load the writing standard from the target repo's laws folder every time.

**Given** content to write
**When** the `tech-writer` works
**Then** it decides whether to extend a document or create one, when to split one, and how to word each line
**And** it writes any Mermaid diagram.

**Given** a reason, a history, or an intent that it was not given
**When** the `tech-writer` writes
**Then** it writes it as unknown, and invents nothing
**And** it makes no decision about what is true or chosen.

**Given** an existing ADR or design doc
**When** the `tech-writer` changes it
**Then** it uses the Edit tool and never a whole-file Write
**And** it leaves the keys and the changelog that the script owns as they are.

**Given** a file under the laws folder
**When** the `tech-writer` works
**Then** it never writes it.

**Given** a finished piece of writing
**When** the pass continues
**Then** the `prose-editor` edits once and the lint runs, and the two agents do not go back and forth
**And** the `tech-writer` returns its outcome and the paths it changed, and never commits.

### Story 5.7: The chair hears a decision

As a user,
I want the round table to hear a decision with a seat that hunts for missed alternatives,
So that a costly choice is tested before it is carried out.

**Covers:** FR-15, FR-17, FR-19, FR-21; AD-13, AD-14; AC-26.

**Acceptance Criteria:**

**Given** a decision matter
**When** the chair seats the table
**Then** five seats vote, and the Scout sits in place of the Enforcer.

**Given** a decision the table adopts, reverses, rejects, or retires
**When** the chair registers it
**Then** it runs the matching ADR command, and keeps the matter folder for the `tech-writer`
**And** it returns the outcome, the matter ID, and the paths that changed.

**Given** a table that an agent convened
**When** the matter is a new decision, or a reversal of an ADR of origin `agent`
**Then** the chair registers the outcome at once.

**Given** a table that an agent convened, and an ADR of origin `user`
**When** the table recommends a reversal or a retirement
**Then** the chair registers nothing, and returns the recommendation for the user.

**Given** the chair's file after this story
**When** the parse test reads every command line in it
**Then** each one names a command that exists.

### Story 5.8: Three fixtures stand in for real repos

As a maintainer,
I want a small code repo, a library, and a story bible kept for testing,
So that `init` and the audits are proven on more than one kind of work.

**Covers:** FR-2, FR-46, FR-53; NFR-4; AD-12, AD-16.

**Acceptance Criteria:**

**Given** `fixtures/`
**When** it is listed
**Then** it holds `code-repo`, `library`, and `story-bible`
**And** each holds invented content only, with no secret and no person's details.

**Given** one of the fixtures
**When** it is read
**Then** it holds decoy project agents named `chair` and `tech-writer`, and a decoy `docs/adr/` folder with content.

**Given** a test or an eval that needs a fixture
**When** it runs
**Then** it copies the fixture to a temporary folder outside this repo
**And** only the contract suite and the evals give the copy a git repo.

**Given** the `plugin/` folder
**When** it is installed
**Then** no fixture is in the installed copy.

### Story 5.9: `init` surveys a repo and sets Avalon up in it

As a user,
I want one skill that looks at my repo, picks a safe place for the docs, and sets Avalon up,
So that I can adopt Avalon in any repo without reading how it works first.

**Covers:** FR-22, FR-31, FR-32, FR-33, FR-36, FR-54; NFR-4; AD-3, AD-12.

**Acceptance Criteria:**

**Given** a machine with no suitable Python
**When** the user runs `/avalon:init`
**Then** the skill makes that check first, shows one message that names the version needed, and sets nothing up.

**Given** a repo
**When** `init` surveys it
**Then** it sets the profile to `application`, `service`, `library`, `story-bible`, or `other`.

**Given** no config file
**When** `init` chooses the root
**Then** it passes the plugin's `default_root` option to `scaffold` as an argument when the user has set it, and `docs/` otherwise.

**Given** a root that holds content Avalon did not create
**When** `init` runs
**Then** it proposes another root, such as `docs/avalon/`, offers it to the user, and writes nothing into the first folder.

**Given** a site generator that publishes the whole of `docs/`
**When** `init` runs
**Then** it warns the user and suggests another root.

**Given** a nesting depth setting too low for a round table
**When** `init` runs
**Then** it warns the user, and says which setting to change.

**Given** the offer to write the block into `AGENTS.md`
**When** the user declines
**Then** `AGENTS.md` is not written.

**Given** ADRs the repo already holds
**When** `init` runs
**Then** it leaves each one untouched and lists it.

**Given** a repo that `init` has already set up
**When** it runs again
**Then** the install time, the install commit, and every existing document are unchanged.

**Given** a folder that is not a git repo, or a repo with no commit
**When** `init` runs
**Then** it passes on the refusal, and tells the user that a first commit is needed.

### Story 5.10: `init` writes the core documents

As a user,
I want `init` to write an overview, a glossary, and the two core ADRs from what my repo shows,
So that an agent's first read of my repo is true and marks what is unknown.

**Covers:** FR-2, FR-4, FR-25, FR-27, FR-32; AD-7, AD-9, AD-10.

**Acceptance Criteria:**

**Given** a repo that `scaffold` has set up
**When** `init` continues
**Then** the `tech-writer` fills the overview, and leaves out every section that does not apply
**And** it adds the repo's own terms to the glossary
**And** the `prose-editor` edits both, `index` runs, and `lint` passes.

**Given** a repo that held work before the install
**When** `init` records the architecture
**Then** `0001-architecture.md` states the repo's form, its major parts and their boundaries, and its primary technologies or formats
**And** it is recorded as a legacy record, by a command the user accepts at a prompt
**And** a reason that the repo does not show is written as unknown.

**Given** a repo that held no work before the install
**When** `init` runs
**Then** it writes no `0001-architecture.md`, and tells the user that the first architecture decision goes to a round table.

**Given** `0002-documentation-system.md`
**When** `init` has finished
**Then** it records the decision to adopt Avalon, with the root path and any local setting.

**Given** decisions that `init` found in the repo with no record
**When** it reports
**Then** it lists them, and the user chooses which to write.

**Given** the repo's profile
**When** `init` reports
**Then** it suggests further design docs that fit the profile.

### Story 5.11: `init` is proven on every fixture

As a maintainer,
I want scored cases that run `init` on each fixture,
So that Avalon is shown to work on a code repo, a library, and a story bible, and beside names that clash with its own.

**Covers:** FR-2, FR-36, FR-41, FR-46; NFR-4; AC-24, AC-31; SM-9.

**Acceptance Criteria:**

**Given** each of the three fixtures
**When** `init` runs on a copy
**Then** it leaves a tree whose `lint` passes.

**Given** the story bible fixture
**When** `init` has run
**Then** the overview has no section that does not apply
**And** the core ADRs mark unknown reasons as unknown.

**Given** the fixture with the decoy agents and the decoy `docs/adr/` folder
**When** Avalon runs there
**Then** each agent is spawned by its full `avalon:` name, and runs Avalon's prompt and not the decoy's
**And** `init` proposes another root, and writes nothing into the decoy folder.

**Given** the results of these cases
**When** an agent's model or effort is changed
**Then** the change is made in that agent's own file, and the cases still pass.

## Epic 6: Record decisions and describe the repo

The user, or a working agent, takes a decision to a round table with `/avalon:adr`, and the `tech-writer` writes the ADR.
`/avalon:design` writes, updates, splits, and merges design docs. `/avalon:intake` sorts a design conversation into laws, decisions, and description.

### Story 6.1: The `adr` skill takes a new decision to the round table

As a user,
I want one skill that tests whether a choice is a decision, takes it to the round table, and has the ADR written,
So that a costly choice is heard before it is carried out, and recorded when it is adopted.

**Covers:** FR-3, FR-15, FR-19, FR-23, FR-24, FR-36, FR-54; AD-7, AD-10, AD-13.

**Acceptance Criteria:**

**Given** a proposed decision
**When** the user or an agent invokes `/avalon:adr`
**Then** the skill applies the ADR test first: the choice is costly to reverse, and there were real alternatives that a future reader would ask about.

**Given** a new decision that fails the ADR test
**When** the skill sorts it
**Then** no round table sits, and no ADR is written.

**Given** a decision that an existing ADR's topic already covers
**When** the skill frames it
**Then** it revises that ADR, and creates no other.

**Given** a decision that passes the test
**When** the table adopts it
**Then** the `tech-writer` reads the adopted text and the reasons from the matter folder, and fills the body, the `summary`, and the `covers` of the ADR
**And** the `prose-editor` edits it once
**And** the skill then runs `index` and `lint`, and closes the matter only when `lint` passes.

**Given** a decision that the table rejects
**When** the skill reports
**Then** the ledger holds the rejection, and no ADR holds a line about it.

**Given** an adopted decision
**When** the skill finishes
**Then** it asks whether the decision implies a law
**And** a law that follows goes to the round table as a proposal of its own, and names the ADR as its source.

**Given** the same checks as the `law` skill
**When** `/avalon:adr` starts
**Then** it stops with one plain message on a missing or old Python, and before it convenes on a nesting depth that is too low.

### Story 6.2: The `adr` skill changes, retires, and confirms a decision

As a user,
I want to reverse, retire, extend, or confirm a recorded decision from my session,
So that each ADR always states the decision in effect, and I keep the last word on my own.

**Covers:** FR-20, FR-21, FR-23, FR-24, FR-25, FR-36; AD-9; AC-28, AC-29. Related journeys: UJ-6, UJ-8.

**Acceptance Criteria:**

**Given** a reversal that the table adopts
**When** the ADR is rewritten
**Then** its body states the new decision
**And** the old choice moves to Alternatives rejected, with the word "Rejected" and the reason it was left
**And** the changelog gains one line.

**Given** a reversal or a retirement of an ADR in effect
**When** the skill runs
**Then** a round table always sits first.

**Given** detail to add to an ADR without changing its decision
**When** the skill runs
**Then** no round table sits, and the changelog gains one line.

**Given** an ADR of origin `agent` that the user wants to confirm
**When** the user says so in the session
**Then** the skill runs the confirm command with `--as-user`, and only after the user has answered.

**Given** a table that would reword or reject a decision the user proposed
**When** the chair returns
**Then** nothing is registered until the user accepts, counters, or directs that it be registered as written.

**Given** a decision that predates Avalon, with evidence from before the install
**When** the user asks for it to be recorded
**Then** the skill records it as a legacy record, by a command the user accepts at a prompt, and no round table sits.

**Given** a decision with no evidence file, or one that landed after install
**When** the user asks for it to be recorded
**Then** it goes to the round table as a late decision, and its ledger row says so.

**Given** a retired ADR that other files cite
**When** the skill continues
**Then** an agent fixes each printed citation, and the change is complete only when `lint` passes.

### Story 6.3: The `design` skill writes and reshapes design docs

As a user,
I want one skill that writes, updates, splits, and merges design docs,
So that the description of my repo stays in a few documents that each have one subject.

**Covers:** FR-4, FR-26, FR-27, FR-29, FR-30, FR-36; AD-7.

**Acceptance Criteria:**

**Given** material to describe
**When** the user invokes `/avalon:design`
**Then** the `tech-writer` puts it in the document that owns its subject, and creates a document only when none does
**And** the `prose-editor` edits once, `index` runs, and `lint` passes.

**Given** a design doc that covers more than one subject, or is longer than the size cap
**When** the skill splits it
**Then** the split leaves no stub, and every link and the index are updated.

**Given** two design docs on one subject
**When** the skill merges them
**Then** one document remains, and every link to the other points to it.

**Given** a term specific to the repo that a document uses
**When** the skill writes
**Then** the glossary defines it once, in alphabetical order, and the document links to it
**And** a definition that tells an agent what it must do is not written into the glossary, and goes to the round table as a law proposal.

**Given** a design doc
**When** the skill writes it
**Then** it describes only the present, has no changelog, and holds at most five `covers` entries.

**Given** a diagram or an image
**When** the skill adds it
**Then** a diagram is Mermaid, with a sentence before it that says what it shows
**And** an image shows only what Mermaid cannot draw, has alt text, and sits in the assets folder.

### Story 6.4: The `intake` skill sorts a design conversation

As a user,
I want to hand Avalon a design, a spec, or a conversation and have it sorted,
So that each rule, decision, and description lands in the kind of document that fits it.

**Covers:** FR-1, FR-3, FR-15, FR-32, FR-36. Related journey: UJ-11.

**Acceptance Criteria:**

**Given** a design, a spec, or a conversation
**When** the user invokes `/avalon:intake`
**Then** the skill sorts its content into law candidates, decisions, and description
**And** it shows the user the sorting before anything is proposed.

**Given** the law candidates and the decisions
**When** the skill continues
**Then** each goes to a round table, and related ones may be heard as a slate with a separate vote on each.

**Given** the description
**When** the skill continues
**Then** it goes to design docs, through the same writing pass as the `design` skill.

**Given** content that is planned work and not a rule, a decision, or a description of the repo as it is
**When** the skill sorts it
**Then** it is left out, and the skill says so.

**Given** an ADR that the repo held before Avalon
**When** the user folds it in through `intake`
**Then** it becomes a legacy record, with the existing file as its evidence
**And** the skill asks the user whether to delete the old file or to replace its body with a link.

### Story 6.5: A working agent obeys the ADRs, and this repo's decisions run through the plugin

As a user,
I want an agent that meets a recorded decision in its way to stop and say so,
So that no later agent undoes a choice without knowing it was made.

**Covers:** FR-21, FR-35, FR-36, FR-48; AD-19. Related journey: UJ-6.

**Acceptance Criteria:**

**Given** a task that requires breaking an ADR
**When** a working agent reaches that part
**Then** it stops that part, and names the ADR
**And** it may take a reversal to a round table, and the ADR binds until the table decides.

**Given** work that disagrees with an ADR
**When** a working agent finds it
**Then** it reports it, and either the work is fixed or the decision goes to the round table as a change.

**Given** an ADR that disagrees with a law
**When** a working agent finds it
**Then** it reports it, and either the ADR is revised or an amendment goes to a round table.

**Given** a design doc that disagrees with the work
**When** a working agent finds it
**Then** it updates the design doc.

**Given** the scored cases for conflicts with an ADR
**When** the evals run
**Then** every one of them passes.

**Given** this repo after this story
**When** a decision is proposed, changed, or retired
**Then** the plugin's `adr` skill, chair, and script handle it, and no stand-in is used
**And** every ADR that was written by hand passes `lint`.

## Epic 7: Keep the docs true

A working agent finds what covers the path it is about to change. The user audits the docs with `/avalon:check`, and brings them back in line after work with `/avalon:sync`.

### Story 7.1: `for` lists what covers a path

As a working agent,
I want one command that names the ADRs and design docs for the path I am about to change,
So that I read what binds and describes that path, and nothing else.

**Covers:** FR-28, FR-42; AD-6; AC-18. Related journey: UJ-2.

**Acceptance Criteria:**

**Given** a path that one ADR and one design doc cover
**When** `for` runs on it
**Then** it lists both, one record on each line, and nothing else.

**Given** a path that no document covers
**When** `for` runs on it
**Then** it lists nothing, and exits 0.

**Given** the `covers` entries of every document
**When** `for` matches them
**Then** it uses the same matcher as the lint.

**Given** a skill that leads an agent to change a file
**When** its file is read
**Then** it tells the agent to run `for` on the path first.

### Story 7.2: `stale` lists the design docs that fell behind, and `verify` stamps one

As a user,
I want the script to tell me which design docs describe paths that changed since they were last checked,
So that I review only those, and trust the rest.

**Covers:** FR-26, FR-43; AD-7, AD-11; AC-15, AC-33, AC-34, AC-35.

**Acceptance Criteria:**

**Given** a design doc, and a covered path that changed in a commit after the one in which the doc's stamp landed
**When** `stale` runs
**Then** it lists the doc.

**Given** a listed doc that an agent has reviewed
**When** `verify` runs on it
**Then** the doc's `verified` date and `verified_commit` are set, and no other part of the file changes
**And** `stale` no longer lists it.

**Given** a design doc, its stamp, and a change to a covered path that all land in one commit
**When** `stale` runs
**Then** it does not list the doc.

**Given** a covered path with an uncommitted change, and a doc whose stamp is committed
**When** `stale` runs
**Then** it lists the doc.

**Given** a doc whose stamp is not committed yet
**When** `stale` runs
**Then** it does not list the doc.

**Given** a design doc with no stamp
**When** `stale` runs
**Then** it lists the doc as never verified, and `lint` does not fail on it.

**Given** a shallow clone
**When** `stale` runs
**Then** it refuses and says why.

**Given** the git adapter
**When** this story extends it
**Then** it also answers which commits changed a path, and which paths have uncommitted changes
**And** the contract suite proves both against real git, and shows that the index is unchanged.

**Given** the `design` skill
**When** it has finished writing a design doc
**Then** it runs `verify` only after the writing agents have returned.

### Story 7.3: `status` gives one short summary

As a user,
I want one command that tells me where the docs stand,
So that I and my agents read one summary and not every file behind it.

**Covers:** FR-12, FR-42; AD-5, AD-10, AD-13.

**Acceptance Criteria:**

**Given** a target repo
**When** `status` runs
**Then** it prints the count of laws in effect against the cap, the stale design docs, and the result of the lint.

**Given** a matter that waits for the user
**When** `status` runs
**Then** it lists each matter with its state.

**Given** a journal left in `.avalon/`
**When** `status` runs
**Then** it reports the journal and does not apply it.

**Given** a tree in an older format
**When** `status` runs
**Then** it parses nothing more, and says that the tree needs to be migrated.

**Given** any run of `status`
**When** it ends
**Then** it has written no file.

### Story 7.4: The law reviewer reports what breaks a law or an ADR

As a user,
I want an agent that checks a diff or a path against the laws and the ADRs,
So that a rule in context is checked, and not only trusted.

**Covers:** FR-38, FR-41; AD-14.

**Acceptance Criteria:**

**Given** a diff or a path
**When** the `law-reviewer` runs
**Then** it reports each violation with the ID of the law or the ADR, the location, and a confidence.

**Given** a finding
**When** its confidence is set
**Then** it is high when the text and the work plainly conflict, medium when they conflict on the likeliest reading, and low when they may conflict and a person should look.

**Given** a law in scope that has a detail file
**When** the `law-reviewer` checks against it
**Then** it opens that detail file.

**Given** a violation
**When** the `law-reviewer` finds it
**Then** it never fixes it.

**Given** the agent file
**When** it is read
**Then** it is the only home of the findings format
**And** its tools are Read, Grep, Glob, and Bash.

**Given** the scored cases for the `law-reviewer` on the fixtures
**When** the evals run
**Then** they meet the threshold.

### Story 7.5: `check` audits the docs and changes nothing

As a user,
I want one skill that reports every problem in the docs,
So that I see where structure, consistency, or prose has slipped before I decide what to fix.

**Covers:** FR-36, FR-37, FR-38, FR-40. Related journey: UJ-10.

**Acceptance Criteria:**

**Given** a target repo
**When** the user invokes `/avalon:check`
**Then** it runs the lint, then an agent audit for contradictions between laws, ADRs, the work, and design docs, then a prose review of every document.

**Given** the prose review under `check`
**When** the `prose-editor` runs
**Then** it reviews every document and only reports.

**Given** a full audit
**When** the user asks for one
**Then** `check` may run the `law-reviewer` on a stronger model.

**Given** any run of `check`
**When** it ends
**Then** no document has changed
**And** its report names each finding with its file, and the ID where there is one.

### Story 7.6: `sync` brings the docs back in line after work

As a user,
I want one skill that updates the docs after a session of work,
So that what the docs describe matches what the repo holds.

**Covers:** FR-26, FR-36, FR-37, FR-38. Related journey: UJ-9; SM-8.

**Acceptance Criteria:**

**Given** a session of work that changed covered paths
**When** the user invokes `/avalon:sync`
**Then** it runs `stale`, and an agent reviews only the listed docs, opening their images too.

**Given** a listed doc
**When** the review finds it untrue
**Then** the `tech-writer` updates it, and the `prose-editor` edits once.

**Given** a listed doc, reviewed and true
**When** the review ends
**Then** the skill resets its stamp through `verify`.

**Given** a decision made during the session that has no record
**When** `sync` reviews the changes
**Then** it flags the decision, and does not record it on its own.

**Given** a law violation in the changes
**When** `sync` reviews them
**Then** it flags the violation, and does not fix it on its own.

**Given** the end of a `sync`
**When** `stale` runs
**Then** it lists no design doc.

## Epic 8: Ready for version 1.0

Two branches that each changed laws can be joined. A root can be moved. A tree in an older format can be brought up to date. A target repo can run the lint in CI.
Every release gate passes, a stranger can install from the README alone, and `v1.0.0` ships.

### Story 8.1: `move-root` moves the tree

As a user,
I want one command that moves Avalon's docs to another folder,
So that I can change where they live without breaking a link.

**Covers:** FR-33; AD-5, AD-6, AD-7; AC-19.

**Acceptance Criteria:**

**Given** a target repo with the root `docs/`
**When** `move-root` runs with the root `docs/avalon/`
**Then** the tree is under the new root
**And** the config file, the block, and every link use the new root
**And** `lint` passes.

**Given** a move
**When** it rewrites a governed file
**Then** it changes links and nothing else in a body
**And** the checksum is unchanged.

**Given** a new root that holds content Avalon did not create, or that breaks the rules for a root
**When** `move-root` runs
**Then** it refuses, and no file changes.

**Given** `move-root`
**When** the hook checks the command
**Then** it never approves it, and the user is asked.

### Story 8.2: `merge` joins law changes from two branches

As a user,
I want one command that makes the law record whole after a git merge of two branches that each changed laws,
So that neither branch's laws are lost, and I never edit the record by hand.

**Covers:** FR-45, FR-60; AD-5, AD-6, AD-11.

**Acceptance Criteria:**

**Given** a git merge that left conflict markers in the registry, the ledger, or the config file
**When** `lint` runs
**Then** it fails and names `merge` as the command to run.

**Given** conflict markers, and the name of the side that is already on the shared branch
**When** `merge` runs
**Then** it reads both sides from the markers, and reads nothing more from git
**And** the named side keeps its IDs
**And** a law on the other side whose ID collides takes the next free ID
**And** every pointer to it in the registry, the archive, the ledger, and the name of its detail file is rewritten
**And** every other citation of it is printed, for an agent to fix.

**Given** the two sides
**When** `merge` has run
**Then** every row from both sides is kept, and no decision is added or dropped
**And** the checksum for the joined files is recorded
**And** `lint` passes once the printed citations are fixed.

**Given** both sides amended or removed the same law
**When** `merge` runs
**Then** it refuses, changes no file, and says that the matter goes to a round table.

**Given** the two sides hold different system versions
**When** `merge` runs
**Then** it refuses, and names `migrate` for the older side.

**Given** `merge`
**When** it runs
**Then** it writes nothing to git, and the hook never approves it without asking.

### Story 8.3: `merge` joins ADR changes from two branches

As a user,
I want the same command to settle two ADRs that took the same number,
So that every decision keeps its record after a merge.

**Covers:** FR-45, FR-60; AD-6, AD-7.

**Acceptance Criteria:**

**Given** two branches that each created an ADR with the same number, and conflict markers in the ledger
**When** `merge` runs with the shared side named
**Then** the ADR on the other side takes the next free number
**And** its file name, its `adr` key, its ledger row, and its index entry are rewritten
**And** every other citation of it is printed.

**Given** two ADR files that share a number with no conflict marker anywhere
**When** `lint` runs
**Then** it fails and names `merge`.

**Given** two ADR files that share a number with no conflict to read
**When** the user names the file that takes the next number
**Then** `merge` renumbers that file, and rewrites the pointers to it.

**Given** a merge that rewrote an ADR
**When** its body is compared with the body before
**Then** only links and IDs differ.

### Story 8.4: An upgrade never changes what the record says

As a user,
I want a later plugin version to work in a repo that an earlier one set up, and to change a tree's layout only when I ask,
So that updating the plugin never rewrites my laws or decisions.

**Covers:** FR-45, FR-61; AD-5, AD-6. The steps inside `migrate` are written by the first release that changes a format.

**Acceptance Criteria:**

**Given** a tree in the current format
**When** `migrate` runs
**Then** it says there is nothing to do, and changes no file.

**Given** a tree in an older format, built in a test from a frozen older reader
**When** `migrate` runs
**Then** every law, archive row, ledger row, ADR, and design doc keeps its content, and only its layout changes
**And** the install time and the install commit are as they were
**And** the command prints each file it changed, and records the system version and the checksum.

**Given** `formats/legacy/`
**When** it is read
**Then** it holds one frozen reader for each past version, and only `migrate` imports it.

**Given** `init` or `scaffold` on a tree in an older format
**When** it runs
**Then** it does not migrate the tree.

**Given** a later release that changes the text of a core law
**When** a user updates the plugin
**Then** the update changes no law in a target repo
**And** the change reaches that repo only as an amendment that a round table hears and the user confirms.

**Given** a release that changes a file format
**When** its notes are written
**Then** they say so, and name the command to run
**And** after 1.0 such a release takes the `major` label.

**Given** `migrate`
**When** the hook checks the command
**Then** it never approves it without asking.

### Story 8.5: A target repo can run the lint in CI

As a user,
I want a recipe that runs Avalon's lint in my repo's CI,
So that a broken record is caught on a pull request, with no agent and no model.

**Covers:** FR-26, FR-62; AD-11, AD-16. It settles one deferred item: how the recipe fetches the script.

**Acceptance Criteria:**

**Given** the Avalon docs
**When** a user looks for the CI recipe
**Then** it fetches `plugin/script/` at a release tag, and runs `lint`
**And** it needs Python 3 and git, and neither Claude Code nor a model.

**Given** a shallow clone
**When** `lint` runs in it
**Then** it works.

**Given** a repo that also wants `stale` in CI
**When** the user reads the recipe
**Then** it does not run `stale`, and it shows how to fetch the full history for a repo that wants it.

**Given** the recipe
**When** it is read
**Then** it says that whether the lint gates a merge is the target repo's choice.

**Given** the recipe as written
**When** it is run against a copy of a fixture
**Then** it passes on a clean tree, and fails on a tree with a hand-edited registry.

### Story 8.6: A stranger can decide and install from the README alone

As a person who has never seen Avalon,
I want the README to tell me what it is, what it needs, what it costs, and how to install it,
So that I can decide and set it up without help.

**Covers:** FR-50, FR-51, FR-53, FR-54; SM-11, SM-12.

**Acceptance Criteria:**

**Given** the README
**When** a person reads it
**Then** it states what Avalon is, whether it is a pre-release, where the latest release is, and the licence
**And** it states the lowest Claude Code version, the lowest Python version, and the supported systems
**And** it gives the two install commands and the first step, `/avalon:init`
**And** it states what Avalon writes into a repo, that the text it writes carries no condition, and that it collects no usage data
**And** it states what the hook approves and denies, and the limits a user must know before trusting it
**And** it links to the licence, the contributor guide, the security policy, the CI recipe, and the release notes.

**Given** a machine that has never held Avalon, on each supported operating system
**When** a person follows only the README
**Then** the plugin installs, and `lint` passes after `init`.

**Given** the repo on GitHub
**When** its community standards checklist is opened
**Then** every item is complete.

**Given** the tracked files
**When** the secret scan runs
**Then** it finds nothing.

### Story 8.7: Every release gate is proven

As the user,
I want each condition for version 1.0 checked and recorded,
So that 1.0 claims only what has been shown.

**Covers:** FR-48, FR-52; SM-1, SM-2, SM-3, SM-10.

**Acceptance Criteria:**

**Given** the 45 acceptance scenarios in `tmp/SPEC.md` section 17
**When** each is matched to what proves it
**Then** each of the 33 script scenarios has an automated test that passes, named for its behaviour
**And** each of the 12 plugin scenarios has an eval case that passes
**And** the nine scenarios that describe git are proven against the fake, and the contract suite proves the git adapter.

**Given** the scored cases on each fixture
**When** the evals run
**Then** every case for the user's final say, for the limits on a table an agent convenes, and for conflict handling passes
**And** at least 80% of the other cases pass on each fixture.

**Given** the top of the repo
**When** `claude plugin validate .` runs
**Then** it passes.

**Given** this repo's ledger
**When** it is read
**Then** it shows that a round table ratified each of the nine core laws.

**Given** a gap this story finds
**When** it is recorded
**Then** it is fixed, or the user decides that 1.0 waits for it.

### Story 8.8: The plans are retired

As the user,
I want the planning files removed once everything lasting in them lives in this repo's own documents,
So that the repo holds one source of truth, and nothing points at a file that is gone.

**Covers:** FR-48; AD-1, AD-19.

**Acceptance Criteria:**

**Given** the plan files under `_bmad-output/` and `tmp/`
**When** each rule, decision, and description in them is checked
**Then** every one that must last is in a law, an ADR, or a design doc of this repo, in its own words
**And** a decision still to be recorded goes to a round table first.

**Given** that check is complete
**When** the user agrees
**Then** the plan files are deleted, and not before.

**Given** the repo after the deletion
**When** the scan of tracked files runs with its skip list emptied of plan folders
**Then** it passes
**And** no tracked file names a plan folder.

**Given** the planning tools under `_bmad/`
**When** the user decides whether they stay
**Then** the decision is carried out, and the ignore rules and the lint config match it.

### Story 8.9: Version 1.0.0 ships

As the user,
I want the first release that claims the whole of Avalon,
So that a person who installs it knows it is no longer a pre-release.

**Covers:** FR-52, FR-59, FR-61; AD-20.

**Acceptance Criteria:**

**Given** every release gate has passed
**When** the owner decides to release 1.0
**Then** the owner sets the repository variable that allows `major`.

**Given** a pull request that removes the pre-release statement from the README
**When** it carries the `major` label
**Then** the check on the pull request shows `v1.0.0` as the version it would get
**And** its merge makes the tag `v1.0.0` and a GitHub release.

**Given** the notes of that release
**When** a person reads them
**Then** they say what Avalon does, and what a user must do in a repo that an earlier release set up.

**Given** a release after `v1.0.0` that changes a file format
**When** its pull request is labelled
**Then** it carries `major`.

## Assumptions made at each gate

The workflow stops for the user four times. This run took the default each time, and each choice below stands until the user changes it.

### Gate 1: the inputs and the extracted requirements

- The inputs are the PRD, its addendum, the architecture spine, and `tmp/SPEC.md`. The PRD names `tmp/SPEC.md` as the home of the requirement text and the acceptance scenarios. `tmp/BRIEF.md` holds reasoning only, and it was not loaded.
- There is no UX input, and none is needed.
- The PRD and the spine are both still drafts. This breakdown treats every answer in them as standing.

### Gate 2: the epic structure

- There are eight epics, one for each build step. The PRD says the build follows those steps, so a different grouping would have to cut across them.
- Epic 3 is named for the script. The workflow prefers an epic named for a user's outcome, and Epic 3 has one: after it, a person can set a repo up by hand and every session there loads the laws.

### Gate 3: the stories

Where the PRD and the spine differ on timing, the stories follow the spine, because it is the later document:

- The core laws are ratified in Epic 2. PRD section 9.2 places that in step 4.
- The Avalon lint joins the gates at the end of Epic 3, when the script can run it. The PRD says step 4.
- A table that an agent convenes is counted at `matter open`. PRD FR-21 says at the first packet.
- The chair gains its steps for a decision in Epic 5, with the ADR commands. The `adr` skill that most often calls them is in Epic 6.

Other choices:

- The first fixture is built in Epic 4, because the first evals need a target repo. The PRD places all three fixtures in step 5.
- The PRD names eight templates. The spine says every governed document that `scaffold` creates has one, so Stories 2.3 and 2.4 add templates for the ledger, the overview, the glossary, and the two indexes.
- The splitter for git conflict markers is built in Story 3.4, because the hook and the version check need it long before `merge` exists.
- `cite fix` is built in two parts: for files under the laws folder in Story 3.13, and for an ADR's changelog in Story 5.3.
- `status` arrives in Epic 7. Between Epic 4 and Epic 7, a matter that waits for the user is visible only in the chair's return.
- A stand-in table keeps its proposal and votes in a matter folder under `.avalon/`, written by hand, so that the working files are never tracked.
- Story 5.1 holds the numbers 0001 and 0002 for the two core ADRs in every repo. The PRD states the hold only for a repo that is empty at install. In any other repo `init` uses both numbers at once, so the result is the same.

### Gate 4: the final check

- The checks in "Final validation" below were run by the same agent that wrote the stories. No second reviewer has read this file.

## Answers to the open points

The first draft of this file left five points for the user. On 2026-11-11 the user asked that each be reasoned to an answer.
Every answer below is this breakdown's reasoning, not the user's word. None is open, and each stands until the user changes it.

### 1. The install commit and squash merges

**The point.** `scaffold` records the commit it ran on, and the legacy test read the repo at that commit. A squash merge or a rebase discards the commits of a branch. So a repo that ran `init` on a branch could record an install commit that is not in its history, and the legacy test would have nothing to read.

**The answer.** The legacy test no longer computes from the recorded commit. It reads the repo as it stood before the install landed, and it finds that point in the history:

- With the install committed: the first parent of the oldest commit, reachable from `HEAD`, that added the config file.
- With the config file not committed yet: `HEAD`.
- Where that commit has no parent: nothing is legacy, and the test says so.

The recorded install commit stays as a record. It is still written once, and the checksum still covers it.

**Why.**

- The sources already treat a design doc's stamp this way. `stale` uses the commit in which the stamp landed, and the stored `verified_commit` only records what was checked.
- A commit that is found in the history survives a squash and a rebase. A commit ID in a file does not.
- On a squash merge, the point found is the shared branch just before the merge. Work done on the branch before `scaffold` ran then counts as after the install, so a decision about it goes to a round table as a late decision. The test errs toward a hearing, which is the safe side.
- The oldest commit is used, so that deleting the config file and adding it again cannot move the point later.

**What it changes.** Spine AD-11, PRD FR-25 and OQ-46, the PRD addendum, and Stories 1.2 and 5.5. It changes REQ-142 in `tmp/SPEC.md`.

### 2. Who proposes the architecture

**The point.** The spine's answers are the planning work's reasoning, and the user has not confirmed them. Should the architecture's ADR carry origin `agent` or `user`?

**The answer.** A record carries the origin of whoever made the call.

- A call the user stated goes to the table as the user's proposal. The gates on a ready pull request and the release by label are examples.
- A call the planning work reasoned goes as an agent's proposal. The entry file with a package, and the contract suite, are examples.
- An ADR that mixes the two is an agent's.
- When a table has finished, the session shows the user the outcome and offers to record a confirmation. A confirmation makes the origin `user`. No later story waits for one.

**Why.**

- Recording a planning call as the user's, before the user has seen the outcome, is the mistaken claim that the product exists to stop.
- Propose, hear, then confirm is the product's own route for an agent's proposal. It also gives the user the table's second opinion before the user stands behind anything.
- The origin has an effect. A table that an agent convenes may reverse an `agent` ADR at once, and may not reverse a `user` ADR. So the offer to confirm is made in the same story, while the user is there.

**What it changes.** Spine AD-19, and Stories 1.5 and 1.6.

### 3. Stories that need the user in person

**The point.** Some stories cannot finish without the user. Is that acceptable, and how does an unattended run handle it?

**The answer.** The asks stay, because each is something only the user can give. Each is one named ask, and the story prepares everything else first. An unattended run stops at the ask and starts no story that waits on it.

| Story | What the user is asked | What waits for the answer |
| --- | --- | --- |
| 1.1 | To apply the first repository settings, or to approve the session's commands for them | The first pull request |
| 1.3 | To accept or change the wording, the kind, and the check of each standard | Stories 1.4 to 1.14 |
| 1.5, 1.6 | Whether to confirm the outcome for a record an agent proposed | Nothing |
| 1.11, 1.13 | To make the new job a required check, or to approve the command for it | Nothing. The next pull request is then held to it. |
| 1.14 | To store the secret for the evals | The plugin evals in Story 4.4 |
| 2.1, 2.2 | Only when a table would reword or reject a core law: to accept, counter, or direct | That law's ratification |
| 3.17 | To approve the first checksum | The seal, and the Avalon lint gate |
| 8.8 | To agree that the plans can be deleted | The deletion |
| 8.9 | To set the variable that allows `major` | `v1.0.0` |
| 1.4 to 2.2 | The go-ahead for a sixth stand-in sitting, if one is needed | That sitting |

For the repository settings, a design doc records the command that applies each one. An agent runs such a command only after the owner approves it, and only the owner enters the value of a secret.

**Why.**

- The wording of a standard is the user's to agree (FR-47).
- The settings act on the user's GitHub repo, and they are seen by everyone who visits it.
- The architecture requires the user's approval for the first checksum (AD-19).
- Deleting the plans and releasing 1.0 cannot be taken back.

**What it changes.** The list "Done, for every story", and Stories 1.1, 1.11, 1.13, and 1.14.

### 4. The cost of the stand-in tables

**The point.** Epics 1 and 2 take the nine core laws, about seven standards, and every architecture and delivery decision to round tables before the plugin exists. One table for each would mean dozens of tables, each with up to 15 seat runs.

**The answer.** A stand-in table hears related proposals as a slate, with a separate vote on each. Five sittings are planned:

1. The standards that are laws (Story 1.4).
2. The architecture (Story 1.5).
3. The tooling and delivery decisions (Story 1.6).
4. The writing standard (Story 2.1).
5. The other eight core laws (Story 2.2).

A chair may split a slate that is too large for one packet. A sixth sitting, and each one after it, needs the user's go-ahead first. These tables are convened at the user's direction, so the daily cap does not count them.

**Why.**

- Five sittings cost at most 75 seat runs and five chair runs, and 25 seat runs when every first round is unanimous. The chair and the Jurist run on Opus, as planned.
- A slate is already part of the process, and it keeps a vote and a ledger row for each proposal.
- The go-ahead past five mirrors the product's own default: an agent brings five matters a day on its own, and asks the user after that.

**What it changes.** Spine AD-19, and Story 1.4.

### 5. Merges before the gates exist

**The point.** The ruleset was turned on in Story 1.14, so thirteen stories would have merged with nothing enforced.

**The answer.** The ruleset comes on in stages.

- Before the first pull request: a pull request is required, merges are squash only with the pull request's title and description as the message, the three version labels exist, and private vulnerability reporting is on (Story 1.1).
- When `gates.yml` has merged: its final job is a required check, and a branch must be up to date (Story 1.11).
- When `pr.yml` has merged: its job is a required check (Story 1.13).
- Last: the secret for the evals, a check of every setting, and the drill (Story 1.14).

Until a gate exists, a pull request says which of that gate's checks its author ran by hand. Every pull request carries a version label from the first one.

**Why.**

- A required check that never reports blocks every merge, so a job cannot be required before its workflow exists. Everything else can be on from the start.
- The code of conduct in Story 1.1 sends reports to the private reporting form, so the form must be on by then.
- The first release run releases only the newest commit, so the pull requests that merged before the release workflow get no version of their own. Nothing is lost by labelling them, and the habit is in place when the check arrives.

**What it changes.** Spine AD-18 and its operations notes, the list "Done, for every story", and Stories 1.1, 1.11, 1.13, and 1.14.

## Final validation

These checks were run on 2026-11-11 by the agent that wrote the stories. A script made the counts, and the agent walked the dependencies by hand.

| Check | Result |
| --- | --- |
| Every FR is named by a story | 62 of 62 |
| Every NFR is named by a story | 5 of 5 |
| Every architecture decision is named by a story | 20 of 20 |
| Every acceptance scenario is named by a story | 45 of 45 |
| Every release gate is named by a story | SM-1, SM-2, SM-3, SM-11, and SM-12 |
| Story shape | 78 stories. Each has its user story, a Covers line, and criteria in Given, When, Then form. |
| Starter template | The architecture names none, so no story sets one up. Story 1.2 creates this repo's docs tree, as AD-19 requires. |
| Built only when needed | The git adapter gains its reads in Stories 3.3, 5.5, and 7.2. The formats arrive in Stories 3.6, 3.15, and 5.1. The fixtures arrive in Stories 4.4 and 5.8. The templates all land in Epic 2, because build step 2 is that step. |
| No story needs a later story | Walked in order. Five criteria leaned on something not yet built, and each was reworded: the version check in Story 3.4, the packet's ADRs in Story 3.10, the hook's command list in Story 4.2, the index after `scaffold` in Story 5.5, and the plugin check in Story 1.8. |
| No epic needs a later epic | Each epic uses only the epics before it. |
| File churn | Epics 3, 5, 7, and 8 each add commands to the script, and the README and the chair's file change in more than one epic. The split is kept, because the PRD fixes the build order, each epic is a release milestone, and Epic 4 puts Avalon to real use before Epics 5 to 8 are built. |

What these checks do not show:

- Whether each story is the right size for one developer agent. Stories 3.7, 4.7, 5.9, and 8.2 are the largest, and the first of them to be built is the test.
- Whether a criterion matches `tmp/SPEC.md` word for word. Each story names the scenarios it covers, and the developer reads the scenario there.
