from datetime import timedelta

import pytest

from app.core.security import (
    InvalidAccessTokenError,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_can_verify_original_password() -> None:
    password_hash = hash_password("a-secure-password")

    assert password_hash != "a-secure-password"
    assert verify_password("a-secure-password", password_hash) is True
    assert verify_password("incorrect-password", password_hash) is False


def test_access_token_round_trips_user_id() -> None:
    token = create_access_token(42)

    assert decode_access_token(token) == 42


def test_expired_access_token_is_rejected() -> None:
    token = create_access_token(42, expires_delta=timedelta(seconds=-1))

    with pytest.raises(InvalidAccessTokenError):
        decode_access_token(token)


def test_invalid_access_token_is_rejected() -> None:
    with pytest.raises(InvalidAccessTokenError):
        decode_access_token("not-a-jwt")
