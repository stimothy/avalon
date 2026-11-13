# Law matter: engineering standards

Kind: law matter, one slate, seven proposals. Proposer: the user. Status: held for a round table; nothing is registered.
Each proposal gets its own vote. Scope `code` is proposed for addition to the scope list, which the user agreed to.

| # | Scope | Origin | Proposed law | Check |
|---|---|---|---|---|
| 1 | code | user | Every test has three parts, in order: Arrange, Act, Assert. | The law-reviewer reads each test. |
| 2 | code | user | Every test is a unit, integration, or end-to-end test, and unit tests and integration tests run apart. | Each kind runs as its own gate job. |
| 3 | code | user | A unit test replaces everything but its unit with a mock and runs fast, and the whole unit run stays within its time budget. | A gate fails when the unit run passes the budget; the default budget is 10 seconds. |
| 4 | code | user | No unit, integration, or end-to-end test uses git or the network. | A gate fails any such test that starts git or opens a network connection. |
| 5 | code | user | Tests cover at least 80% of the repo's Python, tests excluded. | A gate fails below 80%. |
| 6 | code | user | Code passes the repo's linter, formatter, and type checker. | Gates run each tool. |
| 7 | code | user | No directory is a grab bag: its name states one purpose and every file in it serves that purpose, except where the docs layout or the plugin layout fixes it. | The law-reviewer, using the detail below. |

## Detail for proposal 7

A directory is a grab bag when its name states no single purpose, such as `utils`, `helpers`, `misc`, or `common`, or when its files do not all serve the purpose its name states. When a directory becomes a grab bag, its files are grouped into subdirectories.

Two layouts are fixed and exempt: the docs tree (`laws`, `adr`, and `design` hold their files flat) and the plugin's `agents` folder (a subfolder would become part of an agent's name).

## Detail for proposal 4

The contract tests and the plugin evals are separate suites outside the three kinds, so the law needs no exception clause. The contract tests start git in a throwaway repo, use no network, and never touch this repo's own git state.
