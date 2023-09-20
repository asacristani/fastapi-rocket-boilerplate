from app.core.db.engine import get_engine
from app.settings import settings


def test_get_engine():
    engine = get_engine()
    assert settings.database_url == str(engine.url)
