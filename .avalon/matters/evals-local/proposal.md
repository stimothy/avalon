# Decision matter: the evals run locally

Kind: decision matter, one decision. Proposer: the user. Status: proposed; nothing is registered.

The user decided that no workflow runs the plugin evals or calls a model, and asked for a sitting to amend the ADRs that say otherwise. The chair applies the ADR test and checks the decision against the laws and ADR-0001 to ADR-0006.

## The decision

### No workflow runs the eval suite; a contributor runs it locally before a push (origin: user)

The eval suite stays one of the five suites and keeps its fixed reach: Claude Code, a model, and a copy of a fixture. It has no gate job, and no workflow calls a model or holds a model credential. A contributor runs the evals on their own machine, before a push, with their own Claude Code login.

Facts the table should weigh:

- ADR-0003 says each suite's gate job collects coverage data "except the eval job, which collects none". No eval job exists in any workflow today.
- ADR-0004 says "Each suite is its own gate job." That is untrue of the eval suite under this decision.
- ADR-0004 says only the eval suite reaches a model, and LAW-000011 says each suite runs separately from the others. Both stay true.
- Coverage from the eval suite is already absent by design (ADR-0003).
- Without a CI run, nothing checks that a contributor ran the evals. A reviewer's judgment covers it, and the contributor guide says when to run them.
- A gate cannot fail a pull request on an eval result. The final job of `gates.yml` does not list an eval job.
- Running evals in CI would need a model credential held as a repository secret. The user declined to use their Claude subscription for CI.
- `CONTRIBUTING.md` will say which command runs the evals. The command itself is unknown, because the eval suite has no code yet.

Alternative: a gate job that runs the evals with a credential from a repository secret. Alternative: a scheduled or manual workflow that runs them. Alternative: no change to the ADRs.
