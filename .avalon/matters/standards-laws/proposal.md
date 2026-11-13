# Law matter: engineering standards

Kind: law matter, one slate, seven proposals. Proposer: the user. Status: held for a round table; nothing is registered.
Each proposal gets its own vote. Scope `code` is on the scope list, added with the user's agreement.
A stand-in chair and five stand-in seats settled the kind and wording of each standard in a pre-sitting of three rounds, unanimous at the end. The registering sitting hears these texts again, and the user decides.

| # | Scope | Origin | Proposed law | Check |
|---|---|---|---|---|
| 1 | code | user | Every test has exactly one Act, with all of its setup before the Act and all of its assertions after it. | The law-reviewer reads the tests a change touches. |
| 2 | code | user | Every test belongs to exactly one suite: unit, integration, end-to-end, contract, or eval. Unit tests and integration tests run apart. | Each suite is its own gate job, and a gate fails any test in no suite. |
| 3 | code | user | A unit test touches no file system, subprocess, or network, and the whole unit run finishes within the wall-clock budget set by the test-layout ADR. | A gate blocks those calls and times the unit run. |
| 4 | code | user | No unit, integration, or end-to-end test uses git or the network. | A blocking fixture fails any such test that starts git or opens a connection. |
| 5 | code | user | Tests cover at least 80% of the Python this repo authors, tests excluded. | A gate fails below 80%. |
| 6 | code | user | Python this repo authors passes the repo's linter, formatter, and type checker, which the tool-choice ADR names. | Gates run each tool. |
| 7 | code | user | No directory this repo authors is named utils, helpers, misc, common, or tmp. | A gate matches directory names, case-insensitive, at any depth. |

## Shared definition (detail for proposals 5, 6, and 7)

This repo authors every path except those fixed by outside tools: `_bmad/`, `_bmad-output/`, and `.claude/`.

## Detail for proposal 1

Fixtures and parametrization count as Arrange. A `pytest.raises` block that wraps the Act counts as Act plus Assert.

## Detail for proposal 3

The gate must not block the file access that pytest itself makes for temp files, its cache, and imports. The test-layout ADR lists the blocked calls and holds the budget, which defaults to 10 seconds.

## Detail for proposal 4

The contract tests and the plugin evals are suites outside the unit, integration, and end-to-end kinds, so the law needs no exception clause. The contract tests start git in a throwaway repo, use no network, and never touch this repo's own git state.

## Detail for proposal 5

The detail names the tests directory as excluded.

## Note on proposal 7

The plan folder was named `tmp`, a name the law forbids. It is renamed `temporary-plans`, so the law holds on adoption.

## Raised for a separate matter

markdownlint is not part of this slate. It is a docs-scope proposal, checked against the writing standard, for a later sitting.

## Standards that became guidelines

Test-driven development, "a unit test replaces everything outside its unit with a fake", weighing CPU time and memory, DRY and SOLID, and "every file in a directory serves its directory's purpose" are guidelines, held in `docs/design/engineering-standards.md`.
