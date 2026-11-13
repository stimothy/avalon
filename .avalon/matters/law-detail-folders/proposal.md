# Decision matter: the detail files of two laws name plan folders

Kind: amendment of two law detail files. Proposer: the planning work (origin: agent), at the user's direction to convene the table. Status: proposed; nothing is registered.

The scan of tracked files fails on a tracked file outside a short list that names a plan folder. The detail files of LAW-000014 and LAW-000015 each name `_bmad/` and `_bmad-output/`, and no law or ADR lets them. The law rows themselves, and so the laws' text, do not change.

## The amendments

### A. Amend the detail file of LAW-000014

Replace the sentence "This repo authors every git-tracked path except `_bmad/`, `_bmad-output/`, and `.claude/`." with:

> This repo authors every git-tracked path except `.claude/` and the folders that the skip list in `devtools/gates/skip_list.py` names.

### B. Amend the detail file of LAW-000015

Replace the same sentence with the same text.

The skip list is the one home of the folder names, so a change to them is made once.

Alternative: allow the two detail files to name the folders. Alternative: leave the folders named and exempt laws from the scan. Alternative: name the folders as "the plan folders" with no pointer.

Open for the table: whether a law's detail file may point to a file under `devtools/`, and whether the change leaves each law's meaning unchanged.
