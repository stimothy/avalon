"""Command line of the gates: `python -m devtools.gates tracked | secrets | pull-request`."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from devtools.adapters.gh import GhError, RealGh
from devtools.adapters.git import GitError, RealGit
from devtools.adapters.process import RealProcess
from devtools.gates import (
    changed_paths,
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


def run(argv: list[str], root: Path) -> int:
    parser = argparse.ArgumentParser(prog="devtools.gates")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("tracked")
    sub.add_parser("secrets")
    pull = sub.add_parser("pull-request")
    pull.add_argument("--title", required=True)
    pull.add_argument("--body", required=True)
    changes = sub.add_parser("changed-paths")
    source = changes.add_mutually_exclusive_group(required=True)
    source.add_argument("--base")
    source.add_argument("--pr", type=int)
    verdict_parser = sub.add_parser("verdict")
    verdict_parser.add_argument("--needs", required=True, help="the needs context, as JSON")
    verdict_parser.add_argument("--filter-job", default="changes")
    verdict_parser.add_argument("--gate", action="append", default=[], help="job=output")
    sub.add_parser("workflows")
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
    if args.command == "verdict":
        gated = dict(item.split("=", 1) for item in args.gate)
        needs = json.loads(args.needs)
        return _report(verdict.judge(needs, gated, args.filter_job))
    if args.command == "workflows":
        problems: list[str] = []
        for workflow in sorted((root / ".github" / "workflows").glob("*.yml")):
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
