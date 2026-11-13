from __future__ import annotations

import hashlib
import platform
import sys
from pathlib import Path

import pytest

from devtools.gates import __main__ as gates_main
from devtools.gates import gitleaks_install, gitleaks_pin


def _extract(data: bytes, member: str, dest: str) -> str:
    return f"{dest}/{member}"


def test_install_fails_with_two_on_a_bad_checksum(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = gates_main.run(
        ["install-gitleaks", "--dest", str(tmp_path / "bin")],
        tmp_path,
        fetch=lambda url: b"tampered",
        extract=_extract,
    )

    assert code == 2
    assert capsys.readouterr().err != ""


def test_install_adds_its_folder_to_the_path_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    key = gitleaks_install.platform_key(platform.system(), platform.machine())
    monkeypatch.setitem(gitleaks_pin.CHECKSUMS, key, hashlib.sha256(b"ok").hexdigest())
    path_file = tmp_path / "path"

    code = gates_main.run(
        ["install-gitleaks", "--dest", "/d/bin", "--path-file", str(path_file)],
        tmp_path,
        fetch=lambda url: b"ok",
        extract=_extract,
    )

    assert (code, path_file.read_text(encoding="utf-8")) == (0, "/d/bin\n")
    assert capsys.readouterr().out == "/d/bin/gitleaks\n"


def test_the_interpreter_command_passes_on_the_running_version(tmp_path: Path) -> None:
    running = f"{sys.version_info.major}.{sys.version_info.minor}"

    code = gates_main.run(["interpreter", "--expect", running], tmp_path)

    assert code == 0


def test_the_interpreter_command_fails_on_another_version(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = gates_main.run(["interpreter", "--expect", "2.7"], tmp_path)

    assert code == 1
    assert "not 2.7" in capsys.readouterr().out
