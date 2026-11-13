---
adr: 0004
summary: Each test suite has its own folder and a fixed reach, the contract suite runs each git fake and its real adapter through the same cases, and the release code reaches GitHub only through a port.
covers: [tests/**, devtools/**, .github/workflows/**]
origin: agent
---
# ADR-0004: Test suites

## Context

LAW-000011 puts every test in exactly one suite and runs each suite apart from the others. LAW-000012 and LAW-000013 limit what the unit, integration, and end-to-end suites may touch. The laws do not say which folder holds a suite or what each suite may reach.

ADR-0001 puts the file system, git, and the time behind ports. The release code of ADR-0006 reaches GitHub. The repo shows no earlier choice of suite layout. The reason for each choice below is unknown.

## Decision

### Each suite has a folder and a fixed reach

A test's folder sets its suite. Each suite may reach only what this table allows.

| Suite | May reach |
|---|---|
| Unit | One unit, with every port faked. |
| Integration | The real file system in a temporary folder, with git and GitHub faked. |
| End-to-end | The whole command line and the hook, in process, on a temporary folder, with git and GitHub faked. |
| Contract | Real git, in a throwaway repo. |
| Eval | Claude Code, a model, and a copy of a fixture. |

- The contract suite runs each git fake and its real adapter through the same cases.
- The release code reaches GitHub only through a port.
- The real GitHub adapter takes its HTTP transport as a port, and every suite fakes that transport.
- No suite reaches GitHub, and the adapter's lines run under test.
- Each suite is its own gate job.

## Consequences

- A test moves to another suite by moving its folder.
- The contract suite is the one place where a git fake is held to the real git.
- Only the eval suite reaches a model.
- The GitHub adapter is tested only against a fake transport. What the real GitHub returns is not tested by any suite.

## Alternatives rejected

- **Rejected: one suite with markers.** The reason is unknown.
- **Rejected: no contract suite, with the git fakes trusted.** The reason is unknown.
- **Rejected: real git in the integration suite.** The reason is unknown.
- **Rejected: the contract suite on a schedule, not on each pull request.** The reason is unknown.

## Changelog

- 2026-11-12 (agent, table): Created. Recorded the folder and the fixed reach of each suite, and the transport port of the GitHub adapter.
