---
summary: Definitions of the terms this repo uses. Search it for a term you do not know.
covers: [docs/**, .avalon.yml]
verified: 2026-11-12
verified_commit: b91b169fb6b690365f6b9d3e6ed1d8e85cfcc769
---
# Glossary

| Term | Meaning |
|---|---|
| ADR | A living document that records one decision that is costly to reverse. It is edited in place and always states the decision in effect. |
| Archive | The file of every amended or removed law: `docs/laws/archive.md`. Nothing in it is in effect. |
| Avalon | A Claude Code plugin that gives a repo laws, ADRs, and design docs, and the project in this repo that builds it. |
| Chair | The agent that runs a round table, decides, and registers the outcome. |
| Decision | A choice that is costly to reverse and had real alternatives. It is recorded in an ADR. |
| Design doc | A document that describes the repo as it is, with a stamp that shows when it was last checked. |
| Detail file | A file that carries a law's full meaning when one sentence cannot. It is named for the law, such as `LAW-000009.md`. |
| Law | A standing rule in the registry. It binds everything in the repo. |
| Ledger | The record of every round-table decision and every confirmation by the user: `docs/laws/ledger.md`. |
| Legacy | In the repo at the install commit. A legacy decision is recorded without a round table. |
| Matter | What a round table decides: a law matter or a decision matter. |
| Origin | Who a law or ADR came from: `core`, `user`, or `agent`. All three bind equally. |
| Registry | The table of every law in effect: `docs/laws/LAWS.md`. |
| Retired | Amended or removed, for a law. Deleted because it stopped applying, for an ADR. |
| Root | The folder that holds `laws/`, `adr/`, and `design/`. It is `docs/` in this repo. |
| Round table | Five seat agents and a chair that decide a matter in at most three rounds. |
| Scope | A one-word tag on a law, taken from the scope list in `.avalon.yml`. |
| Script | The one command-line program that does every mechanical step. It does not exist yet. |
| Seat | A subagent that votes at a round table from one fixed perspective. |
| Stand-in | A subagent that plays a role that the plugin's own agent will take, such as writer, editor, or seat. |
| The work | Whatever a repo exists to hold, such as source, manuscript, configuration, or prompts. |
