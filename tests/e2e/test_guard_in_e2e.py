import socket

import pytest

import suite_guard


def test_the_guard_fails_a_connection_in_the_end_to_end_suite() -> None:
    sock = socket.socket()
    with pytest.raises(suite_guard.ForbiddenCallError):
        sock.connect(("127.0.0.1", 9))
    sock.close()
