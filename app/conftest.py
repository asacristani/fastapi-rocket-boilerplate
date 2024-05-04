from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pytest_alembic.config import Config
from pytest_mock_resources import create_postgres_fixture
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.db.session import DBSessionMiddleware, db


@pytest.fixture
def alembic_config():
    """Override this fixture to configure the exact
    alembic context setup required."""
    migration_path = "app/core/db/migrations/"
    return Config(
        config_options={
            "file": migration_path + "alembic.ini",
            "script_location": migration_path,
        }
    )


# Configuration of pytest mock postgres fixtures
# @pytest.fixture(scope="session")
# def pmr_postgres_config():
#     return PostgresConfig(image="postgres:16")


alembic_engine = create_postgres_fixture()

engine = create_engine(
    "sqlite://",
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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
    with patch("app.main.get_engine", MagicMock()) as mock_get_engine:
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
        "password": "pass_mock",
    }
    response = db_mocked_app_client.post(url="user/register", json=user_info)
    if response.status_code != 201:
        raise AssertionError(
            f"Expected status code 201, but got {response.status_code}"
        )

    # Login
    response = db_mocked_app_client.post(
        url="user/login",
        data={
            "username": user_info["username"],
            "password": user_info["password"],
        },
    )

    if response.status_code != 200:
        raise AssertionError(
            f"Expected status code 200, but got {response.status_code}"
        )

    user_info["access_token"] = response.json()["access_token"]
    user_info["refresh_token"] = response.json()["refresh_token"]
    user_info["token_type"] = response.json()["token_type"]

    return user_info
