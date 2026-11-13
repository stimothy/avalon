# Contributing

Read the [code of conduct](CODE_OF_CONDUCT.md) and the [overview](docs/design/overview.md) first. Write tests first.

## Set up

You need [uv](https://docs.astral.sh/uv/) and Node. Run each command from the top of the repo:

```sh
uv sync
npm ci
```

`uv sync` creates `.venv`, which git ignores, and installs the Python tools at the versions in `uv.lock`. `npm ci` installs the markdown lint at the version in `package-lock.json`. Nothing under `plugin/` needs either.

## Run the test suites

Each suite runs alone with one command. `uv run pytest` with no argument collects from `tests/` only.

| Suite | Command |
|---|---|
| Unit | `uv run pytest tests/unit` |
| Integration | `uv run pytest tests/integration` |
| End-to-end | `uv run pytest tests/e2e` |
| Contract | `uv run pytest tests/contract` |

The unit, integration, and end-to-end suites share one guard that fails a test that starts a process or opens a network connection. The contract suite is outside it. A unit run that takes longer than 10 seconds fails.

To run a suite on another Python, add `--python`, for example `uv run --python 3.9 pytest tests/unit`.

## Measure coverage

Coverage counts the unit and integration runs together, over `plugin/script/` and `devtools/`. A result below 80 fails.

```sh
uv run coverage run -m pytest tests/unit
uv run coverage run -m pytest tests/integration
uv run coverage combine
uv run coverage report
```

## Check the code and the docs

| Check | Command |
|---|---|
| Linter | `uv run ruff check` |
| Formatter | `uv run ruff format --check` |
| Type checker | `uv run mypy` |
| Markdown lint | `npx markdownlint-cli2` |
