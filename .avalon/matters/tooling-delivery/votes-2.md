# Round 2 votes

Items and seat letters are as in `votes-1.md`. Every seat saw every round 1 vote and reason, and voted on `revision-1.md`.

| Item | P | Sk | J | St | Sc | Tally |
|---|---|---|---|---|---|---|
| 1. Development tools | A | A | A | A | A | 5 approve, 0 amend, 0 reject |
| 2. Lock file | A | A | A | A | A | 5 approve, 0 amend, 0 reject |
| Held law | A | A | A | A | A | 5 approve, 0 amend, 0 reject |
| 3. Suites | A | A | A | M | A | 4 approve, 1 amend, 0 reject |
| 4. No logic in workflows | A | M | M | A | A | 3 approve, 2 amend, 0 reject |
| 5. Gates on ready pull requests | A | A | M | A | A | 4 approve, 1 amend, 0 reject |
| 6. Two workflows, one verdict job | A | A | A | A | A | 5 approve, 0 amend, 0 reject |
| 7. Ruleset | A | A | M | A | A | 4 approve, 1 amend, 0 reject |
| 8. Release by label | A | A | A | A | A | 5 approve, 0 amend, 0 reject |
| 9. Release workflow | A | M | M | A | A | 3 approve, 2 amend, 0 reject |

## Amendments raised

- 3 (St): the real GitHub adapter takes its HTTP transport as a port, every suite fakes the transport, so no suite reaches GitHub and the adapter's lines run under test. Replaces "No suite runs the real GitHub adapter." The Steward would otherwise vote reject on items 1 and 3, because uncovered lines break the coverage law.
- 4 (Sk, J): the gate fails an `if:` of any other form, an action not pinned to a full SHA, a workflow with no stated permissions, a write permission outside the job in `release.yml`, and a locked tool installed any way but from the lock file.
- 5 (J): restore the user's own wording, with no `pr.yml` sentence and with "a newer push cancels the older run". Move the `pr.yml` events and the cancelling of a newer run to decision 6.
- 7 (J): require the title-and-body scan of `pr.yml` as well as the label check.
- 9 (Sk, J): "While no version exists or the latest version is below 1.0.0" and "a repeated run creates no version that already exists".
- Notes (J): the Jurist's remark that the eval suite reaches a model means the line "No suite may reach the network" must not reach any ADR. Each suite's coverage collection excludes the evals.
