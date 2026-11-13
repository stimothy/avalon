# Decision matter: the squash message

Kind: decision matter, one decision. Proposer: the user. Status: proposed; nothing is registered.

The user decided that a squash merge's commit message is the pull request's title only, and asked for a sitting to amend ADR-0005 to say so. The chair applies the ADR test and checks the decision against the laws and ADR-0001 to ADR-0006.

## The decision

### The squash message is the pull request's title alone (origin: user)

The ruleset on `master` allows squash merges only. The commit that a squash makes has the pull request's title as its message and no body. The pull request's description is not part of the commit.

Facts the table should weigh:

- ADR-0005 now says the squash message is the pull request's title and description. The live repository setting is the title with a blank message, so the ADR is the part that is untrue.
- `pr.yml` scans both the title and the body of a pull request for plan citations. Neither ADR-0005 nor the design doc for the workflows states why the body is scanned, so the reason is unknown.
- ADR-0006 and the release code read the labels of the merged pull request, not the commit message. GitHub's generated release notes list pull request titles.
- ADR-0005 rejects "the default squash message" with the reason unknown.
- The body of a pull request stays on GitHub after the merge, and a title is one line.

Alternative: title and description (the current ADR text). Alternative: the default message GitHub builds from the branch's commits. Alternative: no change.
