# Final: the evals run locally

Chair: stand-in. The chair did not propose this matter. Status: decided in round 1 and applied.

The table decides with no round 2. All five seats voted amend, every amendment adds to the record or corrects a line, and none rewords the user's decision.

## The decision

Amend ADR-0003 and ADR-0004: no workflow runs the eval suite or calls a model, and a contributor runs it locally before a push (origin: user).

Tally: 0 approve, 5 amend, 0 reject. Adopted with the user's wording.

- ADR-0004 owns the suite rule; ADR-0003 loses its reference to an eval job. No law and no other ADR is contradicted.
- ADR-0004's line "Each suite is its own gate job" was already untrue, because one `suites` job runs four suites. The rewording corrects it.
- Three alternatives are recorded as rejected. The user's reason is given only for the credential one.
- Nothing checks that the evals were run. The eval command and the contributor guide's wording are unknown until the suite has code.
- Declined: a change to ADR-0005. The Jurist found it holds nothing about evals.

## Applied

`docs/adr/0003-development-tools.md`, `docs/adr/0004-test-suites.md`, `docs/design/gates-workflow.md`, and one row in `docs/laws/ledger.md`.
