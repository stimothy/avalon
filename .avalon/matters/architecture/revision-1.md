# The slate for the vote

Eight decisions, one vote each. Tooling, test suites, workflows, and release are not in this slate; a later sitting hears them. The decisions below do fix the script's language, its Python floor, and its dependency rule.

## 1. Judgment in prompts, mechanics in one script (origin: user)

Agents and skills hold procedure and judgment: what is a law, how a line is worded, how a seat votes. One script does every repeatable step and every write to the record. The script never calls a model. A skill or agent never does by hand a step that a script command does. It names the command instead.

Alternatives: agents do the mechanical steps themselves; a script that calls a model.

## 2. A plugin of three layers in a self-contained folder (origin: agent)

Avalon is a Claude Code plugin with three layers: skills for procedure, agents for judgment, and the script for mechanics. A layer calls its own layer and the layers below it. The guard hook is a command of the script, not a fourth layer. The plugin is installed from the public repo, has no server, and collects nothing. The plugin folder holds only what a user installs and reads nothing outside itself. Tests, fixtures, eval cases, development tools, and workflows live outside it.

Alternatives: a standalone command-line tool; instructions only, with no script; one root with everything together, filtered at install.

## 3. The script is Python on the standard library only (origin: agent)

The script has one entry file that holds no logic and hands over to a package. The package imports only the standard library and itself, runs on Python 3.9 and later, opens no network connection, and uses no randomness. The script is never put on the PATH.

Alternatives: one file of several thousand lines; a package with third-party dependencies; a different language.

## 4. A pure core, with files, git, and the clock behind ports (origin: agent)

The script's decisions, parsing, and rendering do no input or output. Commands reach files, git, and the time only through ports. Only the real file adapter touches the file system, and only the real git adapter starts a process. One layer reads the arguments and chooses the adapters.

Alternative: commands call the file system and git directly.

## 5. A writing command is one all-or-nothing change set (origin: agent)

A command that writes builds its whole change set in memory and checks it. It saves the set to a journal, then applies it. It holds one exclusive lock for its whole run. Each file is replaced atomically, and the config file with its new checksum goes last. A refusal changes no file. The next writing command repairs a crash.

Alternatives: write each file as the command goes; no lock or journal.

## 6. One home for each format, one writer for each file (origin: agent)

One module parses and renders every governed file. A template is the only home of a format's fixed text. Every file under the record has one named writer: the script, the chair, the tech writer, the prose editor, or the user. A writer not named for a path does not write it.

Alternatives: each command parses and writes its own files; no template, with fixed text in code.

## 7. A hook guards the record, and the user's authority is a flag (origin: agent)

A hook, which is a command of the script, denies direct writes to the laws folder, the config file, and the script's working files. The user's authority is one leading flag, and the script refuses the command without it. The hook never pre-approves a flagged command, and the chair never runs one. The hook approves only the plugin's own everyday commands. The flag never takes the place of a round table where a law requires one. In a repo where the plugin is not installed, the hook does not act, and records are written by hand under the stand-in process.

Alternatives: no hook, relying on instructions and the checksum; pre-approving the script's commands by a skill setting.

## 8. One module reads git, and nothing writes it (origin: user)

One module runs a fixed list of read-only git commands. Everything else sees git only as a port. No agent and no script command commits, branches, or tags. The session that asked for the work owns git.

Alternatives: the script commits its own changes; several modules call git.

## Sorted out as failing the ADR test

How the script finds the config file and the root; the closed list of command names and exit codes; where each piece of prompt text lives; the manifest and marketplace details. Each gets a design doc once its code exists. Work in progress as a matter folder is a process decision and goes to its own matter.
