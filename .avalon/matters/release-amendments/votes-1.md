# Round 1 votes (blind)

P is the Practitioner, Sk the Skeptic, J the Jurist, St the Steward, Sc the Scout. A is approve, M is amend. A seat that approved on condition that the record state something, and so asked for an addition, is counted as amend only where it asked to change wording.

| Item | P | Sk | J | St | Sc | Tally |
|---|---|---|---|---|---|---|
| A. Amend LAW-000016 as LAW-000017 | A | M | A | M | M | 2 approve, 3 amend, 0 reject |
| B. ADR-0006: a `none` label | A | A | M | A | M | 3 approve, 2 amend, 0 reject |
| C. ADR-0006: the label check refuses `major` | A | A | M | M | M | 2 approve, 3 amend, 0 reject |

## Amendments raised

- A (Sk): "...with no finding, and no comment in it turns a check off; tool settings that turn a check off live only in `pyproject.toml`." (St): "...with no finding, and no check is turned off outside `pyproject.toml`." (Sc): "turns a check off only in `pyproject.toml`", verb order fixed. These reword the user's accepted law.
- A (P, J, Sk, St, Sc): the record must state what "a check" covers: `# noqa`, `# ruff: noqa`, `# fmt: off`, `# fmt: skip`, `# type: ignore`, and `# mypy:`, and not `# pragma: no cover`. (St, J): a detail file `LAW-000017.md` is the home. (J): the archive row fills every column.
- B (J): the Context of ADR-0006 says the label decision came from the user and the other from the agent, which is untrue once the skip of a `none` commit and the refusal of `major` are the user's. (Sc): add rejected alternatives: skip by path, a skip marker in the title, batching into a scheduled release; and say whether `none` is allowed on a change to `plugin/**`.
- C (St): one combined sentence in place of the user's added sentence. This rewords the user's sentence. (J): the Consequences line says a label can change after the merge "when no check can stop the merge", since a label event can fire for a closed pull request. (Sc): say the label check reads the latest version and the variable through the same GitHub port as the release code (ADR-0004). (Sk): the label check and the release code call one shared function under `devtools/`.
- C (J): the user is asked to confirm that the release code's refusal stays.

## Notes for the chair

An amendment that rewords the user's accepted wording registers nothing until the user answers. Take the amendments that add to the record without rewording the user's sentences, and list the rest under held for the user.
