from app.services.user.models import User


def test_authenticate_user_no_exists(db_mocked_app_client):
    user = User.authenticate_user(username="test", password="test")

    assert user is None
