from unittest import TestCase
from unittest.mock import (
    patch,
    MagicMock,
)

from jose import jwt
from datetime import timedelta
from fastapi import HTTPException

from app.core.auth.functions import (
    hash_password,
    verify_password,
    create_jwt_token,
    create_access_token,
    get_current_admin,
    get_current_user,
    verify_refresh_token,
)


class TestPassword(TestCase):

    def test_verify_password_ok(self):
        password_plain = "test"
        password_hashed = hash_password(password_plain)

        assert verify_password(password_plain, password_hashed)

    def test_verify_password_ko(self):
        password_plain = "test"
        password_hashed = hash_password(password_plain)

        assert not verify_password("incorrect_password", password_hashed)


class TestToken(TestCase):

    def test_create_token(self):
        access_token = create_access_token(username="test")
        assert str == type(access_token)

    def test_get_current_user_ok(self):
        access_token = create_access_token(username="test")
        username = get_current_user(access_token)
        assert "test" == username

    def test_get_current_user_no_username(self):
        access_token = create_jwt_token(data={}, expiration_delta=timedelta(minutes=30))
        with self.assertRaises(HTTPException):
            get_current_user(access_token)

    def test_get_current_user_invalid_signature(self):
        with self.assertRaises(HTTPException):
            get_current_user("invalid_token")

    def test_get_current_user_expired_signature(self):
        access_token = create_jwt_token(data={}, expiration_delta=timedelta(minutes=-30))
        with self.assertRaises(HTTPException):
            get_current_user(access_token)

    def test_get_current_admin_ok(self):
        access_token = create_access_token(username="test")
        username = get_current_admin(access_token)
        assert "test" == username

    def test_get_current_admin_no_username(self):
        access_token = create_jwt_token(data={}, expiration_delta=timedelta(minutes=30))
        username = get_current_admin(access_token)
        assert username is None

    def test_get_current_admin_invalid_signature(self):
        username = get_current_admin("incorrect_token")
        assert username is None

    def test_get_current_admin_expired_signature(self):
        access_token = create_jwt_token(data={}, expiration_delta=timedelta(minutes=-30))
        username = get_current_admin(access_token)
        assert username is None

    def test_verify_refresh_token_ok(self):
        payload = {"scopes": "refresh_token"}
        token = create_jwt_token(data=payload, expiration_delta=timedelta(minutes=30))
        assert payload == verify_refresh_token(token)

    def test_verify_refresh_token_no_scopes(self):
        payload = {}
        token = create_jwt_token(data=payload, expiration_delta=timedelta(minutes=30))
        assert verify_refresh_token(token) is None

    def test_verify_refresh_token_invalid_signature(self):
        assert verify_refresh_token("invalid_token") is None

    def test_verify_refresh_token_expired_signature(self):
        payload = {"scopes": "refresh_token"}
        token = create_jwt_token(data=payload, expiration_delta=timedelta(minutes=-30))
        assert verify_refresh_token(token) is None
