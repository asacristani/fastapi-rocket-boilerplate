import asyncio
import unittest
from unittest.mock import MagicMock, patch

import pytest
from fastapi import Request

from app.core.db.session import (
    DBSession,
    DBSessionMeta,
    DBSessionMiddleware,
    MissingSessionError,
    SessionNotInitialisedError,
)


class MockASGIApp:
    async def __call__(self, scope, receive, send):
        pass


async def mock_call_next(request: Request):
    pass


class TestDBSessionMiddleware(unittest.TestCase):
    def setUp(self):
        self.app = MockASGIApp()

    def test_db_session_middleware_constructor(self):
        # Test when both db_url and custom_engine are None
        with self.assertRaises(ValueError):
            DBSessionMiddleware(self.app)

        # Test when custom_engine is provided
        middleware = DBSessionMiddleware(self.app, custom_engine=object())
        self.assertIsInstance(middleware, DBSessionMiddleware)

    def test_db_session_middleware_dispatch(self):
        request = Request(scope={"type": "http"}, receive=None)

        middleware = DBSessionMiddleware(self.app, db_url="sqlite://")

        with patch(
            "app.core.db.session.db"
        ) as mock_db:  # Replace 'your_module' with the actual module name
            mock_db.return_value.__enter__.return_value = (
                None  # Mock the context manager behavior
            )

            # Await the coroutine
            async def run_test():
                response = await middleware.dispatch(request, mock_call_next)
                self.assertIsNone(
                    response
                )  # Adjust this assertion as per your response logic
                # Check if the db context manager was called
                mock_db.assert_called_once()

            asyncio.run(run_test())


class TestDBSession(unittest.TestCase):
    def test_db_session_constructor(self):
        # Enter good
        with DBSession() as db_session:
            self.assertIsInstance(db_session, DBSessionMeta)

        # Exit rollback
        with self.assertRaises(RuntimeError):
            with DBSession() as db_session:
                self.assertIsNotNone(db_session)
                raise RuntimeError("Simulated error")

        # Exit commit
        with DBSession(commit_on_exit=True) as db_session:
            self.assertIsNotNone(db_session)

    @patch("app.core.db.session._Session", None)
    def test_session_not_initialised(self):
        with self.assertRaises(SessionNotInitialisedError):
            with DBSession() as db_session:
                self.assertIsNotNone(db_session)


class TestDBSessionMeta(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _db_mocked(self, db_mocked):
        self.db = db_mocked

    def test_session_ok(self):
        db_test = DBSession
        session = db_test.session
        if session is None:
            raise AssertionError("Session should not be None.")

    def test_session_missing(self):
        with patch(
            "app.core.db.session._session", MagicMock()
        ) as mock_session:
            mock_session.get.return_value = None
            db_test = DBSession
            session = db_test.session
            self.assertRaises(MissingSessionError, session)

    @patch("app.core.db.session._Session", None)
    def test_session_no_initialised(self):
        db_test = DBSession
        with self.assertRaises(SessionNotInitialisedError):
            db_test.session
