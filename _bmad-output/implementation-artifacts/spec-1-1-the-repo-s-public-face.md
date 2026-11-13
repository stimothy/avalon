---
title: 'Story 1.1: The repo''s public face'
type: 'chore'
created: '2026-11-12'
status: 'done'
baseline_commit: 'fadb595272fcdf5784e9679edb26fb471bc9b5ed'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The public repo `stimothy/avalon` has a one-line README, no licence, no code of conduct, and its GitHub settings allow direct pushes, merge commits, and rebase merges. It has no version labels and no private vulnerability reporting.

**Approach:** Add `LICENSE`, a pre-release `README.md`, and `CODE_OF_CONDUCT.md` (Covenant 3.0) in one pull request. Confirm `.gitignore` meets the ignore criteria. Apply the first GitHub settings only after the owner approves the exact commands.

## Boundaries & Constraints

**Always:** Docs only; no code. No personal name, email, or home path in any tracked file. The Covenant text stays verbatim except the reporting instruction. Every settings change is shown to the owner before it runs.

**Never:** Run a settings command without approval. Merge, push to `master`, or publish a personal address. Add a security policy (Epic 4).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Ignore rules | Create `.venv/`, `.env`, `.claude/settings.local.json`, `.memlog.md` | `git status` shows none | Add the missing pattern |
| Settings not approved | Owner has not answered | Files done; commands printed; story not marked done | Report as pending |

**Decision (owner approved):** The session applies the GitHub settings itself.

</frozen-after-approval>

## Code Map

- `.gitignore` -- already ignores OS/editor files, `.serena/`, `.claude` local state, `_bmad` user layers, `.venv/`, `.env*`, caches and decision logs. Check against the criteria; do not rewrite.
- `README.md` -- currently `# Avalon` only; replace.
- `temporary-plans/BRIEF.md`, `temporary-plans/SPEC.md` -- tracked working notes; do not edit or link from the README.
- GitHub `stimothy/avalon`: public. No rulesets. `allow_merge_commit` and `allow_rebase_merge` true. `squash_merge_commit_title` COMMIT_OR_PR_TITLE and message COMMIT_MESSAGES (need PR_TITLE and PR_BODY). Only the default labels exist. `private-vulnerability-reporting` is disabled.

## Tasks & Acceptance

**Execution:**
- [x] `LICENSE` -- MIT text, `Copyright (c) 2026 the Avalon contributors` -- FR-49
- [x] `README.md` -- what Avalon is, pre-release with no working round table, no usage data collected, MIT with link, link to `CODE_OF_CONDUCT.md` -- FR-50, NFR-5
- [x] `CODE_OF_CONDUCT.md` -- Covenant 3.0 verbatim; reporting: the repo's private vulnerability reporting form (`/security/advisories/new`) marked as a conduct report, and GitHub's abuse report for a maintainer -- FR-51
- [x] `.gitignore` -- add any missing pattern from the ignore criteria -- FR-53
- [x] GitHub settings (after approval) -- ruleset on `master` requiring a PR; squash only with PR title and PR body; labels `major`, `minor`, `patch`; private vulnerability reporting on -- AD-18
- [x] Pull request -- carries one of the three labels; created as a draft PR, not merged

**Acceptance Criteria:**
- Given the repo, when the PR opens, then `master` takes changes only through a PR, merges are squash-only, the three labels exist and the PR carries one, and private vulnerability reporting is on.
- Given `LICENSE`, then it is MIT and names "the Avalon contributors" with no person or email.
- Given the README, then it states pre-release, no working round table, no data collection, and MIT, and links the licence and the code of conduct.
- Given `CODE_OF_CONDUCT.md`, then it is Covenant 3.0, routes conduct reports as above, and publishes no address.
- Given a venv, a personal config file, or a decision log, then git ignores it.

## Implementation Notes

## Verification

**Commands:**
- `grep -rIEn "@[A-Za-z0-9.-]+\.[a-z]{2,}|/Users/" LICENSE README.md CODE_OF_CONDUCT.md` -- expected: no match
- `git check-ignore -v .venv .env .claude/settings.local.json _bmad-output/x/.memlog.md` -- expected: every path matched
- `gh api repos/stimothy/avalon/rulesets` and `gh label list` -- expected: ruleset present, three labels

## Review Triage Log

Inline self-review only (no reviewer subagents launched). No findings. Verification greps and ignore checks passed; settings verified via gh.
