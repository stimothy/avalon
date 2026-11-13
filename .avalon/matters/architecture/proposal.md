# Decision matter: the architecture

Kind: decision matter, one slate. Proposer: the planning work reasoned most of it from the user's rules, so the user is offered the outcome to confirm. Status: a stand-in round table heard the slate in two rounds. All nine decisions are recorded in ADR-0001, each 5 approve, 0 amend, 0 reject. The user accepted the table's wording of the two held decisions and confirmed ADR-0001, so its origin is `user`.

## Held for the user

The table reworded both decisions that the user stated, so nothing is registered until the user accepts the table's wording, counters, or directs that each be registered as written. The table's wording is in `revision-2.md`, and the decision numbers below are the numbers there: decisions 1 and 9. The slate further down is the first draft, kept as it was proposed; the screening and two rounds changed its numbering and wording.

- Judgment in prompts, mechanics in one script. The table added that ADR-0002 applies where the plugin is not installed.
- One module reads git, and nothing writes it. The table made it refer to the port of the pure-core decision instead of restating it.

## Sorted out for design docs

How the script finds the config file and the root; the closed lists of command names, exit codes, and everyday commands; where each piece of prompt text lives; the manifest and marketplace details; the journal, the lock, atomic replacement, and the text a refused command prints. Work in progress as a matter folder is a process decision and needs its own matter.

## Offered to the user

ADR-0001 has origin `agent`. The user may confirm it, which makes the origin `user`, adds a `(user)` changelog line, and adds one ledger row decided by `user`.

The sitting seats the Practitioner, the Skeptic, the Jurist, the Steward, and the Scout. The Skeptic argues the strongest alternative for each decision, including doing nothing.

## How to read the slate

Each decision is proposed to become part of one ADR, `0001-architecture`. Each has its own vote. The origin is `user` where the user stated the call and `agent` where the planning work reasoned it.

The chair first applies the ADR test to each: costly to reverse, and real alternatives that a later reader would ask about. A call that fails goes to the list at the end and gets a design doc once its code exists.

## The decisions

### 1. Judgment in prompts, mechanics in one script (origin: user)

Agents and skills hold procedure and judgment: what is a law, how a line is worded, how a seat votes. One script does every repeatable step and every write to the record. The script never calls a model. A skill or agent never does by hand what a script command does, and names the command instead.

Alternative: agents do the mechanical steps themselves. Alternative: a script that calls a model.

### 2. Form: a plugin of three layers (origin: agent)

Avalon is a Claude Code plugin with three layers: skills for procedure, agents for judgment, and the script for mechanics. A layer calls its own layer and the ones below it. The guard hook is a command of the script, not a fourth layer. The plugin is installed from the public repo. It has no server and collects nothing.

Alternative: a standalone command-line tool. Alternative: instructions only, with no script.

### 3. One entry file, a package beside it, the standard library only (origin: agent)

The script has one entry file that holds no logic and hands over to a package. The package imports only the standard library and itself, runs on Python 3.9 and later, opens no network connection, and uses no randomness. The script is never put on the PATH.

Alternative: one file of several thousand lines. Alternative: a package with third-party dependencies. Alternative: a different language.

### 4. A pure core, with files, git, and the clock behind ports (origin: agent)

The script's decisions and its parsing and rendering do no input or output. Commands reach files, git, and the time only through ports. Only the real file adapter touches the file system, and only the real git adapter starts a process. One layer reads arguments and chooses adapters.

Alternative: commands call the file system and git directly.

### 5. A command is one all-or-nothing change set (origin: agent)

A command that writes builds its whole change set in memory and checks it. It saves the set to a journal, then applies it. It holds one exclusive lock for its whole run. Each file is replaced atomically, and the config file with the new checksum goes last. A refusal changes no file. A crash is repaired by the next writing command.

Alternative: write each file as the command goes. Alternative: no lock or journal.

### 6. One home for each format, one writer for each file (origin: agent)

One module parses and renders every governed file. A template is the only home of a format's fixed text. Every file under the record has one named writer: the script, the chair, the tech writer, the prose editor, or the user. A writer not named for a path does not write it.

Alternative: each command parses and writes its own files. Alternative: no template, with fixed text in code.

### 7. A hook guards the record, and the user's authority is a flag (origin: agent)

A hook that is a command of the script denies a direct write to the laws folder, the config file, and the script's working files. The user's authority is one leading flag that the script refuses without. The hook never pre-approves a flagged command, and the chair never runs one. The hook approves only the plugin's own everyday commands.

Alternative: no hook, and rely on instructions and the checksum. Alternative: pre-approve the script's commands by a skill setting.

### 8. One module reads git, and nothing writes it (origin: user)

One module runs a fixed list of read-only git commands. Everything else sees git only as a port. No agent and no script command commits, branches, or tags. The session that asked for the work owns git.

Alternative: the script commits its own changes. Alternative: several modules call git.

### 9. The plugin folder holds only what a user installs (origin: agent)

The plugin folder is self-contained and reads nothing outside itself. Tests, fixtures, eval cases, development tools, and workflows live outside it. The marketplace file names the plugin folder, and the manifest sets no version.

Alternative: one root with everything together, filtered at install.

## Candidates to screen out (resolved: see "Sorted out for design docs" above)

The planning work also reasoned these. The chair decided whether each passes the ADR test.

- How the script finds the config file and the root.
- That the script's command names and exit codes are a closed list, and prompts quote only commands that exist.
- Where each piece of prompt text lives.
- Work in progress as a matter, with one folder and one record, and its three states.
- The primary technologies and their versions are not decided here. Tooling is for a later sitting.
