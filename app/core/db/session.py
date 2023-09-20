from contextvars import ContextVar
from typing import Dict, Optional, Union

from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker as sessionmaker_
from sqlmodel import Session, create_engine, select
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.types import ASGIApp


class sessionmaker(sessionmaker_):
    def __init__(self, *args, **kwargs):
        if "class_" not in kwargs:
            kwargs["class_"] = Session
        super().__init__(*args, **kwargs)


_Session: sessionmaker | None = None
_session: ContextVar[Optional[Session]] = ContextVar("_session", default=None)


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        db_url: Optional[Union[str, URL]] = None,
        custom_engine: Optional[Engine] = None,
        engine_args: Dict = None,
        session_args: Dict = None,
        commit_on_exit: bool = False,
    ):
        super().__init__(app)
        engine_args = engine_args or {}
        self.commit_on_exit = commit_on_exit
        session_args = session_args or {}
        if not custom_engine and not db_url:
            raise ValueError(
                "You need to pass a db_url or a custom_engine parameter."
            )
        if not custom_engine:
            engine = create_engine(db_url, **engine_args)
        else:
            engine = custom_engine

        global _Session
        _Session = sessionmaker(bind=engine, **session_args)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        with db(commit_on_exit=self.commit_on_exit):
            response = await call_next(request)
        return response


class MissingSessionError(Exception):
    """
    Exception raised for when the user tries to
    access a database session before
    it is created.
    """

    def __init__(self):
        msg = """
        No session found! Either you are not currently in a request context,
        or you need to manually create a session context by using a `db`
        instance as a context manager e.g.:

        with db():
            db.session.query(User).all()
        """
        super().__init__(msg)


class SessionNotInitialisedError(Exception):
    """
    Exception raised when the user creates a new DB session without first
    initialising it.
    """

    def __init__(self):
        msg = """
        Session not initialised! Ensure that DBSessionMiddleware has been
        initialised before attempting database access.
        """
        super().__init__(msg)


class DBSessionMeta(type):
    # using this metaclass means that we can access db.session as a property
    # at a class level,
    # rather than db().session

    @property
    def session(self) -> Session:
        if _Session is None:
            raise SessionNotInitialisedError
        session = _session.get()
        if session is None:
            raise MissingSessionError
        return session

    def get_one(self, model: any, key: any, value: any) -> object:
        try:
            statement = select(model).where(
                key == value, model.deleted == False
            )
            result = self.session.exec(statement).one()
            return result
        except NoResultFound:
            return None

    def get_all(self, model: any, offset: int, limit: int, order_by: any):
        """Get all items excluding delete ones"""
        statement = (
            select(model)
            .where(model.deleted == False)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )
        result = self.session.exec(statement).all()
        return result

    def update(self, item: any) -> object:
        """Create or modify"""
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item: any) -> bool:
        """TODO: Add return False when exceptions are observed"""
        self.session.delete(item)
        self.session.commit()
        return True

    def count(self, model: any) -> int:
        result = len(
            self.session.exec(
                select(model).where(model.deleted == False)
            ).all()
        )
        return result


class DBSession(metaclass=DBSessionMeta):
    def __init__(
        self, session_args: Dict = None, commit_on_exit: bool = False
    ):
        self.token = None
        self.session_args = session_args or {}
        self.commit_on_exit = commit_on_exit

    def __enter__(self):
        if not isinstance(_Session, sessionmaker):
            raise SessionNotInitialisedError
        self.token = _session.set(_Session(**self.session_args))
        return type(self)

    def __exit__(self, exc_type, *_):
        sess = _session.get()
        if exc_type is not None:
            sess.rollback()
        if self.commit_on_exit:
            sess.commit()
        sess.close()
        _session.reset(self.token)


db: DBSessionMeta = DBSession
