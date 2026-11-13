# Ledger

Every round-table decision and every confirmation by the user, one row each.

| Date | Decision | Proposed by | Decided by | Rounds | Tally | Dissent |
|---|---|---|---|---|---|---|
| 2026-11-12 | Added LAW-000010 | user | table | 3 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Added LAW-000011 | user | table | 3 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Added LAW-000012 | user | table | 3 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Added LAW-000013 | user | table | 3 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Added LAW-000014 | user | table | 3 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Added LAW-000015 | user | table | 3 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: a plugin of three layers in a self-contained folder | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: the script is Python on the standard library only | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: a pure core, with files, git, and the clock behind ports | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: a writing command is one all-or-nothing change set | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: one home for each format, one writer for each file | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: a hook guards the record | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: the user's authority is one leading flag | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: judgment in prompts, mechanics in one script | user | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0001: one module reads git, and nothing writes it | user | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Confirmed ADR-0001 | agent | user | none | none | none |
| 2026-11-12 | Adopted ADR-0003: pytest, coverage, ruff, and mypy, configured in one pyproject.toml | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0003: the lock file is the only home of a tool version | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0004: each suite has a folder and a fixed reach | agent | table | 2 | 4 approve, 1 amend, 0 reject | St: the GitHub adapter takes its HTTP transport as a port that every suite fakes, so its lines run under test |
| 2026-11-12 | Adopted ADR-0005: workflows hold no logic | agent | table | 2 | 3 approve, 2 amend, 0 reject | Sk, J: the gate must name every failure it checks: `if:` forms, SHA pins, permissions, writes, and lock-file installs |
| 2026-11-12 | Adopted ADR-0005: gates run only on a pull request that is ready for review | user | table | 2 | 4 approve, 1 amend, 0 reject | J: keep the user's wording; move the pr.yml events and the newer-run cancel to decision 6 |
| 2026-11-12 | Adopted ADR-0005: two workflows gate a pull request, and one job gives the verdict | agent | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0005: a ruleset protects master | agent | table | 2 | 4 approve, 1 amend, 0 reject | J: require the title-and-body scan of pr.yml as well as the label check |
| 2026-11-12 | Adopted ADR-0006: a release is chosen by a label | user | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Adopted ADR-0006: one workflow releases, catches up, and writes nothing else | agent | table | 2 | 3 approve, 2 amend, 0 reject | Sk, J: cover the case of no version yet, and say a repeated run creates no version that already exists |
| 2026-11-12 | Added LAW-000016 | user | table | 2 | 5 approve, 0 amend, 0 reject | none |
| 2026-11-12 | Confirmed ADR-0003 | agent | user | none | none | none |
| 2026-11-12 | Confirmed ADR-0004 | agent | user | none | none | none |
| 2026-11-12 | Confirmed ADR-0005 | agent | user | none | none | none |
| 2026-11-12 | Confirmed ADR-0006 | agent | user | none | none | none |
| 2026-11-12 | Amended LAW-000016 as LAW-000017 | user | table | 1 | 2 approve, 3 amend, 0 reject | Sk, St, Sc: reword the law text (held for the user); all seats: state what "a check" covers, in a detail file |
| 2026-11-12 | Amended ADR-0006: a none label releases nothing | user | table | 1 | 3 approve, 2 amend, 0 reject | J: the Context must name the user's parts; Sc: add rejected alternatives, and say whether `none` may mark a change to `plugin/**` |
| 2026-11-12 | Amended ADR-0006: the label check refuses major below 1.0.0 | user | table | 1 | 2 approve, 3 amend, 0 reject | J: say no check can stop the merge, and ask the user to confirm the release code's refusal stays; St: one combined sentence (held for the user); Sc: use the same GitHub port |
| 2026-11-12 | Amended LAW-000017 as LAW-000018 | user | user | none | none | none |
| 2026-11-12 | Reworded ADR-0006: one sentence for the refusal of major | user | user | none | none | none |
| 2026-11-13 | Amended LAW-000014 detail: the excluded plan folders are those `PLAN_FOLDERS` lists, which adds a third plan folder | agent | table | 1 | 0 approve, 5 amend, 0 reject | P: name the constant, settle where `.claude/` lives, confirm the third folder; Sk: record the wider scope; J: a change to `PLAN_FOLDERS` goes to a table; St: only plan folders are exempt, not lock files; Sc: a pointer into code lets an edit change scope (declined: add the detail files to the allow list) |
| 2026-11-13 | Amended LAW-000015 detail: the excluded plan folders are those `PLAN_FOLDERS` lists, which adds a third plan folder | agent | table | 1 | 0 approve, 5 amend, 0 reject | P: name the constant, settle where `.claude/` lives, confirm the third folder; Sk: record the wider scope; J: a change to `PLAN_FOLDERS` goes to a table; St: only plan folders are exempt, not lock files; Sc: a pointer into code lets an edit change scope (declined: add the detail files to the allow list) |
| 2026-11-13 | Amended ADR-0005: the secret scan is done by gitleaks | user | table | 1 | 0 approve, 5 amend, 0 reject | P: one version home, install by checksum, tracked files only, a clear message when missing, the same gate locally and in CI; Sk: GitHub scanning cannot fail a local run; J: ADR-0005 owns it with a cross-reference in ADR-0003, and the workflow gate fails any other install; St: the version home is unknown until the workflow is written, and the alternatives are recorded; Sc: give the reasons the seats can state (git-secrets declined) |
