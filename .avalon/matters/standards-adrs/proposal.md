# Decision matter: test layout and tool choice

Kind: decision matter, one slate, two proposals. Proposer: the planning work reasoned the specifics from the user's rules, so the user is offered the outcome to confirm. Status: held for a round table; nothing is registered.

## 1. Test layout

- Decision: every test sits in one of five suites: unit, integration, end-to-end, contract, or eval. A test's directory sets its suite.
- Contract tests (real git in a throwaway repo) and plugin evals (need a model and the network) are outside the unit, integration, and end-to-end kinds.
- Integration tests may use the file system. Every read of git sits behind one boundary that the three kinds replace with a fake and the contract tests prove against real git.
- The unit run has a wall-clock budget, 10 seconds by default. The ADR lists the calls the unit gate blocks: file system, subprocess, and network, apart from pytest's own temp, cache, and import access.
- Check: each suite is its own gate job.

## 2. Tool choice

- Decision: `pytest` runs tests, `coverage` measures them, `ruff` lints and formats, and `mypy` checks types. Configuration lives at the repo root, in `pyproject.toml`.
- Method: line coverage, with unit and integration tests counted together. The 80% floor and the scope of authored Python are in the law, not here.
- Check: gates run each tool.
