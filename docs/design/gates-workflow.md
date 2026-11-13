---
summary: What `gates.yml` runs and when, the one job to require as a check, the Python and runner choices, and how Dependabot is set up.
covers: [.github/**, devtools/gates/**]
verified: 2026-11-13
verified_commit: 88d1415a2345a8a913ac4d85a68b9a0c18ea9327
---
# The gates workflow

`.github/workflows/gates.yml` checks the code and the docs of a pull request. The rules it follows are in [ADR-0005](../adr/0005-workflows-and-gates.md).

## When it runs

It runs on a pull request into `master` when the pull request is opened, reopened, given more commits, or marked ready for review. A draft runs no job. A push or a merge to `master` runs nothing. A newer run on the same pull request cancels the older one.

## The jobs

| Job | Runs | When |
|---|---|---|
| `changes` | The changed-path filter, which sets the `docs` and `plugin` outputs. | Always |
| `suites` | One job for each pair of Ubuntu or macOS and Python 3.9 or 3.14, four in all. Each runs the four test suites one after another. | Always |
| `code` | The linter, the formatter, the type checker, coverage, the scan of tracked files, the workflow check, and the secret scan, once, on Ubuntu and Python 3.14. | Always |
| `docs` | The markdown lint. | When a markdown file or a file under `docs/` changed |
| `plugin` | `claude plugin validate` on the repo root, which holds the marketplace file, and on `plugin/`. | When a file under `plugin/` changed |
| `all-green` | The verdict. | Always, after every other job, except on a draft |

## The check to require

`all-green` is the one job to require in the ruleset on `master`. It runs after every other job, even when one failed, and fails unless each job succeeded or was skipped because the filter said it did not apply (`devtools/gates/verdict.py`). Requiring it covers every other job, so a new job needs no change to the ruleset as long as `all-green` lists it in `needs`.

## Python and runners

Jobs are few and long, not many and short, to stay within the limit on jobs that run at once. A suite that fails stops the later suites of its job.

- Every runner label is pinned: `ubuntu-24.04` and `macos-15`.
- The "current release" of Python is written as `3.14`, in the `suites` matrix and in `code`.
- A job on Python 3.9 first runs `python -m devtools.gates interpreter --expect 3.9`, which fails when the interpreter reports another version.
- On macOS the 3.9 job uses `/usr/bin/python3` and sets `UV_PYTHON_DOWNLOADS=never`, so `uv` downloads no interpreter. The `macos-15` runner's system interpreter reports 3.9.6, so no other runner or install is in use.
- Every job installs the Python tools with `uv sync --locked` and the Node tools with `npm ci`. `claude plugin validate` runs from the Claude Code package in `package-lock.json`.

## gitleaks

`devtools/gates/gitleaks_pin.py` holds the one version and one checksum for each platform. `python -m devtools.gates install-gitleaks` downloads that version, fails if the checksum differs, and puts it on the path. `code` runs that command, then the scan.

## Dependabot

`.github/dependabot.yml` asks for weekly updates of GitHub Actions pins, npm packages, and `uv` packages. Each pull request carries the `patch` label.

The `uv` ecosystem is configured for the root, where `uv.lock` lives. Whether Dependabot rewrites `uv.lock` is unknown until it opens its first `uv` pull request. If it does not, a maintainer runs `uv lock --upgrade` by hand and commits `uv.lock` to that pull request.

Dependabot does not update `gitleaks_pin.py`, so a maintainer changes that file by hand.
