# Outcome: tooling and delivery

A stand-in round table heard the slate in two rounds, with no third round. The chair adopted all nine decisions with wording edits that took every round 2 amendment. The final wording is in `final.md`.

## Recorded

- ADR-0003 holds the development tools and the lock file. ADR-0004 holds the suites. ADR-0005 holds workflows and gates. ADR-0006 holds releases.
- The ledger has one row for each of the nine decisions.
- The decisions of the user (gates on a pull request ready for review, and release by a label) were adopted in the user's own words, so nothing about them is held.
- Every ADR has origin `agent`, because each holds at least one call that the planning work reasoned. The user is offered the outcome to confirm.

## Held for the user

The table reworded the held law ("format check", "with no finding", the ADR's ID), so LAW-000016 is not registered until the user answers. The matter folder `.avalon/matters/standards-laws/` stays until then. The table's wording is in `final.md`.

The user may also decide three proposals that no decision includes:

- bar suppressions in the held law, outside `pyproject.toml`;
- a `none` label for a pull request that should not release;
- refuse `major` below 1.0.0 in the label check.

## Sorted out for design docs

Required checks come on in stages. It is now a guideline in `docs/design/engineering-standards.md`. markdownlint is a docs-scope proposal for a later sitting.
