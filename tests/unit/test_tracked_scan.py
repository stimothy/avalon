from __future__ import annotations

from devtools.gates import skip_list, tracked_scan
from fakes.gate_fakes import FakeGit

PLAN_ID = "A" + "D-" + "7"
PLAN_FILE = f"{skip_list.PLAN_FOLDERS[0]}/x.md"


def test_the_scan_reports_a_finding_and_skips_skipped_and_unreadable_files() -> None:
    texts = {
        "docs/a.md": f"line\n{PLAN_ID}\n",
        "uv.lock": PLAN_ID,
        PLAN_FILE: PLAN_ID,
        "docs/ok.md": "clean",
    }
    git = FakeGit(["docs/a.md", "uv.lock", PLAN_FILE, "docs/ok.md", "bin"])

    found = tracked_scan.scan_tracked_files(git, texts.get)

    assert [(f.path, f.line) for f in found] == [("docs/a.md", 2)]
