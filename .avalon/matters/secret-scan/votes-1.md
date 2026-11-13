# Round 1 votes (blind)

P is the Practitioner, Sk the Skeptic, J the Jurist, St the Steward, Sc the Scout. M is amend.

| Item | P | Sk | J | St | Sc | Tally |
|---|---|---|---|---|---|---|
| The secret scan is done by gitleaks | M | M | M | M | M | 0 approve, 5 amend, 0 reject |

## Amendments raised

None rewords the user's decision; each adds to the record.

- P: state the gitleaks version in exactly one pinned place that the gate reads; the workflow installs from it with a checksum check; scan tracked files only; a clear message when the binary is missing; developer and CI run the same gate and version; extend ADR-0003.
- Sk: the strongest alternative is GitHub secret scanning with no gate. It cannot fail a local run, so a gate is justified. State the version in one file, `devtools/gitleaks-version`; install by checksum through an action pinned to a full commit SHA; scan tracked files only; extend ADR-0003 with the exception.
- J: no law or ADR is contradicted. ADR-0005 owns the decision, with one cross-reference line in ADR-0003. A tool `uv.lock` cannot lock has its version in exactly one file under `devtools/`; a workflow installs it only through a `devtools/` command that reads the file and checks the checksum, or an action pinned to a full commit SHA; the workflow gate fails any other install.
- St: ADR-0003 says a tool `uv.lock` cannot lock has exactly one home for its version, a file the ADR names. The home of the gitleaks version is unknown until the workflow is written. No other file states it. Record the four alternatives with "The reason is unknown".
- Sc: all four alternatives are named, but none has a stated reason. git-secrets is missing (minor). Reasons the seats can give: a pattern scan means this repo maintains its own rules; GitHub secret scanning is not a gate and cannot fail a local run.

## Notes for the chair

Take amendments that add to the record. The user's decision is unchanged, so it can register. Unknowns are written as unknown (LAW-000006).
