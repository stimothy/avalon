---
title: 'Story 1.2: This repo''s own Avalon tree, created by hand'
type: 'feature'
created: '2026-11-12'
status: 'done'
baseline_commit: 'b91b169fb6b690365f6b9d3e6ed1d8e85cfcc769'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The repo has no Avalon docs tree, no `.avalon.yml`, and no `CLAUDE.md`, so no rule, decision, or description has a home.

**Approach:** Write by hand, in final format, the tree an Avalon install would create: `docs/laws/`, `docs/adr/`, `docs/design/`, `.avalon.yml`, and the `CLAUDE.md` block that imports the registry. Formats come from `temporary-plans/SPEC.md` sections 3, 5, 6, 7, 9, 11.

## Boundaries & Constraints

**Always:** Docs and config only; no code. Core law text copied verbatim from the draft set. Permanent files cite no plan folder, requirement ID, or home path. No time words ("new", "now", "previously") in the prose docs. Unknowns are written as unknown.

**Never:** Hold a round table or add a ledger row for ADR 0002. Put a checksum in `.avalon.yml`. Add `0001-architecture.md`. Add a law beyond the nine core laws.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Covers globs | Each `covers` entry | Matches at least one tracked path; at most five entries per doc | Fix the glob |
| Law length | Each registry law | One sentence, at most 200 characters | Shorten only if the user agrees; core text is verbatim |
| Session load | Session opens in repo | `CLAUDE.md` block imports `docs/laws/LAWS.md` | N/A |

</frozen-after-approval>

## Code Map

- `temporary-plans/SPEC.md` -- formats (sections 3, 5, 6, 7, 8, 9, 11) and default caps (section 18). Read-only; never cited from permanent files.
- `.gitignore` -- tracks `docs/`, `.avalon.yml`, `CLAUDE.md`; nothing to change.
- Install commit: `b91b169fb6b690365f6b9d3e6ed1d8e85cfcc769` (HEAD of `master` when the tree is created).

## Tasks & Acceptance

**Execution:**
- [x] `docs/laws/LAWS.md` -- registry: binding statement, nine core laws, origin `core`, LAW-000009 links its detail file -- FR-32
- [x] `docs/laws/archive.md`, `docs/laws/ledger.md` -- header-only tables, archive opens with "not in effect" line -- FR-32
- [x] `docs/laws/LAW-000009.md` -- draft writing standard as detail file (exempt from the four-part body) -- FR-32
- [x] `docs/adr/0002-documentation-system.md`, `docs/adr/README.md` -- install ADR, origin `user`, `(user)` changelog; index -- FR-34
- [x] `docs/design/overview.md`, `glossary.md`, `README.md` -- stand-in written and edited against the draft standard -- FR-48
- [x] `.avalon.yml`, `CLAUDE.md` -- config without checksum; block between markers -- FR-32

**Acceptance Criteria:**
- Given the repo, then every file named in story 1.2 exists and the archive and ledger hold no row.
- Given the registry, then it holds LAW-000001 to LAW-000009, origin `core`.
- Given `.avalon.yml`, then it holds root, profile, version 1, UTC install time, install commit, caps, scope list, and no checksum.
- Given `CLAUDE.md`, then the block sits between the two markers and imports the registry.
- Given ADR 0002, then origin is `user`, the changelog line carries `(user)`, and the ledger has no row for it.

## Implementation Notes

Stand-in writer and stand-in editor were this session, working against the draft writing standard. `temporary-plans/` is left out of the overview map so permanent docs name no plan folder. Install time is UTC at creation. ADR 0002 and the glossary/overview stamps use the install commit.

## Spec Change Log

## Review Triage Log

Inline self-review only. Greps for emails, home paths, plan citations pass; remaining time-word hits are the verbatim core law, the archive column header, and the standard's own quoted examples. Law lengths max 163 of 200.

## Design Notes

Choices made without the user (not visible in the result's intent): profile `other`; caps are the defaults the spec suggests (law 200 characters, registry 100 laws, document 400 lines, diagram 15 nodes, image 500 KB, sentence 40 words); scope list `all, laws, adr, design, docs`; `verified_commit` holds the install commit.

## Verification

**Commands:**
- `grep -rIEn "@[A-Za-z0-9.-]+\.[a-z]{2,}|/Users/" docs .avalon.yml CLAUDE.md` -- expected: no match
- `grep -rIn "temporary-plans/\|REQ-\|_bmad" docs .avalon.yml CLAUDE.md` -- expected: no match
- `awk -F'|' 'NR>2 && /^\| LAW-/ {print length($5)}' docs/laws/LAWS.md` -- expected: each at most 201
