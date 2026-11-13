---
summary: What `gates.yml`, `pr.yml`, and `release.yml` run and when, the jobs to require as checks, the Python and runner choices, and how Dependabot is set up.covers: [.github/**, devtools/gates/**]
verified: 2026-11-13
verified_commit: 2e8c0fb00d73bebf6e7ec47cf0ad2ce2752569b7
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

No job runs the evals, and no workflow calls a model or holds a model credential. A contributor runs the evals locally before a push ([ADR-0004](../adr/0004-test-suites.md)).

## The check to require

`all-green` is the one job to require in the ruleset on `master`. It runs after every other job, even when one failed, and fails unless each job succeeded or was skipped because the filter said it did not apply (`devtools/gates/verdict.py`). Requiring it covers every other job, so a new job needs no change to the ruleset as long as `all-green` lists it in `needs`.

## Python and runners

Jobs are few and long, not many and short, to stay within the limit on jobs that run at once. A suite that fails stops the later suites of its job.

- Every runner label is pinned: `ubuntu-24.04` and `macos-15`.
- The "current release" of Python is written as `3.14`, in the `suites` matrix and in `code`.
- A job on Python 3.9 first runs `python -m devtools.gates interpreter --expect 3.9`, which fails when the interpreter reports another version.
- On macOS the 3.9 job uses `/usr/bin/python3` and sets `UV_PYTHON_DOWNLOADS=never`, so `uv` downloads no interpreter. The `macos-15` runner's system interpreter reports 3.9.6, so no other runner or install is in use.
- Every job installs the Python tools with `uv sync --locked` and the Node tools with `npm ci`. `claude plugin validate` runs from the Claude Code package in `package-lock.json`.

## The pull request workflow

`.github/workflows/pr.yml` checks the pull request itself. It runs on a pull request into `master` when the pull request is opened, reopened, given more commits, marked ready for review, labelled, unlabelled, or has its title or body edited. A draft runs no job. A newer run on the same pull request cancels the older one, in a group of its own, so `gates.yml` is never touched.

Its one job, `pr`, is the check to require next to `all-green`. It runs, in order:

1. `python -m devtools.gates pr-labels --pr N`, which fails unless the pull request carries exactly one of `major`, `minor`, `patch`, and `none`, and fails `major` while no version exists or the latest is below `v1.0.0`, unless the repository variable `ALLOW_PRE_1_MAJOR` is `true` (`devtools/gates/pr_labels.py`, which calls `policy.major_refusal`).
2. `python -m devtools.gates pull-request`, which scans the title and the body for plan citations.
3. `python -m devtools.release dry-run --pr N`, which shows the version the pull request would get.

A workflow token cannot read repository variables through `gh`, so the workflow passes `ALLOW_PRE_1_MAJOR` in the environment, and `RealGh.variable` uses the environment when it defines the name, an empty value meaning unset, and asks `gh` only when it does not.

## The release workflow

`.github/workflows/release.yml` runs on a push to `master` and is the only workflow that does. All its runs share the group `release`, and a later run never cancels one in progress. Its one job, `release`, is the only job with a write permission (`contents: write`). It checks out the full history and runs `python -m devtools.release release --ref` the pushed commit. See [the release code](release.md).

## gitleaks

`devtools/gates/gitleaks_pin.py` holds the one version and one checksum for each platform. `python -m devtools.gates install-gitleaks` downloads that version, fails if the checksum differs, and puts it on the path. `code` runs that command, then the scan.

## Dependabot

`.github/dependabot.yml` asks for weekly updates of GitHub Actions pins, npm packages, and `uv` packages. Each pull request carries the `patch` label.

The `uv` ecosystem is configured for the root, where `uv.lock` lives. Whether Dependabot rewrites `uv.lock` is unknown until it opens its first `uv` pull request. If it does not, a maintainer runs `uv lock --upgrade` by hand and commits `uv.lock` to that pull request.

Dependabot does not update `gitleaks_pin.py`, so a maintainer changes that file by hand.
