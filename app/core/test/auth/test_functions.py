from datetime import timedelta
from unittest import TestCase

from fastapi import HTTPException

from app.core.auth.functions import (
    create_access_token,
    create_jwt_token,
    get_current_admin,
    get_current_user,
    hash_password,
    verify_password,
    verify_refresh_token,
)


class TestPassword(TestCase):
    def test_verify_password_ok(self):
        password_plain = "test"
        password_hashed = hash_password(password_plain)

        if not verify_password(password_plain, password_hashed):
            raise AssertionError("Password verification failed.")

    def test_verify_password_ko(self):
        password_plain = "test"
        password_hashed = hash_password(password_plain)

        if verify_password("incorrect_password", password_hashed):
            raise AssertionError("Password verification should fail.")


class TestToken(TestCase):
    def test_create_token(self):
        access_token = create_access_token(username="test")
        if type(access_token) != str:
            raise AssertionError("Access token should be of type str.")

    def test_get_current_user_ok(self):
        access_token = create_access_token(username="test")
        username = get_current_user(access_token)
        if username != "test":
            raise AssertionError("Username should be 'test'.")

    def test_get_current_user_no_username(self):
        access_token = create_jwt_token(
            data={}, expiration_delta=timedelta(minutes=30)
        )
        with self.assertRaises(HTTPException):
            get_current_user(access_token)

    def test_get_current_user_invalid_signature(self):
        with self.assertRaises(HTTPException):
            get_current_user("invalid_token")

    def test_get_current_user_expired_signature(self):
        access_token = create_jwt_token(
            data={}, expiration_delta=timedelta(minutes=-30)
        )
        with self.assertRaises(HTTPException):
            get_current_user(access_token)

    def test_get_current_admin_ok(self):
        access_token = create_access_token(username="test")
        username = get_current_admin(access_token)
        if username != "test":
            raise AssertionError("Username should be 'test'.")

    def test_get_current_admin_no_username(self):
        access_token = create_jwt_token(
            data={}, expiration_delta=timedelta(minutes=30)
        )
        username = get_current_admin(access_token)
        if username is not None:
            raise AssertionError("Username should be None.")

    def test_get_current_admin_invalid_signature(self):
        username = get_current_admin("incorrect_token")
        if username is not None:
            raise AssertionError("Username should be None.")

    def test_get_current_admin_expired_signature(self):
        access_token = create_jwt_token(
            data={}, expiration_delta=timedelta(minutes=-30)
        )
        username = get_current_admin(access_token)
        if username is not None:
            raise AssertionError("Username should be None.")

    def test_verify_refresh_token_ok(self):
        payload = {"scopes": "refresh_token"}
        token = create_jwt_token(
            data=payload, expiration_delta=timedelta(minutes=30)
        )
        if payload != verify_refresh_token(token):
            raise AssertionError(
                "Payload should match the result of verify_refresh_token."
            )

    def test_verify_refresh_token_no_scopes(self):
        payload = {}
        token = create_jwt_token(
            data=payload, expiration_delta=timedelta(minutes=30)
        )
        if payload != verify_refresh_token(token):
            raise AssertionError(
                "Payload should match the result of verify_refresh_token."
            )

    def test_verify_refresh_token_invalid_signature(self):
        if verify_refresh_token("invalid_token") is not None:
            raise AssertionError("Invalid token should return None.")

    def test_verify_refresh_token_expired_signature(self):
        payload = {"scopes": "refresh_token"}
        token = create_jwt_token(
            data=payload, expiration_delta=timedelta(minutes=-30)
        )
        if verify_refresh_token(token) is not None:
            raise AssertionError(
                "Refresh token verification should return None."
            )
