import pytest
from fastapi.responses import RedirectResponse

from app.core.admin.auth import AdminAuth
from app.core.auth.functions import create_access_token
from app.settings import settings


class MockRequest:
    def __init__(self, form_data=None, session=None):
        self.form_data = form_data or {}
        self.session = session or {}

    async def form(self):
        return self.form_data

    async def url_for(self, url):
        return "whatever"


@pytest.fixture
def admin_auth():
    return AdminAuth(secret_key="secret_key")


@pytest.fixture
def valid_token():
    return create_access_token(username=settings.admin_user)


@pytest.mark.asyncio
async def test_admin_auth_login_successful(admin_auth):
    mock_request = MockRequest(
        form_data={
            "username": settings.admin_user,
            "password": settings.admin_pass,
        }
    )

    result = await admin_auth.login(mock_request)

    if result is not True:
        raise AssertionError("Expected result to be True, but it was not.")


@pytest.mark.asyncio
async def test_admin_auth_login_failed(admin_auth):
    mock_request = MockRequest(
        form_data={
            "username": "invalid_username",
            "password": "invalid_password",
        }
    )

    result = await admin_auth.login(mock_request)

    if result is not True:
        raise AssertionError("Expected result to be True, but it was not.")


@pytest.mark.asyncio
async def test_admin_auth_logout(admin_auth):
    mock_request = MockRequest()

    result = await admin_auth.logout(mock_request)

    if result is not True:
        raise AssertionError("Expected result to be True, but it was not.")


@pytest.mark.asyncio
async def test_admin_auth_authenticate_valid_token(admin_auth, valid_token):
    mock_request = MockRequest(session={"token": valid_token})

    result = await admin_auth.authenticate(mock_request)

    if result is not None:
        raise AssertionError("Expected result to be None, but it was not.")


@pytest.mark.asyncio
async def test_admin_auth_authenticate_invalid_token(admin_auth):
    mock_request = MockRequest(session={"token": "invalid_token"})

    result = await admin_auth.authenticate(mock_request)

    if not isinstance(result, RedirectResponse):
        raise AssertionError(
            "Expected result to be an instance of RedirectResponse."
        )

    if result.status_code != 302:
        raise AssertionError("Expected status code to be 302, but it was not.")
