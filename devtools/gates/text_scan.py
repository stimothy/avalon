"""Pure checks on text: plan citations and paths inside a person's home folder."""

from __future__ import annotations

import re
from dataclasses import dataclass

from devtools.gates import skip_list

PLAN_PREFIXES: tuple[str, ...] = ("REQ", "AC", "FR", "NFR", "OQ", "SM", "UJ", "AD")

# A whole, case-sensitive token: a plan prefix, a hyphen, and digits.
_PLAN_ID = re.compile(r"(?<![A-Za-z0-9_])(?:" + "|".join(PLAN_PREFIXES) + r")-\d+(?![A-Za-z0-9_])")
_PLAN_FOLDER = re.compile(
    r"(?<![\w-])(?:" + "|".join(re.escape(f) for f in skip_list.PLAN_FOLDERS) + r")(?![\w-])"
)
# A plan file named alone, as a whole token, with no folder before it.
_PLAN_FILE = re.compile(
    r"(?<![\w-])(?:" + "|".join(re.escape(f) for f in skip_list.PLAN_FILES) + r")(?![\w-])"
)
# Built in pieces, so this file does not hold a home path itself.
_UNIX_HOMES = "|".join(f"/{name}/" for name in ("Us" + "ers", "ho" + "me"))
_WINDOWS_HOME = r"(?i:[a-z]:\\" + "Us" + r"ers\\)[^\\\s`'\"]+"
_HOME_PATH = re.compile(rf"(?:{_UNIX_HOMES})[^/\s`'\"]+|{_WINDOWS_HOME}")


@dataclass(frozen=True)
class Finding:
    """One problem, with the file and the 1-based line it was found on."""

    path: str
    line: int
    kind: str
    text: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.kind}: {self.text}"


def _scan_lines(path: str, text: str, pattern: re.Pattern[str], kind: str) -> list[Finding]:
    found: list[Finding] = []
    for number, line in enumerate(text.splitlines(), start=1):
        found.extend(Finding(path, number, kind, m.group(0)) for m in pattern.finditer(line))
    return found


def plan_citations(path: str, text: str) -> list[Finding]:
    """Find plan IDs, and plan folder and file names in a file not allowed to name one."""
    found = _scan_lines(path, text, _PLAN_ID, "plan ID")
    if not skip_list.may_name_a_plan_folder(path):
        found += _scan_lines(path, text, _PLAN_FOLDER, "plan folder")
        found += _scan_lines(path, text, _PLAN_FILE, "plan file")
    return found


def home_paths(path: str, text: str) -> list[Finding]:
    """Find paths inside a person's home folder."""
    return _scan_lines(path, text, _HOME_PATH, "home path")


def scan_file(path: str, text: str) -> list[Finding]:
    """Run every text check on one tracked file."""
    return plan_citations(path, text) + home_paths(path, text)


def scan_pull_request(title: str, body: str) -> list[Finding]:
    """Check a pull request's title and body for plan citations."""
    return plan_citations("pull request title", title) + plan_citations("pull request body", body)
