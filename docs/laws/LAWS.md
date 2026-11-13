# Laws

Every law in this table is binding. Read the whole table before any work.
Open a detail file only when the one-line law is not enough to act on.

| ID | Scope | Origin | Law | Detail |
|---|---|---|---|---|
| LAW-000001 | all | core | Nothing in this repo may contradict a law in this table. | |
| LAW-000002 | all | core | Precedence is laws, then ADRs, then the work, then design docs; when two disagree, the lower one is corrected or the higher one is changed through its own process. | |
| LAW-000003 | laws | core | A law is created, amended, or removed only by a round table. | |
| LAW-000004 | all | core | A contradiction, or a request that would break a law or an ADR, is reported with its ID and never silently resolved or worked around. | |
| LAW-000005 | docs | core | Docs state only what is true now; replaced content is removed, and history lives in ADR changelogs, the law archive, the ledger, and git. | |
| LAW-000006 | docs | core | Docs state only what the repo shows or the user has said; unknowns are written as unknown. | |
| LAW-000007 | adr | core | After install, a decision that meets the ADR test goes to the round table before it is carried out, and is recorded in an ADR when it is adopted. | |
| LAW-000008 | design | core | A change that makes a design doc untrue updates that doc in the same change. | |
| LAW-000009 | docs | core | Every doc follows the writing standard. | [more](LAW-000009.md) |
| LAW-000010 | code | user | Every test has exactly one Act, with all of its setup before the Act and all of its assertions after it. | [more](LAW-000010.md) |
| LAW-000011 | code | user | Every test belongs to exactly one suite (unit, integration, end-to-end, contract, or eval), and each suite runs separately from the others. | |
| LAW-000012 | code | user | A unit test touches no file system, subprocess, or network beyond pytest's own import and cache access, and the whole unit run finishes within 10 seconds. | [more](LAW-000012.md) |
| LAW-000013 | code | user | No integration or end-to-end test uses git or the network. | [more](LAW-000013.md) |
| LAW-000014 | code | user | Tests cover at least 80% of the lines of Python this repo authors, tests excluded. | [more](LAW-000014.md) |
| LAW-000015 | code | user | No directory this repo authors is named utils, helpers, misc, common, or tmp, in any letter case. | [more](LAW-000015.md) |
| LAW-000018 | code | user | Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and no check is turned off outside `pyproject.toml`. | [more](LAW-000018.md) |
