Nothing in this file is in effect. It lists every law that was amended or removed.

| ID | Status | Text | Date | Replaced by | Now in effect | Reason |
|---|---|---|---|---|---|---|
| LAW-000016 | Amended | Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding. | 2026-11-12 | LAW-000017 | LAW-000018 | A comment such as `# type: ignore` could empty the law, so the law bars turning off a check outside `pyproject.toml`. |
| LAW-000017 | Amended | Python this repo authors passes the format check, linter, and type checker that the tool-choice ADR (ADR-0003) names, with no finding, and turns off a check only in `pyproject.toml`. | 2026-11-12 | LAW-000018 | LAW-000018 | The wording read as if Python turns off a check, so it now says that no check is turned off outside `pyproject.toml`. |
