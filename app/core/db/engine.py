from sqlmodel import create_engine

from app.settings import settings

database_url = settings.database_url


def get_engine():
    return create_engine(database_url)
