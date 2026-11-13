# Epic 1 Context: A public repo that governs itself and gates every change

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

A contributor can clone the public repo, set up the tools, and open a pull request that the gates check; every merge releases a version below 1.0. The repo holds its own Avalon docs tree from day one, and a stand-in round table hears its first laws and decisions. Stories 1.1 to 1.6 write no code: engineering standards come before any code, and the architecture's round table comes before the code that follows it.

## Stories

- Story 1.1: The repo's public face
- Story 1.2: This repo's own Avalon tree, created by hand
- Story 1.3: The engineering standards, refined with the user
- Story 1.4: A stand-in round table hears the standards that are laws
- Story 1.5: A stand-in round table hears the architecture
- Story 1.6: A stand-in round table hears the tooling and delivery decisions
- Story 1.7: A contributor can set up the tools and run each suite
- Story 1.8: A person can install the plugin from the repo
- Story 1.9: A gate scans tracked files for plan citations, home paths, and secrets
- Story 1.10: Gate logic lives in tested code
- Story 1.11: The gates run on a pull request that is ready for review
- Story 1.12: Release code works out the next version
- Story 1.13: A pull request needs one version label, and a merge releases
- Story 1.14: The owner turns the rules on, and a drill proves them

## Requirements & Constraints

- Avalon is MIT licensed; templates later carry MIT No Attribution.
- The README must let a stranger decide whether to use Avalon; early on it states pre-release status.
- The repo carries the community files GitHub's community standards checklist names (licence, code of conduct, security policy later).
- No tracked file or governed document may publish a secret or a person's private details.
- No data collection: Avalon opens no network connection and collects no usage data; the README says so.
- Gates run only on pull requests into `master` that are ready for review; a newer push cancels an older run.
- A merge into `master` releases the next semantic version, chosen by a `major`, `minor`, or `patch` label.

## Technical Decisions

- `gates.yml` and `pr.yml` gate a pull request with one final verdict job. A ruleset on `master` requires a PR, both checks, an up-to-date branch, and squash merges.
- Only a few files (the gate skip list, `.gitignore`, `pyproject.toml`, markdown lint config) may name a plan folder.
- Git ignores local tool state, personal config, virtual environments, and working files such as decision logs and review notes.
