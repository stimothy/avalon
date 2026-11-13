"""Command line of the gates: `python -m devtools.gates tracked | secrets | pull-request`."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

from devtools.adapters import download
from devtools.adapters.gh import GhError, RealGh
from devtools.adapters.git import GitError, RealGit
from devtools.adapters.process import RealProcess
from devtools.gates import (
    changed_paths,
    gitleaks_install,
    interpreter,
    pr_labels,
    secret_scan,
    text_scan,
    tracked_scan,
    verdict,
    workflow_check,
)


def _read_text(root: Path, path: str) -> str | None:
    try:
        return (root / path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _report(lines: list[str]) -> int:
    for line in lines:
        print(line)
    return 1 if lines else 0


def run(
    argv: list[str],
    root: Path,
    fetch: gitleaks_install.Fetch = download.fetch,
    extract: gitleaks_install.Extract = download.extract_member,
) -> int:
    parser = argparse.ArgumentParser(prog="devtools.gates")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("tracked")
    sub.add_parser("secrets")
    pull = sub.add_parser("pull-request")
    pull.add_argument("--title", required=True)
    pull.add_argument("--body", required=True)
    labels = sub.add_parser("pr-labels")
    labels.add_argument("--pr", type=int, required=True)
    changes = sub.add_parser("changed-paths")
    source = changes.add_mutually_exclusive_group(required=True)
    source.add_argument("--base")
    source.add_argument("--pr", type=int)
    verdict_parser = sub.add_parser("verdict")
    verdict_parser.add_argument("--needs", required=True, help="the needs context, as JSON")
    verdict_parser.add_argument("--filter-job", default="changes")
    verdict_parser.add_argument("--gate", action="append", default=[], help="job=output")
    sub.add_parser("workflows")
    install = sub.add_parser("install-gitleaks")
    install.add_argument("--dest", required=True)
    install.add_argument("--path-file", help="a file to which the install folder is appended")
    python = sub.add_parser("interpreter")
    python.add_argument("--expect", required=True, help="the major.minor version, such as 3.9")
    args = parser.parse_args(argv)

    process = RealProcess()
    git = RealGit(process, str(root))
    try:
        if args.command == "changed-paths":
            paths = (
                git.changed_files(args.base)
                if args.base
                else RealGh(process, str(root)).changed_files(args.pr)
            )
            print("\n".join(changed_paths.render(changed_paths.outputs(paths))))
            return 0
    except (GitError, GhError) as error:
        print(error, file=sys.stderr)
        return 2
    if args.command == "pr-labels":
        try:
            return _report(pr_labels.check(git, RealGh(process, str(root), os.environ), args.pr))
        except (GitError, GhError) as error:
            print(error, file=sys.stderr)
            return 2
    if args.command == "interpreter":
        return _report(interpreter.check(args.expect, tuple(sys.version_info[:3])))
    if args.command == "install-gitleaks":
        try:
            installed = gitleaks_install.install(
                fetch, extract, platform.system(), platform.machine(), args.dest
            )
        except (gitleaks_install.InstallError, OSError) as error:
            print(error, file=sys.stderr)
            return 2
        if args.path_file:
            with open(args.path_file, "a", encoding="utf-8") as handle:
                handle.write(str(Path(installed).parent) + "\n")
        print(installed)
        return 0
    if args.command == "verdict":
        gated = dict(item.split("=", 1) for item in args.gate)
        needs = json.loads(args.needs)
        return _report(verdict.judge(needs, gated, args.filter_job))
    if args.command == "workflows":
        problems: list[str] = []
        folder = root / ".github" / "workflows"
        for workflow in sorted([*folder.glob("*.yml"), *folder.glob("*.yaml")]):
            problems += workflow_check.check(workflow.name, workflow.read_text(encoding="utf-8"))
        return _report(problems)
    if args.command == "tracked":
        found = tracked_scan.scan_tracked_files(git, lambda p: _read_text(root, p))
        return _report([f.render() for f in found])
    if args.command == "pull-request":
        return _report([f.render() for f in text_scan.scan_pull_request(args.title, args.body)])
    try:
        return _report(secret_scan.scan_secrets(git, process, str(root)))
    except secret_scan.ToolMissingError as error:
        print(error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:], Path.cwd()))
