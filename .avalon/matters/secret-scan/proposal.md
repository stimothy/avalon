# Decision matter: the secret scan

Kind: decision matter, one decision. Proposer: the user. Status: proposed; nothing is registered.

The user stated the choice of tool and asked for a sixth stand-in sitting to hear it. The chair applies the ADR test (costly to reverse, and real alternatives that a later reader would ask about) and checks the decision against the laws and ADR-0001, ADR-0003, ADR-0004, ADR-0005, and ADR-0006. A call that fails the test becomes a guideline in `docs/design/engineering-standards.md`. A call that an ADR already owns extends that ADR.

## The decision

### The secret scan is done by gitleaks (origin: user)

A gate in `gates.yml` scans the tracked files for a secret with `gitleaks`. The gate fails on a finding. Code under `devtools/` runs the tool through the one adapter that starts processes, and the unit tests replace that adapter with a fake. The docs of this repo record that `gitleaks` does the scan.

Known facts the table should weigh:

- `gitleaks` is not a Python package, so `uv.lock` cannot lock it. ADR-0003 says the lock file is the only home of the version of a tool it locks. Where the version of `gitleaks` is stated is unknown.
- How a workflow installs `gitleaks` is unknown until the workflow is written.
- ADR-0005 says every action is pinned to a full commit SHA, and logic stays out of workflows.

Alternative: `trufflehog`. Alternative: `detect-secrets`. Alternative: a pattern scan written under `devtools/`. Alternative: GitHub's own secret scanning and push protection, with no gate.
