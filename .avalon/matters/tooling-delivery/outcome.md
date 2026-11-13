# Outcome: tooling and delivery

A stand-in round table heard the slate in two rounds, with no third round. The chair adopted all nine decisions with wording edits that took every round 2 amendment. The final wording is in `final.md`.

## Recorded

- ADR-0003 holds the development tools and the lock file. ADR-0004 holds the suites. ADR-0005 holds workflows and gates. ADR-0006 holds releases.
- The ledger has one row for each of the nine decisions.
- The user accepted the table's wording of the held law, so LAW-000016 was registered (later amended as LAW-000017), and the matter folder `.avalon/matters/standards-laws/` is removed.
- The user confirmed the four ADRs, so each has origin `user`, a `(user)` changelog line, and a ledger row decided by `user`.

## Amended afterward

The user accepted three proposals that no adopted decision included. A second table heard them in `.avalon/matters/release-amendments/`: LAW-000016 became LAW-000017 (a check is turned off only in `pyproject.toml`), and ADR-0006 gained a `none` label and a refusal of `major` below 1.0.0 in the label check.

Questions for the user remain in `.avalon/matters/release-amendments/final.md`, under "Held for the user".

## Sorted out for design docs

Required checks come on in stages. It is now a guideline in `docs/design/engineering-standards.md`. markdownlint is a docs-scope proposal for a later sitting.
