import pytest
from unittest.mock import patch, MagicMock
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.db.session import DBSessionMiddleware, db


engine = create_engine(
    "sqlite://", echo=False, connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(scope="session")
def db_mocked():
    # Set global session variables
    from app.main import app
    DBSessionMiddleware(app, custom_engine=engine)

    # Create tables
    SQLModel.metadata.create_all(engine)

    with db():
        yield db


@pytest.fixture(scope="session")
def db_mocked_app_client():
    with patch(
            "app.main.get_engine", MagicMock()
    ) as mock_get_engine:
        mock_get_engine.return_value = engine

        # Create APP client
        from app.main import app, get_engine
        app.add_middleware(DBSessionMiddleware, custom_engine=get_engine())
        client = TestClient(app)

        # Create tables
        SQLModel.metadata.create_all(engine)

        yield client


@pytest.fixture(scope="session")
def user_mocked_info(db_mocked_app_client):
    user_info = {
            "username": "user_mock@anyprovider.com",
            "password": "pass_mock"
        }
    response = db_mocked_app_client.post(
        url="user/register",
        json=user_info
    )
    assert 201 == response.status_code

    # Login
    response = db_mocked_app_client.post(
        url="user/login",
        data={
            "username": user_info["username"],
            "password": user_info["password"]
        },

    )

    assert 200 == response.status_code

    user_info["access_token"] = response.json()["access_token"]
    user_info["refresh_token"] = response.json()["refresh_token"]
    user_info["token_type"] = response.json()["token_type"]

    return user_info
