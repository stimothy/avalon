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

The eval suite reaches Claude Code and a model. No workflow runs it and no workflow calls a model, so run it on your own machine, with your own Claude Code login, before you push. Its command is unknown until the suite has code.

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

## Propose a change

1. Open an issue with the bug or proposal template, or go straight to a pull request.
2. Branch from `master`, write the tests first, and run the suites and the checks above on your machine.
3. Open a draft pull request. A draft runs no gate.
4. Mark it ready for review. The gates run, and a new push cancels the run in progress.
5. Fix what a gate or a reviewer reports. A merge squashes the branch into one commit whose message is the pull request's title.

The pull request template asks for the checks you ran.

## The gates and the version labels

`gates.yml` checks the code and the docs, and `pr.yml` checks the pull request itself. [The gates workflow](docs/design/gates-workflow.md) lists the jobs and the check that `master` requires.

Each pull request carries exactly one of the labels `major`, `minor`, `patch`, and `none`, and the label decides the version that its merge releases. A maintainer sets the label, so a contributor does not. [The release code](docs/design/release.md) says how the label is read and when `major` is refused.

## Change a law or an ADR

The laws and the ADRs change only through a round table. The round table hears your proposal in your own session, and the pull request carries the row that records the decision in `docs/laws/ledger.md`. A maintainer's merge decides whether the change stands.

## Licence

A contribution is accepted under the [MIT licence](LICENSE).

## Where the rules are

The binding rules are in [the registry of laws](docs/laws/LAWS.md). The decisions are in [the ADRs](docs/adr/README.md), and the descriptions of the repo are in [the design docs](docs/design/README.md).
