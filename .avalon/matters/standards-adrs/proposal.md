# Decision matter: test layout and tool choice

Kind: decision matter, one slate, two proposals. Proposer: the user stated the rules; the planning work reasoned the specifics, so the user is offered the outcome to confirm. Status: held for a round table; nothing is registered.

## 1. Test layout

- Decision: tests live in suites that run apart. Unit tests, integration tests, and end-to-end tests are the three kinds. Contract tests (real git in a throwaway repo) and plugin evals (need a model and the network) are separate suites outside the three kinds.
- Integration tests reach the file system, because git is the script's only other outside dependency.
- Every read of git sits behind one boundary. The three kinds replace it with a fake; the contract tests prove it against real git.
- Check: gates run each suite as its own job.

## 2. Tool choice

- Decision: `pytest` runs tests, `coverage` measures them, `ruff` lints and formats, `mypy` checks types, and `markdownlint` checks markdown.
- Unit and integration tests count together toward the 80% floor, over all Python in the repo except the tests.
- Check: gates run each tool.
