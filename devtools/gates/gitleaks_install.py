"""Install the pinned gitleaks: fetch the archive, check its checksum, then extract it."""

from __future__ import annotations

import hashlib
from collections.abc import Callable

from devtools.gates import gitleaks_pin

URL = "https://github.com/gitleaks/gitleaks/releases/download/v{v}/gitleaks_{v}_{key}.tar.gz"
SYSTEMS = {"Darwin": "darwin", "Linux": "linux"}
MACHINES = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "x64", "amd64": "x64"}

Fetch = Callable[[str], bytes]
Extract = Callable[[bytes, str, str], str]


class InstallError(RuntimeError):
    """Raised when gitleaks cannot be installed as pinned."""


def platform_key(system: str, machine: str) -> str:
    """Return the release name of a platform, such as `linux_x64`."""
    return f"{SYSTEMS.get(system, system)}_{MACHINES.get(machine.lower(), machine)}"


def install(
    fetch: Fetch,
    extract: Extract,
    system: str,
    machine: str,
    dest: str,
    checksums: dict[str, str] | None = None,
    version: str = gitleaks_pin.VERSION,
) -> str:
    """Return the path of the installed tool; raise InstallError on a bad platform or checksum."""
    sums = gitleaks_pin.CHECKSUMS if checksums is None else checksums
    key = platform_key(system, machine)
    if key not in sums:
        raise InstallError(f"no pinned build of gitleaks for {key}")
    data = fetch(URL.format(v=version, key=key))
    if hashlib.sha256(data).hexdigest() != sums[key]:
        raise InstallError(f"the checksum of the gitleaks archive for {key} does not match")
    return extract(data, "gitleaks", dest)
