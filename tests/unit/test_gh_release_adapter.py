from __future__ import annotations

import json

import pytest

from devtools.adapters.gh import GhError, PullRequest, RealGh
from devtools.adapters.process import Completed
from fakes.gate_fakes import FakeProcess

_PULLS = json.dumps(
    [
        {"number": 4, "merged_at": "2026-11-13T00:00:00Z", "labels": [{"name": "patch"}]},
        {"number": 5, "merged_at": None, "labels": [{"name": "minor"}]},
    ]
)


def test_merged_pull_requests_keeps_only_merged_ones_with_their_labels() -> None:
    process = FakeProcess(default=Completed(0, _PULLS, ""))

    pulls = RealGh(process, "/repo").merged_pull_requests("abc")

    assert pulls == [PullRequest(4, ["patch"])]


def test_merged_pull_requests_asks_the_commit_endpoint() -> None:
    process = FakeProcess(default=Completed(0, "[]", ""))

    RealGh(process, "/repo").merged_pull_requests("abc")

    assert process.calls == [["gh", "api", "repos/{owner}/{repo}/commits/abc/pulls"]]


def test_pull_request_reads_the_labels_it_carries() -> None:
    out = json.dumps({"number": 6, "labels": [{"name": "major"}, {"name": "bug"}]})
    process = FakeProcess(default=Completed(0, out, ""))

    pull = RealGh(process, "/repo").pull_request(6)

    assert pull == PullRequest(6, ["major", "bug"])


def test_a_release_that_exists_is_found() -> None:
    process = FakeProcess()

    found = RealGh(process, "/repo").release_exists("v0.1.0")

    assert found is True


def test_a_release_that_is_not_found_does_not_exist() -> None:
    process = FakeProcess(default=Completed(1, "", "release not found\n"))

    found = RealGh(process, "/repo").release_exists("v0.1.0")

    assert found is False


def test_any_other_failure_of_the_release_lookup_is_raised() -> None:
    process = FakeProcess(default=Completed(1, "", "bad credentials\n"))

    with pytest.raises(GhError, match="bad credentials"):
        RealGh(process, "/repo").release_exists("v0.1.0")


def test_create_release_makes_the_tag_and_release_in_one_call() -> None:
    process = FakeProcess()

    RealGh(process, "/repo").create_release("v0.1.0", "abc", "notes")

    assert process.calls == [
        [
            "gh",
            "release",
            "create",
            "v0.1.0",
            "--target",
            "abc",
            "--title",
            "v0.1.0",
            "--notes",
            "notes",
            "--generate-notes",
        ]
    ]


def test_create_release_raises_when_gh_fails() -> None:
    process = FakeProcess(default=Completed(1, "", "tag exists\n"))

    with pytest.raises(GhError, match="tag exists"):
        RealGh(process, "/repo").create_release("v0.1.0", "abc", "notes")


def test_a_variable_is_read_without_its_newline() -> None:
    process = FakeProcess(default=Completed(0, "true\n", ""))

    value = RealGh(process, "/repo").variable("ALLOW_PRE_1_MAJOR")

    assert value == "true"


def test_a_variable_that_is_not_set_is_none() -> None:
    process = FakeProcess(default=Completed(1, "", "variable ALLOW not found\n"))

    value = RealGh(process, "/repo").variable("ALLOW")

    assert value is None


def test_any_other_failure_of_the_variable_lookup_is_raised() -> None:
    process = FakeProcess(default=Completed(1, "", "forbidden\n"))

    with pytest.raises(GhError, match="forbidden"):
        RealGh(process, "/repo").variable("ALLOW")
