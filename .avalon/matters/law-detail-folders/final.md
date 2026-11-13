# Final: the plan folder names in two law detail files

Chair: stand-in. The chair did not propose this matter. Status: decided in round 1, applied, and confirmed by the user. Origin: agent, confirmed by the user.

All five seats voted amend (0 approve, 5 amend, 0 reject). The table decides with no round 2.

## The decision

Amend the detail files of LAW-000014 and LAW-000015. Each points to `PLAN_FOLDERS` in the skip list instead of naming the folders, and each adds a guard: a change to `PLAN_FOLDERS` changes the scope of the law and goes to a round table before it merges. The law rows do not change.

- Both laws now also exclude a third plan folder. The table finds this acceptable, and the user must confirm it.
- `.claude/` stays named in the sentence. It is not a plan folder, so it does not belong in `PLAN_FOLDERS`.
- The lock files give no exemption from either law.
- Declined: adding the two detail files to the allow list of the scan.
- The guard is a written rule. No gate enforces it, and whether one should is unknown.

## Applied

`docs/laws/LAW-000014.md`, `docs/laws/LAW-000015.md`, and two rows in `docs/laws/ledger.md`.
