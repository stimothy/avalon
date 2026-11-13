---
title: 'Story 1.4: A stand-in round table hears the standards that are laws'
type: 'feature'
created: '2026-11-12'
status: 'in-review'
baseline_commit: 'c9c4fd9'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The seven law proposals from Story 1.3 are held, unregistered, so no engineering standard binds yet.

**Approach:** A stand-in chair (Opus) runs one sitting on the seven proposals as one slate. Five stand-in seats (Practitioner, Skeptic, Jurist, Steward, Enforcer) vote in parallel and blind, at most three rounds. The chair decides each proposal and records the outcome by hand in the registry and the ledger.

## Boundaries & Constraints

**Always:** Docs only. Seats: Opus for the Jurist, Sonnet for the rest. Round 1 votes are blind. A later round shows every seat every vote and reason. Tally is `N approve, N amend, N reject`, summing to five. New IDs follow LAW-000009, origin `user`. Each proposal gets its own vote and ledger row.

**Never:** Register anything the table would reword or reject without the user's decision; hold such a proposal and report it. Track the chair or seat briefs in any file. Edit a law by any path other than this hand-run table. Run a fourth round.

## Decisions

- A user proposal that the table rewords or rejects stays unregistered and is reported for the user to accept, counter, or direct as written.
- Seats are spawned by the session; the chair is a separate Opus subagent that screens, revises, and decides.

</frozen-after-approval>

## Code Map

- `.avalon/matters/standards-laws/proposal.md` -- the slate (7 proposals) and detail notes.
- `docs/laws/LAWS.md` -- registry; append rows after LAW-000009 only.
- `docs/laws/ledger.md` -- one row per decision.
- `docs/laws/LAW-<id>.md` -- detail files only where a law has detail (proposals 1, 3, 4, 5 carry detail notes).
- `.avalon.yml` -- `law_max_chars: 200`, `registry_max_laws: 100`.

## Tasks & Acceptance

- [x] Screen the slate, then run rounds with five seats
- [x] `docs/laws/LAWS.md`, `docs/laws/ledger.md`, detail files -- record adopted laws and every decision
- [x] Held proposals -- left unregistered and reported

**Acceptance:** Given the repo, then registry rows are in ID order with next IDs after LAW-000009, each ledger tally sums to five, and no tracked file holds a brief.

## Implementation Notes

The ledger records decisions; `docs/laws/` is edited by hand here because the law skill does not exist yet (Story 1.4 is the stand-in for it).

## Outcome

Three rounds; the last round was 5 approve, 0 amend, 0 reject on all seven. LAW-000010 (proposal 1, the user's wording) was registered. The user then accepted the table's wording for proposals 2, 3, 4, 5, and 7, registered as LAW-000011 to LAW-000015. Proposal 6 waits for the tool-choice ADR (Story 1.6) and is held in the matter folder. No ledger row exists for a held proposal.
