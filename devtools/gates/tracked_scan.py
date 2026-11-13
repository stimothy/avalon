"""The scan of tracked files: plan citations and home paths."""

from __future__ import annotations

from collections.abc import Callable

from devtools.adapters.git import GitPort
from devtools.gates import skip_list, text_scan
from devtools.gates.text_scan import Finding

# Returns a file's text, or None when the file is missing or is not text.
Reader = Callable[[str], "str | None"]


def scan_tracked_files(git: GitPort, read: Reader) -> list[Finding]:
    """Scan every tracked text file that the skip list does not skip."""
    found: list[Finding] = []
    for path in git.tracked_files():
        if skip_list.is_skipped(path):
            continue
        text = read(path)
        if text is not None:
            found.extend(text_scan.scan_file(path, text))
    return found
