"""The adapters that fetch a file and unpack an archive. Tests replace them with fakes."""

from __future__ import annotations

import io
import os
import tarfile
import urllib.request


def fetch(url: str) -> bytes:
    """Return the bytes at `url`."""
    with urllib.request.urlopen(url, timeout=60) as response:
        data: bytes = response.read()
    return data


def extract_member(data: bytes, member: str, dest: str) -> str:
    """Write one file of a gzip tar archive into `dest`, mark it executable, return its path."""
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        source = archive.extractfile(member)
        if source is None:
            raise FileNotFoundError(member)
        path = os.path.join(dest, os.path.basename(member))
        with open(path, "wb") as target:
            target.write(source.read())
    os.chmod(path, 0o755)
    return path
