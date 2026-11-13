"""Command line of the release code: `python -m devtools.release release | dry-run --pr N`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from devtools.adapters.gh import GhError, GhPort, RealGh
from devtools.adapters.git import GitError, GitPort, RealGit
from devtools.adapters.process import RealProcess
from devtools.release import run as release_run


def run(argv: list[str], git: GitPort, gh: GhPort) -> int:
    parser = argparse.ArgumentParser(prog="devtools.release")
    sub = parser.add_subparsers(dest="command", required=True)
    walk = sub.add_parser("release")
    walk.add_argument("--ref", default="HEAD", help="the commit to walk back from")
    dry = sub.add_parser("dry-run")
    dry.add_argument("--pr", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "dry-run":
            print(release_run.dry_run(git, gh, args.pr))
        else:
            for made in release_run.release(git, gh, args.ref):
                print(f"{made.tag} at {made.commit}")
    except release_run.ReleaseStopError as stop:
        print(stop)
        return 1
    except (GitError, GhError) as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    _process = RealProcess()
    _root = str(Path.cwd())
    sys.exit(run(sys.argv[1:], RealGit(_process, _root), RealGh(_process, _root)))
