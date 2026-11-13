---
adr: 0002
summary: This repo uses Avalon for its laws, ADRs, and design docs, with the root at docs/.
covers: [docs/**, .avalon.yml, CLAUDE.md]
origin: user
---
# ADR-0002: Documentation system

## Context

Avalon is a plugin that gives a repo three kinds of governed document. This repo builds Avalon and follows the same process on itself.
No `docs/` folder existed when the system was adopted, so the default root caused no clash.

## Decision

This repo uses Avalon. The root is `docs/`, which holds `laws/`, `adr/`, and `design/`. The config file is `.avalon.yml` at the top of the repo. A managed block in `CLAUDE.md` imports the registry.

The user made this decision by setting up the system by hand. No round table sat for it.

## Consequences

- Every law is created, amended, or removed through a round table.
- Until the plugin's agents exist, stand-in subagents hold the round table, and records are written by hand.
- Design docs live in `docs/design/` and are updated in the same change that makes them untrue.

## Alternatives rejected

- **Rejected: a root other than `docs/`.** The reason is unknown.
- **Rejected: no governed docs in this repo.** The reason is unknown.

## Changelog

- 2026-11-12 (user): Created. Adopted Avalon in this repo.
