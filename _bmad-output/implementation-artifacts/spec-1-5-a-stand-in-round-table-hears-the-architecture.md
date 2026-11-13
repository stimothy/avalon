---
title: 'Story 1.5: A stand-in round table hears the architecture'
type: 'feature'
created: '2026-11-12'
status: 'in-progress'
baseline_commit: '5618774b4af6954620fbe0e9e16d6a7419d910b8'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The architecture lives only in a plan that will be deleted, so the code that follows has no decision of record. Docs-only story; no code.

**Approach:** The session sorts the architecture's calls against the ADR test, states each survivor in its own words, with no plan ID or plan file name, and takes them to one stand-in sitting as a slate. A stand-in writer and editor then write `docs/adr/0001-architecture.md` from what the table adopts.

## Boundaries & Constraints

**Always:** Seats are the Practitioner, Skeptic, Jurist, Steward, and the Scout in place of the Enforcer. Opus for the chair and Jurist, Sonnet for the rest. The chair did not propose the matter. Round 1 is blind. Later rounds show every vote and reason. At most three rounds. The Skeptic argues the strongest alternative, including doing nothing. The Scout asks whether the real alternatives were considered. Tally is `N approve, N amend, N reject`, summing to five. Each decision gets its own vote and its own ledger row (`Adopted ADR-0001: ...`). Origin per decision: `user` for a call the user stated, `agent` for one the planning work reasoned. An ADR that mixes both is `agent`. The ADR has keys `adr`, `summary`, `covers`, `origin`; sections Context, Decision, Consequences, Alternatives rejected, Changelog in that order; it records the repo's form, its major parts and their boundaries, and its primary technologies; every line under Alternatives rejected has the word "Rejected"; the changelog line has date, marker, and a one-line summary. `docs/adr/README.md` lists the file. The docs follow the writing standard. Any decision the session sorts out as failing the ADR test is listed in the matter folder as a topic for a design doc once its code exists.

**Never:** Register a decision that the table would reword or reject when the user stated it, until the user answers. Cite a plan ID or plan file in any tracked file. Track the chair or seat briefs. Run a fourth round. Edit a law file other than the ledger rows this sitting earns. Settle tooling, suites, workflows, or release decisions here (Story 1.6). Carry the process or the tree-creation decisions here; they already have records.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Table adopts a decision | Last round all approve or chair adopts | Decision is in the ADR, ledger row added | N/A |
| Table rejects an agent decision | Chair rejects | Ledger row `Rejected: ...`, no ADR line | N/A |
| Table would reword or reject a user decision | User-origin decision | Nothing registered, held and reported for the user | Report with objection |
| Agent ADR after the sitting | Origin `agent` | Session shows the outcome, offers confirmation; on yes origin becomes `user`, `(user)` changelog line, ledger row decided by `user` with `none` rounds, tally, dissent | No confirmation: origin stays `agent` |

</frozen-after-approval>

## Code Map

- `_bmad-output/planning-artifacts/architecture/architecture-avalon-2026-11-11/ARCHITECTURE-SPINE.md` -- source of the calls; AD-2 to AD-14 and AD-16 are the candidates. AD-1, AD-15, AD-17, AD-18, AD-20 belong to Story 1.6 or later gates; AD-19 is the process and has its own record.
- `temporary-plans/SPEC.md` section 5 -- ADR format, markers, the ADR test, ledger format. Read only; never cited.
- `docs/adr/0002-documentation-system.md` -- model for ADR style.
- `docs/adr/README.md` -- index; add the 0001 line before 0002.
- `docs/laws/ledger.md` -- append rows only.
- `docs/design/glossary.md` -- add terms the ADR uses that it does not define (for example port, change set, hook).
- `docs/design/overview.md` -- check it stays true; update in the same change if not.
- `.avalon/matters/architecture/proposal.md` -- new matter folder: the slate, then outcomes. Same shape as `.avalon/matters/standards-laws/proposal.md`.
- `.avalon/matters/standards-adrs/proposal.md` -- the held tool-choice matter; not touched here.

## Tasks & Acceptance

**Execution:**
- [x] `.avalon/matters/architecture/proposal.md` -- write the slate in own words with origins; the chair screens it against the ADR test and the duplicate check
- [x] (no file) -- stand-in chair and five seats run up to three rounds; seats spawned by the session, briefs untracked
- [x] `docs/adr/0001-architecture.md` -- stand-in writer writes, stand-in editor edits, from the adopted decisions only
- [x] `docs/adr/README.md`, `docs/laws/ledger.md`, `docs/design/glossary.md` -- index line, one ledger row per decision, terms
- [x] `.avalon/matters/architecture/proposal.md` -- record outcomes and the sorted-out topics for design docs

**Acceptance Criteria:**
- Given the repo after the sitting, then `0001-architecture.md` has the required keys, sections, "Rejected" lines, and a dated changelog line, and the ledger tally of every row sums to five.
- Given a grep of tracked files outside `_bmad-output/`, `_bmad/`, and `temporary-plans/`, then no plan ID or plan file name appears.
- Given an agent-origin ADR, then the session offers the user the confirmation and records the answer as the matrix says.

## Implementation Notes

Implemented directly by the session, because the seats must be spawned by the session. Chair screening cut the slate to eight; round 1 split the hook from the flag, giving nine. Round 2 was 5 approve, 0 amend, 0 reject on all nine, so no third round. Decisions 2 to 8 (origin agent) are in `docs/adr/0001-architecture.md` with seven ledger rows. Decisions 1 and 9 (origin user) were reworded by the table and are held for the user; they have no ledger row, as in the standards sitting. The overview was checked and stays true. The glossary gained 14 rows. The matter folder is `.avalon/matters/architecture/`.

## Spec Change Log

## Review Triage Log

| Finding | Verdict | Route | Evidence |
|---|---|---|---|
| ADR lists "git, read-only", resting on held decision 9 | low | patch | Fixed: now "git". |
| Diagram draws the hook outside the script | low | patch | Fixed: hook is inside the script subgraph. |
| Proposal numbering differs from voted slate; candidates section stale | low | patch | Fixed: pointer to revision 2, heading marked resolved. |
| Held decisions leak through decision 4 and the Context layer sentence | false | n/a | Both sentences are decisions 2 and 4 as voted. |
| Decisions 1 and 9 have no ledger row | false | n/a | The matrix holds them; nothing is registered. |
| Alternatives mostly "reason is unknown" | false | n/a | Required by the rule that unknowns are written as unknown. |
| `covers` names a path that does not exist | false | n/a | The ADR governs the planned plugin folder. |
| Chair's final edit after the vote | false | n/a | The chair may adopt with final edits; wording only. |
| Round 2 votes lack per-seat reasons | low | not fixed | Cosmetic, matter folder only. |
| Glossary verified stamp unchanged | low | defer | Stamp is the script's to write (verify command). |

## Design Notes

Slate, in own words (the chair may split or merge): (1) judgment lives in prompts and mechanics in one script that never calls a model, in three layers: skills, agents, script [user and agent]; (2) the script is one entry file with a package beside it, standard library only, Python 3.9 floor, no network [agent]; (3) a pure core with files, git, and the clock behind ports [agent]; (4) a command is one all-or-nothing change set under a lock [agent]; (5) each file format has one home, fixed text has one template, each file has one writer [agent]; (6) a hook guards the record, and the user's authority is a flag no pre-approval covers [agent]; (7) one read-only git module, and nothing writes git [user]; (8) the plugin folder holds only what a user installs [agent]. Candidates for screening out as design-doc material: the config and root resolver, the closed command interface, where each prompt text lives, work in progress as a matter folder.

## Verification

**Manual checks (if no CLI):**
- `grep -rEn "\b(REQ|AC|FR|NFR|OQ|SM|UJ|AD)-[0-9]+" docs .avalon README.md` -- expected: no output.
- Read the ledger rows and ADR frontmatter against the Always list.
