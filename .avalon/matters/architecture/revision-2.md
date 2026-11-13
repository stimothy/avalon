# The slate for the vote, revision 2

Nine decisions, one vote each. The old decision 7 is now two votes, 7 and 8, because the flag has its own alternatives. Tooling, test suites, workflows, and release are not in this slate. A later sitting hears them.

## 1. Judgment in prompts, mechanics in one script (origin: user)

Agents and skills hold procedure and judgment: what is a law, how a line is worded, how a seat votes. One script does every repeatable step and every write to the record. The script never calls a model. A skill or agent never does a step by hand when a script command does it. It names the command instead. Where the plugin is not installed, ADR-0002 applies and this rule does not.

Alternatives: agents do the mechanical steps themselves; a script that calls a model. The reason each lost is unknown.

## 2. A plugin of three layers in a self-contained folder (origin: agent)

Avalon is a Claude Code plugin with three layers. Skills hold procedure and sit on top. Agents hold judgment and sit in the middle. The script holds mechanics and sits at the bottom. A skill may call agents and the script. An agent may call the script. The script calls neither. The guard hook is a command of the script, not a fourth layer. The plugin is installed from the public repo, has no server, and collects nothing. The plugin folder holds the script, its templates, and everything else a user installs. It loads no code or data from outside its own folder, except the files of the repo it governs. Tests, fixtures, eval cases, development tools, and workflows live outside it.

Alternatives: a standalone command-line tool; instructions only, with no script; one root with everything together, filtered at install. The reason each lost is unknown.

## 3. The script is Python on the standard library only (origin: agent)

The script has one entry file that holds no logic and hands over to a package. The package imports only the standard library and itself, and opens no network connection. It runs on Python 3.9 and later. The reason for the 3.9 floor is unknown.

Alternatives: one file of several thousand lines; a package with third-party dependencies; a different language, with none named. The reason each lost is unknown.

## 4. A pure core, with files, git, and the clock behind ports (origin: agent)

The script's decisions, parsing, and rendering do no input or output. Commands reach files, git, and the time only through ports. Only the real file adapter touches the file system. Only the real git adapter starts a process. One layer reads the arguments and chooses the adapters.

Alternative: commands call the file system and git directly. The reason it lost is unknown.

## 5. A writing command is one all-or-nothing change set (origin: agent)

One module carries out every write, and every writing command calls it. A command that writes builds its whole change set in memory and checks it, then applies the set as one all-or-nothing change. It holds one exclusive lock for its whole run. The config file, with its new checksum, is written last. A refusal changes no file. Before a command reads or writes, it repairs any unfinished change set it finds. If it cannot repair the set, it refuses.

Alternatives: write each file as the command goes; no lock; replace each file atomically with no recovery for the whole set. The last one lost because a crash between two files leaves part of a set written. The reason the first two lost is unknown.

## 6. One home for each format, one writer for each file (origin: agent)

One module parses and renders every governed file. A template is the only home of a format's fixed text. Every file under the record has one named writer: the script, the chair, the tech writer, the prose editor, or the user. A writer not named for a path does not write it. Naming the user as a writer gives no leave to edit the laws folder outside a round table (LAW-000003). Where the plugin is not installed, the stand-in chair is the named writer (ADR-0002).

Alternatives: each command parses and writes its own files; no template, with fixed text in code. The reason each lost is unknown.

## 7. A hook guards the record (origin: agent)

The guard hook denies direct writes by any tool, the shell included, to the laws folder, the config file, and the script's working files. It approves only a closed list of the plugin's everyday commands. It never approves a flagged command ahead of time. Where the plugin is not installed, see ADR-0002.

Alternatives: no hook, relying on instructions and the checksum; approving the script's commands ahead of time through a skill setting. The reason each lost is unknown.

## 8. The user's authority is one leading flag (origin: agent)

The script refuses a command that needs the user's authority unless it carries one leading flag. Only the user runs a flagged command. No agent or skill runs one. The flag guards against mistakes. It is not a security boundary. The flag never takes the place of a round table where a law requires one.

Alternatives: a confirmation prompt; an environment variable. The reason each lost is unknown.

## 9. One module reads git, and nothing writes it (origin: user)

The git adapter of decision 4 is one module. It runs a fixed list of read-only git commands. No agent and no script command commits, branches, or tags. The session that asked for the work owns git.

Alternatives: the script commits its own changes; several modules call git. The reason each lost is unknown.

## Sorted out as failing the ADR test

How the script finds the config file and the root; the closed lists of command names, exit codes, and everyday commands; where each piece of prompt text lives; the manifest and marketplace details. Each gets a design doc once its code exists. Work in progress as a matter folder is a process decision and goes to its own matter.

## Moved to design docs

The journal and how a change set is repaired; the lock type and a stale lock; atomic replacement of each file; what a user sees when the lock is held; the text a refused command prints; that the script is never put on the PATH, and why; no randomness; how the config file is parsed without YAML.
