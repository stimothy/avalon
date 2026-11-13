from __future__ import annotations

import hashlib

import pytest

from devtools.gates import gitleaks_install, gitleaks_pin


class FakeFetch:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.urls: list[str] = []

    def __call__(self, url: str) -> bytes:
        self.urls.append(url)
        return self.data


class FakeExtract:
    def __init__(self) -> None:
        self.calls: list[tuple[bytes, str, str]] = []

    def __call__(self, data: bytes, member: str, dest: str) -> str:
        self.calls.append((data, member, dest))
        return f"{dest}/{member}"


def _pin(data: bytes) -> dict[str, str]:
    return {"linux_x64": hashlib.sha256(data).hexdigest()}


def test_the_archive_is_fetched_from_the_pinned_version() -> None:
    fetch = FakeFetch(b"archive")

    gitleaks_install.install(
        fetch, FakeExtract(), "Linux", "x86_64", "/d", _pin(b"archive"), "9.9.9"
    )

    assert fetch.urls == [
        "https://github.com/gitleaks/gitleaks/releases/download/v9.9.9/gitleaks_9.9.9_linux_x64.tar.gz"
    ]


def test_a_matching_checksum_extracts_the_tool() -> None:
    extract = FakeExtract()

    path = gitleaks_install.install(
        FakeFetch(b"archive"), extract, "Linux", "x86_64", "/d", _pin(b"archive"), "9.9.9"
    )

    assert (path, extract.calls) == ("/d/gitleaks", [(b"archive", "gitleaks", "/d")])


def test_a_wrong_checksum_extracts_nothing() -> None:
    extract = FakeExtract()

    with pytest.raises(gitleaks_install.InstallError, match="checksum"):
        gitleaks_install.install(
            FakeFetch(b"tampered"), extract, "Linux", "x86_64", "/d", _pin(b"archive"), "9.9.9"
        )

    assert extract.calls == []


def test_an_unknown_platform_is_refused() -> None:
    with pytest.raises(gitleaks_install.InstallError, match="no pinned build"):
        gitleaks_install.install(FakeFetch(b""), FakeExtract(), "Plan9", "mips", "/d", {}, "9.9.9")


@pytest.mark.parametrize(
    ("system", "machine", "key"),
    [
        ("Darwin", "arm64", "darwin_arm64"),
        ("Darwin", "x86_64", "darwin_x64"),
        ("Linux", "AMD64", "linux_x64"),
    ],
)
def test_platform_names_map_to_release_names(system: str, machine: str, key: str) -> None:
    found = gitleaks_install.platform_key(system, machine)

    assert found == key


def test_every_pinned_platform_has_a_sha256_checksum() -> None:
    sums = list(gitleaks_pin.CHECKSUMS.values())

    assert all(len(s) == 64 and int(s, 16) >= 0 for s in sums)
