from backend.security import (
    is_loopback_host,
    parse_bearer_token,
    token_is_valid,
)


def test_is_loopback_host() -> None:
    assert is_loopback_host("127.0.0.1")
    assert is_loopback_host("localhost")
    assert is_loopback_host("::1")
    assert not is_loopback_host("0.0.0.0")
    assert not is_loopback_host("192.168.1.10")


def test_parse_bearer_token() -> None:
    assert parse_bearer_token("Bearer abc123") == "abc123"
    assert parse_bearer_token("bearer abc123") == "abc123"
    assert parse_bearer_token("Basic abc123") is None
    assert parse_bearer_token(None) is None


def test_token_is_valid() -> None:
    assert token_is_valid("abc123", "abc123")
    assert not token_is_valid("abc123", "zzz")
    assert not token_is_valid(None, "abc123")
    assert not token_is_valid("abc123", None)
