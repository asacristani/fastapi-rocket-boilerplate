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
        self.assertEqual(200, response.status_code)

    def test_check_health_ok(self):
        with patch("app.main.get_engine", MagicMock()), patch(
            "app.main.celery", MagicMock()
        ), patch("app.main.pika", MagicMock()), patch(
            "app.main.redis", MagicMock()
        ):
            response = self.app.get("/check_health")
            self.assertEqual(200, response.status_code)

    def test_check_health_ko(self):
        with patch(
            "app.main.get_engine", MagicMock()
        ) as mock_get_engine, patch(
            "app.main.celery", MagicMock()
        ) as mock_celery, patch(
            "app.main.pika.BlockingConnection", MagicMock()
        ) as mock_pika, patch(
            "app.main.redis.StrictRedis", MagicMock()
        ) as mock_redis:
            mock_get_engine.return_value.connect.side_effect = (
                OperationalError("test", "test", "test")
            )
            mock_celery.control.inspect.return_value.ping.return_value = False
            mock_pika.side_effect = Exception("Mocked exception")
            mock_redis.return_value.ping.side_effect = Exception(
                "Mocked exception"
            )

            response = self.app.get("/check_health")

            self.assertEqual(200, response.status_code)
            self.assertEqual(
                {
                    "celery": "down",
                    "db": "down",
                    "rabbitmq": "down",
                    "redis": "down",
                },
                response.json(),
            )
