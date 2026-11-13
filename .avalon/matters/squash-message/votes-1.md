# Round 1 votes (blind)

P is the Practitioner, Sk the Skeptic, J the Jurist, St the Steward, Sc the Scout. M is amend.

| Item | P | Sk | J | St | Sc | Tally |
|---|---|---|---|---|---|---|
| The squash message is the pull request's title alone | M | M | M | M | M | 0 approve, 5 amend, 0 reject |

## Amendments raised

None rewords the user's decision; each adds to the record.

- P: the ruleset bullet says the title alone, with no body; a changelog line (user, table); the design doc is corrected in the same change if it is untrue.
- Sk: doing nothing is weakest, because ADR-0005 is untrue now; the body scan stays; its reason is unknown unless the user gives one.
- J: ADR-0005 owns the decision and no law or other ADR is contradicted; line 76 is the only untrue text; the proposal wrongly said a doc gives "permanent" as the reason for the body scan, so that statement is corrected to unknown; add "Rejected: the pull request's title and description as the squash message"; add a changelog entry.
- St: record that the body is not in git history; state unknowns as unknown; add a changelog line; no gate checks the setting.
- Sc: add the rejected alternative; keep the default-message rejection as unknown; mark the reason for scanning the body as unknown unless the user has said it.

## Notes for the chair

The proposal's claim about a "permanent" reason was wrong; the chair checked, and the Jurist is right (LAW-000006). `docs/design/gates-workflow.md` says nothing about squash content, so it needs no change.
