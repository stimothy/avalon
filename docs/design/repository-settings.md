---
summary: The GitHub settings of this repo, the command that applies each one, and the rule that an agent runs such a command only after the owner approves it.
covers: [.github/CODEOWNERS]
verified: 2026-11-13
verified_commit: 1c675793f174975d556bef5fcfd79866aaa6ebf0
---
# Repository settings

The settings below live on GitHub, not in the repo, and no gate checks them. [ADR-0005](../adr/0005-workflows-and-gates.md) and [ADR-0006](../adr/0006-releases.md) state the rules they carry out. The owner applies them.

## Who runs a command

An agent runs a command on this page only after the owner approves that command. No setting needs a secret, so no one stores one, and no workflow calls a model.

## The ruleset on `master`

One ruleset applies to the default branch. It has no bypass actors, the owner included.

| Rule | Setting |
|---|---|
| Deletion | Blocked. |
| Non-fast-forward pushes | Blocked. |
| Pull request | Required. Squash is the only allowed merge method. A new push dismisses a stale review. Every review thread must be resolved. A code owner must review, and no approval count is required. |
| Status checks | `all-green` (the final job of `gates.yml`) and `pr` (the job of `pr.yml`) must pass, and the branch must be up to date. |

`.github/CODEOWNERS` names the owner as the code owner of every path.

To change the ruleset, read it, edit the JSON, and write it back. Replace `ID` with the ruleset's id from the first command:

```sh
gh api repos/stimothy/avalon/rulesets
gh api repos/stimothy/avalon/rulesets/ID
gh api -X PUT repos/stimothy/avalon/rulesets/ID --input ruleset.json
```

## Merges

Only squash merges are on. The commit has the pull request's title as its message and no body.

```sh
gh api -X PATCH repos/stimothy/avalon \
  -F allow_squash_merge=true -F allow_merge_commit=false -F allow_rebase_merge=false \
  -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=BLANK
```

## Labels

The four labels `major`, `minor`, `patch`, and `none` exist. The command that created the first three is unknown. The fourth was made with:

```sh
gh label create none --description "No release" --color ededed
```

A maintainer sets the label of each pull request ([the release code](release.md)).

## Private vulnerability reporting

It is on. The security policy and the conduct reports use it.

```sh
gh api -X PUT repos/stimothy/avalon/private-vulnerability-reporting
```

## The variable that allows `major`

`ALLOW_PRE_1_MAJOR` is not set, so the release code refuses `major` below `v1.0.0`. Only the owner sets it, for the pull request that makes `v1.0.0`:

```sh
gh variable set ALLOW_PRE_1_MAJOR --body true
```
