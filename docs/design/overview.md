---
summary: What this repo is, what it holds, and where each part lives. Read it before the first change.
covers: ['*']
verified: 2026-11-12
verified_commit: b91b169fb6b690365f6b9d3e6ed1d8e85cfcc769
---
# Overview

Avalon is a Claude Code plugin that gives any repo three kinds of governed document: laws, ADRs, and design docs. This repo builds Avalon, and it follows Avalon's own process on itself. Terms are defined in the [glossary](glossary.md).

## Purpose and audience

The plugin is for people who work with agents in a repo and want its rules, decisions, and descriptions kept in one checked place. The repo is public, MIT licensed, and pre-release. It has no working round table and collects no usage data.

## What it contains

The repo holds its own governed docs and the files that describe and license it. The plugin itself (skills, agents, hook, script, and templates) does not exist yet. The docs are written by hand, and stand-in subagents hold the round table.

## Map of the repo

| Path | Holds |
|---|---|
| `docs/laws/` | The registry of laws, the archive, the ledger, and law detail files. |
| `docs/adr/` | ADRs and their index. |
| `docs/design/` | Design docs and their index. |
| `.avalon.yml` | The config file: root, profile, version, install record, caps, and scope list. |
| `CLAUDE.md` | The managed block that loads the registry into every session. |
| `README.md`, `LICENSE`, `CODE_OF_CONDUCT.md` | The public face of the repo. |
| `CONTRIBUTING.md` | The setup command, the command for each test suite, the check commands, and how to propose a change. |
| `.github/` | The workflows, the Dependabot config, the code owner file, and the issue and pull request templates. See [the gates workflow](gates-workflow.md) and [the repository settings](repository-settings.md). |
| `devtools/` | The Python code the gates run: the gate commands, the release code, and the adapters they use. |
| `tests/` | The `unit/`, `integration/`, `e2e/`, `contract/`, and `fakes/` folders, the shared guard, and the unit time budget. |
| `pyproject.toml`, `uv.lock` | The Python development tools, their one configuration, and their locked versions. |
| `package.json`, `package-lock.json`, `.markdownlint-cli2.jsonc` | The markdown lint, its locked version, and its rules. |

## How to work in it

- Read the registry before any work. Every law in it binds.
- Read the ADR for an area before changing it. The index is [docs/adr/README.md](../adr/README.md).
- Change a law only through a round table.
- Update a design doc in the same change that makes it untrue.
