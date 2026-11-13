# Outcome: tooling and delivery

A stand-in round table heard the slate in two rounds, with no third round. The chair adopted all nine decisions with wording edits that took every round 2 amendment. The final wording is in `final.md`.

## Recorded

- ADR-0003 holds the development tools and the lock file. ADR-0004 holds the suites. ADR-0005 holds workflows and gates. ADR-0006 holds releases.
- The ledger has one row for each of the nine decisions.
- The user accepted the table's wording of the held law, so LAW-000016 is registered, and the matter folder `.avalon/matters/standards-laws/` is removed.
- The user confirmed the four ADRs, so each has origin `user`, a `(user)` changelog line, and a ledger row decided by `user`.

## Open for the user

The user accepted three proposals that no adopted decision includes. Each changes a record that is already written, so each needs a table:

- bar suppressions in LAW-000016, outside `pyproject.toml`;
- a `none` label for a pull request that should not release (ADR-0006);
- refuse `major` below 1.0.0 in the label check (ADR-0006).

## Sorted out for design docs

Required checks come on in stages. It is now a guideline in `docs/design/engineering-standards.md`. markdownlint is a docs-scope proposal for a later sitting.
