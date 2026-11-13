"""Command line of the gates: `python -m devtools.gates tracked | secrets | pull-request`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from devtools.adapters.git import RealGit
from devtools.adapters.process import RealProcess
from devtools.gates import secret_scan, text_scan, tracked_scan


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
    args = parser.parse_args(argv)

    process = RealProcess()
    git = RealGit(process, str(root))
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
