---
title: 'Story 1.3: The engineering standards, refined with the user'
type: 'feature'
created: '2026-11-12'
status: 'in-review'
baseline_commit: '712486c'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The user's ten engineering standards have no exact wording, kind, or check, so nothing binds the first line of code.

**Approach:** Give each standard wording, a kind, and a check. Guidelines go into one design doc, written by a stand-in writer and edited by a stand-in editor. Laws and ADRs are held as proposals in matter folders under `.avalon/`, unregistered.

## Boundaries & Constraints

**Always:** Docs and config only. Permanent files cite no plan folder, requirement ID, or home path. Each law is one sentence of at most 200 characters with a scope.

**Never:** Register a law or ADR, add a ledger row, or add code, a test, or a workflow.

## Decisions

- Kinds as the addendum proposes. The user sent the kind question to the chair and the seats; the table may change a kind.
- The no-git/no-network law is scoped to the three test kinds, with no exception clause.
- A `code` scope is added to the scope list; the user agreed.

</frozen-after-approval>

## Tasks & Acceptance

- [x] `.avalon/matters/standards-laws/proposal.md` -- seven law proposals with scope, wording, check
- [x] `.avalon/matters/standards-adrs/proposal.md` -- two ADR proposals (test layout, tool choice)
- [x] `docs/design/engineering-standards.md`, `docs/design/README.md`, `docs/design/glossary.md` -- guidelines doc, index row, term
- [x] `.avalon.yml` -- add `code` to scopes

**Acceptance:** Given the repo, then no code, test, or workflow exists; the registry still holds nine laws; the design index lists the new doc.

## Implementation Notes

`.avalon/` is not git-ignored yet, so the proposals are tracked and travel with the branch. The Story 1.4 round table hears the laws.
