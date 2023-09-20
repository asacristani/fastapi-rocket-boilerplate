from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import OperationalError


class TestMain(TestCase):
    @pytest.fixture(autouse=True)
    def _db_mocked_app_client(self, db_mocked_app_client):
        self.app = db_mocked_app_client

    def test_endpoint_main(self):
        response = self.app.get("/")
        assert 200 == response.status_code

    def test_check_health_ok(self):
        with patch("app.main.get_engine", MagicMock()) as mock_connect:
            mock_connect.connect().return_value = object()

            response = self.app.get("/check_health")

            assert 1 == mock_connect.connect.call_count
            assert 200 == response.status_code

    def test_check_health_ko(self):
        with patch("app.main.get_engine", MagicMock()) as mock_get_engine:
            mock_get_engine.return_value.connect.side_effect = (
                OperationalError("test", "test", "test")
            )

            response = self.app.get("/check_health")

            assert 503 == response.status_code
