# Round 1 votes (blind)

P is the Practitioner, Sk the Skeptic, J the Jurist, St the Steward, Sc the Scout. M is amend.

| Item | P | Sk | J | St | Sc | Tally |
|---|---|---|---|---|---|---|
| A. Amend the detail file of LAW-000014 | M | M | M | M | M | 0 approve, 5 amend, 0 reject |
| B. Amend the detail file of LAW-000015 | M | M | M | M | M | 0 approve, 5 amend, 0 reject |

## Amendments raised

- All five: the skip list holds three folders, including a third plan folder, which the old sentences never named. The change widens the exemption of both laws, and the record must say so.
- P: name the constant: "...the plan folders that `PLAN_FOLDERS` in `devtools/gates/skip_list.py` lists." Either add `.claude/` to the skip list or record why it is exempt elsewhere, because the exemption splits across two homes. Confirm that the third folder is meant to be exempt.
- Sk: use the same wording, and record the extension to the third folder. Or decide that a law's scope may not depend on code, and exempt the two detail files in the skip list instead.
- J: add "A change to `PLAN_FOLDERS` changes the scope of this law and goes to a round table before it merges." A pointer from a detail file into code is not barred. The change needs its own ledger row.
- St: "...except `.claude/` and the plan folders listed in `devtools/gates/skip_list.py`; that file is the one home of those folder names." Confirm the skip list holds only plan folders (it also holds lock files).
- Sc: pointing a law at code lets an ordinary edit change its scope with no round table (LAW-000003). Argue the simplest alternative: add the two detail files to `MAY_NAME_A_PLAN_FOLDER`, which needs no law change. If A and B stand, name the four folders in the sentence and have the skip list cite the law.

## Notes for the chair

The two detail files are tracked docs, and the scan fails them as they stand. Decide between pointing to the constant and the alternatives. Unknowns are written as unknown.
