# Round 1 votes (blind)

Items use the numbers in `screening.md`. P is the Practitioner, Sk the Skeptic, J the Jurist, St the Steward, Sc the Scout. A is approve, M is amend.

| Item | P | Sk | J | St | Sc | Tally |
|---|---|---|---|---|---|---|
| 1. Development tools | A | M | A | M | M | 2 approve, 3 amend, 0 reject |
| 2. Lock file | A | A | M | A | M | 3 approve, 2 amend, 0 reject |
| Held law | A | A | M | M | A | 3 approve, 2 amend, 0 reject |
| 3. Suites | A | A | M | A | M | 3 approve, 2 amend, 0 reject |
| 4. No logic in workflows | M | A | M | A | A | 3 approve, 2 amend, 0 reject |
| 5. Gates on ready pull requests | M | A | M | A | A | 3 approve, 2 amend, 0 reject |
| 6. Two workflows, one verdict job | A | A | M | A | M | 3 approve, 2 amend, 0 reject |
| 7. Ruleset | A | M | A | M | M | 2 approve, 3 amend, 0 reject |
| 8. Release by label | A | M | M | A | M | 2 approve, 3 amend, 0 reject |
| 9. Release workflow | A | A | M | M | M | 2 approve, 3 amend, 0 reject |

## Amendments raised

- 1: measure coverage from the unit, integration, and contract runs together, since the git adapters run only in the contract suite (Sk); say why ruff and mypy, name the venv, and follow LAW-000014 without restating its number (St); add alternatives black, flake8, pyright, unittest (Sc); say which run the unit time budget is timed on (J, note).
- 2: say "the version of a tool that `uv.lock` locks", so `uv` and the Python floor are not caught; drop the plugin-folder sentence, which repeats ADR-0001 (J); name the gate that checks it, or drop the claim (St); add alternatives poetry, pdm, pip-tools (Sc).
- Held law: cite ADR-0003 by ID, say "format check" and "with no finding" (J); do not depend on an ADR number (St); optionally bar suppressions beyond `pyproject.toml` (Sk).
- 3: name the fifth suite "eval" as LAW-000011 does (J, St); add alternatives: real git in one end-to-end test (excluded by LAW-000013), contract tests on a schedule (Sc); the GitHub lookup falls outside every suite's reach (J, note).
- 4: replace "a few fixed forms" with a closed list that ADR-0005 states, including `always()` (J); or let `devtools/` hold the list (P); state how SHA pins are updated (St).
- 5: add `edited`, `labeled`, and `unlabeled` for `pr.yml`, or give `pr.yml` its own triggers (P, J); say why no gate runs on `master` and that early feedback is local (St, Sk).
- 6: replace "did not touch what the job covers" with "skipped by its own `if:` condition" (J); require every skip to be explicit (Sk); add alternative: the ruleset requires each job by name (Sc).
- 7: no bypass actors, including the owner (Sk); say how the ruleset is checked, or that it is manual and who owns it (St, J); add alternatives: classic branch protection, the default squash message (Sc).
- 8: add a `none` label for a pull request that should not release (Sk); the label check also refuses `major` below 1.0.0 without the owner's variable (J); add alternatives: a version file, release-please, semantic-release, Conventional Commits (Sc).
- 9: `release.yml` is the one exception to "only the release job may write", and name the variable, "unknown until chosen" (St); "a bad release is never deleted or retagged" (J); ADR-0006 says its tagging code is outside `plugin/**` (J, St); say what happens to a commit with no pull request (Sk); add alternatives: a schedule, a release pull request (Sc).

## Notes for the chair

- Decisions 5 and 8 are the user's. An amendment that rewords either one registers nothing until the user answers.
- Moving the staged required checks into `engineering-standards.md` makes that doc's count and summary untrue, so it is updated in the same change.
