from __future__ import annotations

import io
import os
import tarfile
from pathlib import Path

import pytest

from devtools.adapters import download


def _archive(name: str, body: bytes) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        info = tarfile.TarInfo(name)
        info.size = len(body)
        archive.addfile(info, io.BytesIO(body))
    return buffer.getvalue()


def test_fetch_reads_the_bytes_at_a_file_url(tmp_path: Path) -> None:
    source = tmp_path / "a.bin"
    source.write_bytes(b"abc")

    data = download.fetch(source.as_uri())

    assert data == b"abc"


def test_extract_member_writes_an_executable_file(tmp_path: Path) -> None:
    data = _archive("gitleaks", b"binary")

    path = download.extract_member(data, "gitleaks", str(tmp_path / "bin"))

    assert (Path(path).read_bytes(), os.access(path, os.X_OK)) == (b"binary", True)


def test_extract_member_fails_on_a_missing_member(tmp_path: Path) -> None:
    data = _archive("other", b"x")

    with pytest.raises(KeyError):
        download.extract_member(data, "gitleaks", str(tmp_path))
