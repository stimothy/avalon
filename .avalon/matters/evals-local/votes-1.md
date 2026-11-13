# Round 1 votes (blind)

P is the Practitioner, Sk the Skeptic, J the Jurist, St the Steward, Sc the Scout. M is amend.

| Item | P | Sk | J | St | Sc | Tally |
|---|---|---|---|---|---|---|
| No workflow runs the eval suite; a contributor runs it locally | M | M | M | M | M | 0 approve, 5 amend, 0 reject |

## Amendments raised

None rewords the user's decision; each adds to the record or corrects a line it makes untrue.

- P: correct the two ADR lines; say that no check verifies a local run; record the three alternatives; the eval command is unknown.
- Sk: a scheduled or manual workflow still needs a credential; ADR-0004's gate-job line is already untrue, because one `suites` job runs four suites; add that no workflow holds a model credential.
- J: no law is broken; ADR-0003 and ADR-0004 each lose one line; the earlier contradiction in ADR-0004 is reported under LAW-000004; the gates design doc gains a statement; `CONTRIBUTING.md` gives the eval command as unknown until the suite has code.
- St: the eval command and the wording of `CONTRIBUTING.md` are unknown and must not be claimed; both ADR changelogs get an entry.
- Sc: record the three alternatives; the user's reason covers only the credential one; the others are unknown.

## Notes for the chair

The proposal said ADR-0004's line was untrue only for the eval suite. The Jurist and Skeptic show it was untrue for every suite, so the rewording names the `suites` job. ADR-0005 needs no change.
