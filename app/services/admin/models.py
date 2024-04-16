from typing import Any

from sqladmin._queries import Query
from starlette.requests import Request

from app.core.admin.models import ModelViewCore
from app.core.auth.functions import hash_password
from app.core.models.record import Record
from app.services.user.models import RevokedToken, User


class UserAdmin(ModelViewCore, model=User):
    # Menu
    icon = "fa-solid fa-user"

    # List page
    column_list = [User.id, User.username, User.deleted]
    column_searchable_list = [User.username]

    # Detail Page
    pass

    # Form page
    async def insert_model(self, request: Request, data: dict) -> Any:
        """Overwrite insert method for hashing the password"""
        if "hashed_password" in data:
            data["hashed_password"] = hash_password(data["hashed_password"])

        model = await Query(self).insert(data)

        Record(
            model_type=self.model.__name__,
            model_id=model.id,
            source="ADMIN",
            action="CREATE",
            owner=request.session.get("username"),
        ).save()

        return model

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        """Overwrite update method for hashing the password"""
        if "hashed_password" in data:
            data["hashed_password"] = hash_password(data["hashed_password"])

        model = await Query(self).update(pk, data)

        Record(
            model_type=self.model.__name__,
            model_id=model.id,
            source="ADMIN",
            action="UPDATE",
            owner=request.session.get("username"),
        ).save()

        return model

    # General options
    column_labels = {
        User.username: "email"
    }  # This modifies the name of the columns for list and detail pages


class RevokedTokenAdmin(ModelViewCore, model=RevokedToken):
    icon = "fa-solid fa-ban"
    column_list = [
        RevokedToken.created_datetime,
        RevokedToken.username,
        RevokedToken.token,
    ]


class RecordAdmin(ModelViewCore, model=Record):
    icon = "fa-solid fa-clock-rotate-left"

    # Permissions
    can_create = False
    can_edit = False
    can_delete = False

    # List page
    column_searchable_list = [Record.model_type, Record.model_id]
