# ADRs

Each ADR records one decision that is costly to reverse. Read the ADR for an area before changing it.

- [0001-architecture.md](0001-architecture.md): Avalon is a plugin of three layers with a standard-library Python script that never calls a model, has a pure core and all-or-nothing writes, and reads git through one read-only module.
- [0002-documentation-system.md](0002-documentation-system.md): This repo uses Avalon for its laws, ADRs, and design docs, with the root at docs/.
- [0003-development-tools.md](0003-development-tools.md): pytest, coverage, ruff, and mypy are the development tools, configured in one pyproject.toml, and the lock file is the only home of a tool version.
- [0004-test-suites.md](0004-test-suites.md): Each test suite has its own folder and a fixed reach, and the release code reaches GitHub only through a port.
- [0005-workflows-and-gates.md](0005-workflows-and-gates.md): Workflows hold no logic, gates run on pull requests that are ready for review, gitleaks does the secret scan, and a ruleset protects master.
- [0006-releases.md](0006-releases.md): A pull request's label picks the version or none, and one workflow releases every newer commit not labelled none.
