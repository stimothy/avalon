- source_spec: `_bmad-output/implementation-artifacts/spec-1-5-a-stand-in-round-table-hears-the-architecture.md`
  summary: The glossary gained rows but its verified stamp still names the older commit.
  evidence: The stamp is written by the verify command once the script exists; hand-editing it would forge a check.

- source_spec: `_bmad-output/implementation-artifacts/spec-1-6-a-stand-in-round-table-hears-the-tooling-and-delivery-decisions.md`
  summary: ADR-0006 starts the first release run at the commit that added release.yml, which may carry no version label, and states no concurrency guard for overlapping release runs.
  evidence: Raised in review; the table adopted neither wording, so the release story (1.12 and 1.13) should settle both and update ADR-0006.
