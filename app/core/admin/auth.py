from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend

from app.core.auth.functions import create_access_token, get_current_admin
from app.settings import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        if (
            not username == settings.admin_user
            or not password == settings.admin_pass
        ):
            return False

        # And update session
        token = create_access_token(username=username)
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | None:
        token = request.session.get("token")

        # Validate token
        if not token or not (username := get_current_admin(token=token)):
            return RedirectResponse(
                request.url_for("admin:login"), status_code=302
            )

        request.session.update({"username": username})

        return None
