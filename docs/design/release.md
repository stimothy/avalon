---
summary: How the release code under `devtools/release/` works out versions from tags and pull request labels, what a run does, the dry run, and what the release notes hold.
covers: [devtools/release/**, devtools/adapters/gh.py, devtools/adapters/git.py]
verified: 2026-11-13
verified_commit: 2e8c0fb00d73bebf6e7ec47cf0ad2ce2752569b7
---
# The release code

`python -m devtools.release` turns merged pull requests and their labels into versions. The rules it follows are in [ADR-0006](../adr/0006-releases.md). `release.yml` runs `release` on each push to `master`, and `pr.yml` runs `dry-run` on each pull request ([the workflows](gates-workflow.md)).

## Versions and labels

- The latest version is the highest tag of exactly the form `vMAJOR.MINOR.PATCH`, compared as numbers. A tag of any other form, such as `v1.0`, `v1.0.0-rc1`, or `v01.0.0`, is ignored (`version.py`).
- A pull request carries exactly one of `major`, `minor`, `patch`, and `none`. Other labels are ignored.
- The label raises its own part and zeroes every part after it. With no version, the count starts from `v0.0.0`.
- `none` makes no version.

## The refusal of `major`

`policy.major_refusal` refuses `major` while no version exists or the latest is below `v1.0.0`, unless the repository variable `ALLOW_PRE_1_MAJOR` has the value `true`. The release run, the dry run, and the label check of `pr.yml` (`devtools/gates/pr_labels.py`) all call it.

## A release run

`python -m devtools.release release [--ref HEAD]` walks the commits on the first-parent line after the commit of the latest version, oldest first. With no version it takes only the newest commit.

For each commit it reads the labels its merged pull request carries at that moment:

| Commit | Result |
|---|---|
| No merged pull request | No version of its own; its changes ship in the next one. |
| Label `none` | Skipped; its changes ship in the next one. |
| More than one merged pull request, or not exactly one of the four labels | The run stops and names the pull request or the commit. |
| `major` that is refused | The run stops and names the pull request. |
| Any other label | One call creates the tag at that commit and the GitHub release. |

Before the walk, if the latest version's tag exists without its GitHub release, the run creates that release on the tag's own commit and leaves the tag as it is. A version whose release exists is not made again, so a second run over the same commits makes nothing twice. The code never pushes a commit.

Exit codes: 0 when the run finishes, 1 when it stops on a commit, 2 when git or `gh` fails.

## The dry run

`python -m devtools.release dry-run --pr N` prints the version pull request `N` would get from the latest tag, or the reason it is refused, and creates nothing. It does not walk the commits between the latest tag and the pull request, so it can differ from a later run when other pull requests merge first.

## Release notes

The notes start with an `On upgrade` section for what a user must do in a target repo, followed by the list of changes that GitHub generates. The `On upgrade` section holds a fixed line until a person edits the release.

## Ports

The code reaches git through `RealGit` and GitHub through `RealGh`, which runs `gh` through the process adapter and reads the repository variable from the environment first, because a workflow token cannot read it. Unit tests replace both with fakes. The contract suite runs the git fake and `RealGit` through the same cases in a throwaway repo. No suite reaches GitHub.
