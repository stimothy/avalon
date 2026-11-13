# Law matter: engineering standards

Kind: law matter, one slate. Proposer: the user. Status: a stand-in round table heard the slate in three rounds; LAW-000010 is registered, and six proposals are held for the user's decision. Scope `code` is on the scope list.

## Shared definition (detail for proposals 5, 6, and 7)

This repo authors every git-tracked path except `_bmad/`, `_bmad-output/`, and `.claude/`. The table recommends the words "git-tracked", so that untracked and ignored files do not count.

## Held proposals

Each held proposal was voted on separately and ended 5 approve, 0 amend, 0 reject in the last round. A proposal marked "reworded" differs from the user's text, so it is registered only when the user accepts the table's wording, counters it, or directs that the original be registered as written.

| # | Scope | Origin | Table's recommended law | The user's original | Check |
|---|---|---|---|---|---|
| 2 | code | user | Every test belongs to exactly one suite (unit, integration, end-to-end, contract, or eval), and each suite runs separately from the others. | Reworded: two sentences became one, and "run apart" became "separately". | Each suite is its own gate job, and a gate fails any test in no suite. |
| 3 | code | user | A unit test touches no file system, subprocess, or network beyond pytest's own import and cache access, and the whole unit run finishes within 10 seconds. | Reworded: the 10-second budget and the carve-out move from the detail and the test-layout ADR into the law. | A gate blocks those calls and times the unit run. |
| 4 | code | user | No integration or end-to-end test uses git or the network. | Reworded: "unit" is dropped, because proposal 3 already covers unit tests. | A blocking fixture fails any such test that starts git or opens a connection. |
| 5 | code | user | Tests cover at least 80% of the lines of Python this repo authors, tests excluded. | Reworded: "lines" names the measure. | A gate fails below 80%. |
| 6 | code | user | Python this repo authors passes the repo's linter, formatter, and type checker, which the tool-choice ADR names. | Not reworded. Held because the tool-choice ADR does not exist yet. | Gates run each tool. |
| 7 | code | user | No directory this repo authors is named utils, helpers, misc, common, or tmp, in any letter case. | Reworded: "in any letter case" moves from the check into the law. | A gate matches directory names at any depth. |

## Detail for proposal 3

The gate does not block the file access that pytest makes for its cache and imports. It blocks temp files, so a unit test uses a fake and not `tmp_path`. Real file access belongs in the integration suite.

## Detail for proposal 4

The contract tests and the plugin evals are suites outside the unit, integration, and end-to-end kinds, so the law needs no exception clause. The contract tests start git in a throwaway repo, use no network, and never touch this repo's own git state.

## Detail for proposal 5

The tests directory is excluded.

## Option for the user on LAW-000010

The Enforcer proposed requiring a `# Act` comment on the Act of each test, so that a gate could check the law. The table did not adopt it. The user may propose it as an amendment.

## Raised for a separate matter

markdownlint is not part of this slate. It is a docs-scope proposal, checked against the writing standard, for a later sitting.
