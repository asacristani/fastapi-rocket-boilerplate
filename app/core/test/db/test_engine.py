from app.core.db.engine import get_engine
from app.settings import settings


def test_get_engine():
    engine = get_engine()
    if settings.database_url != str(engine.url):
        raise AssertionError("Database URL does not match engine URL.")
