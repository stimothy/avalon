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
