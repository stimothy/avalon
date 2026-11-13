---
title: 'Story 1.6: A stand-in round table hears the tooling and delivery decisions'
type: 'feature'
created: '2026-11-12'
status: 'done'
baseline_commit: '604b974e418b72f0fd127f120a14b442fc3822e9'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The decisions behind the dev tools, the five test suites, the two pull request workflows, and the release by label live only in plans that will be deleted. The law held in Story 1.4 names a tool-choice ADR that does not exist. Docs-only story; no code.

**Approach:** The session sorts these calls against the ADR test, states each survivor in its own words (no plan ID, no plan file name), and takes them to one stand-in sitting as a slate. Stand-in writer and editor record what the table adopts, extending an ADR that owns the topic or adding the next number. The held law goes to the same sitting.

## Boundaries & Constraints

**Always:** Seats are the Practitioner, Skeptic, Jurist, Steward, and the Scout in place of the Enforcer. Opus for the chair and Jurist, Sonnet for the rest. The chair did not propose the matter. Round 1 is blind; later rounds show every vote and reason; at most three rounds. The Skeptic argues the strongest alternative, including doing nothing; the Scout asks whether the real alternatives were considered. Tally is `N approve, N amend, N reject`, summing to five. Each decision gets its own vote and ledger row (`Adopted ADR-NNNN: ...`). Origin is `user` for a call the user stated (gates only on a pull request ready for review; release chosen by a label; the suite rules in LAW-000010 to LAW-000015) and `agent` for one the planning work reasoned (for example a contract suite that starts git); an ADR that mixes both is `agent`. A failed ADR test becomes a guideline in `docs/design/engineering-standards.md`. Each ADR has keys `adr`, `summary`, `covers`, `origin`; sections Context, Decision, Consequences, Alternatives rejected, Changelog in that order; every Alternatives line has the word "Rejected"; the changelog line has date, marker, one-line summary. The tool-choice ADR names each tool and its purpose and states no version; the lock file is the only home of versions. `docs/adr/README.md` lists every ADR. The held law goes to the table in the same sitting as the user's proposal, and is registered with the next law ID (LAW-000016) only if adopted; the matter folder `.avalon/matters/standards-laws/` is then removed. The docs follow the writing standard. Agent-origin ADRs are offered to the user for confirmation as in Story 1.5.

**Never:** Register a decision the table would reword or reject when the user stated it, until the user answers. Cite a plan ID or plan file in any tracked file. Track the chair or seat briefs. Run a fourth round. Edit a law file beyond the registry row, ledger rows, and detail file this sitting earns. Rewrite ADR-0001 or ADR-0002 beyond a change the table adopts. Write code, workflows, or `pyproject.toml`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Table adopts a decision | Last round all approve or chair adopts | In an ADR, ledger row added | N/A |
| Table rejects an agent decision | Chair rejects | Ledger row `Rejected: ...`, no ADR line | N/A |
| Table would reword or reject a user decision | User-origin | Nothing registered; held and reported with the objection | Report |
| Tool-choice ADR adopted | Held law, 5-0-0 earlier | Law heard same sitting; LAW-000016 registered if adopted, matter folder removed | If rejected: ledger row, folder still removed |
| Agent ADR after sitting | Origin `agent` | Outcome shown, confirmation offered; yes gives origin `user`, `(user)` changelog line, ledger row decided by `user` with `none` | No answer: stays `agent` |

</frozen-after-approval>

## Code Map

- `_bmad-output/planning-artifacts/architecture/architecture-avalon-2026-11-11/ARCHITECTURE-SPINE.md` -- source of the calls: the suites, the plugin-folder rule, workflows that hold no logic, the two PR workflows and ruleset, the release workflow, and the Stack (tool names only).
- `.avalon/matters/standards-adrs/proposal.md` -- held test-layout and tool-choice matter; reuse its wording.
- `.avalon/matters/standards-laws/proposal.md` -- holds the law to hear; folder removed at the end.
- `.avalon/matters/architecture/` -- model for matter-folder shape (proposal, revisions, votes).
- `docs/adr/0001-architecture.md`, `0002-documentation-system.md`, `README.md` -- style model and index; ADR-0001 owns architecture only, so expect new ADRs.
- `docs/laws/LAWS.md`, `ledger.md`, `LAW-0000NN.md` -- registry row, ledger rows, optional detail file.
- `docs/design/engineering-standards.md`, `glossary.md`, `overview.md` -- guideline home for failed calls; new terms; keep overview true.

## Tasks & Acceptance

**Execution:**
- [x] `.avalon/matters/tooling-delivery/proposal.md` -- write the slate in own words with origins; chair screens against the ADR test and duplicates; include the held law
- [x] (no file) -- stand-in chair and five seats run up to three rounds; briefs untracked
- [x] `docs/adr/` -- stand-in writer and editor write or extend ADRs from adopted decisions only; update `README.md`
- [x] `docs/laws/` -- ledger row per decision; if adopted, LAW-000016 in `LAWS.md` (and detail file if needed)
- [x] `docs/design/engineering-standards.md`, `glossary.md`, `overview.md` -- guidelines for failed calls, new terms, truth check
- [x] `.avalon/matters/standards-laws/`, `standards-adrs/` -- remove once registered or rejected; record outcomes in the new matter

**Acceptance Criteria:**
- Given the repo after the sitting, then every ADR has the required keys, sections, "Rejected" lines, and dated changelog line, and every ledger tally sums to five.
- Given a grep of tracked files outside `_bmad-output/`, `_bmad/`, and `temporary-plans/`, then no plan ID or plan file name appears.
- Given the ledger, then every law and ADR except the nine draft core laws and ADR-0002 has a row showing a table's decision or the user's.
- Given the tool-choice ADR, then it holds no tool version.

## Implementation Notes

Implemented directly by the session, because the seats must be spawned by the session. The chair kept all nine decisions and grouped them into ADR-0003 (tools), ADR-0004 (suites), ADR-0005 (workflows and gates), and ADR-0006 (releases). Round 1 had amends on most items and no rejects; round 2 had amends on decisions 3, 4, 5, 7, and 9, all wording, so the chair adopted with no round 3. Nine ledger rows were added. The table reworded the user's held law, so LAW-000016 is NOT registered and `.avalon/matters/standards-laws/` stays; the user must accept the table's wording (in `.avalon/matters/tooling-delivery/final.md`). The user's decisions 5 and 8 were adopted in the user's own words. Three proposals are held for the user: a suppressions bar, a `none` label, and refusing `major` below 1.0.0 at the label check. Staged required checks became a guideline. Afterward the user accepted the table's wording and confirmed the ADRs: LAW-000016 is registered, the standards-laws matter folder is removed, ADR-0003 to ADR-0006 have origin `user` with `(user)` changelog lines, and the ledger has five more rows. The three held proposals still need a table.

## Spec Change Log

## Review Triage Log

| Finding | Verdict | Route | Evidence |
|---|---|---|---|
| Final job runs on a draft under `always()` | medium | patch | Fixed: ADR-0005 says the final job joins `always()` with the draft test. |
| final.md says the held law is adopted and nothing registered | medium | patch | Fixed: status, ruling, and pending ledger row reworded. |
| First release run starts at a commit that may lack a label; no concurrency guard | medium | defer | Table adopted no wording; logged in deferred-work.md. |
| Design doc stamps not refreshed | low | defer | Stamp is the script's to write; already deferred from Story 1.5. |
| "more commits" differs from the user's "new commits" | low | not fixed | The writing standard bars "new" outside a changelog; meaning unchanged. |
| Cancel-older-run stated in decisions 5 and 6 | low | not fixed | Decision 5 keeps the user's words; decision 6 generalises. |
| ADR-0006 gaps (first version number, PR lookup, variable name) | low | not fixed | Unknowns are written as unknown by rule; later stories decide. |
| ADR-0004 omits folder names, ADR-0003 omits Python version | false | n/a | Not decisions the table heard; the layout lands in Story 1.7. |
| Ruleset unverifiable, staged checks only in the design doc | false | n/a | ADR-0005 states it is set by hand and unchecked; staging is a failed ADR test. |
| Edge cases on step-level `if:`, unblock route, `major` version number | low | not fixed | Beyond the adopted wording; no harm shown. |

## Verification

**Manual checks (if no CLI):**
- `grep -rEn "\b(REQ|AC|FR|NFR|OQ|SM|UJ|AD)-[0-9]+" docs .avalon README.md` -- expected: no output.
- Read ledger rows and ADR frontmatter against the Always list; confirm `.avalon/matters/standards-laws/` is gone.
