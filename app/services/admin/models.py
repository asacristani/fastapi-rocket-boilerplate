from app.core.models.record import Record
from app.services.user.models import User, RevokedToken

from app.core.admin.models import ModelViewCore


class UserAdmin(ModelViewCore, model=User):
    # Menu
    icon = "fa-solid fa-user"

    # List page
    column_list = [User.id, User.username, User.deleted]
    column_searchable_list = [User.username]

    # Detail Page
    pass

    # General options
    column_labels = {User.username: "email"}  # This modifies the name of the columns for list and detail pages


class RevokedTokenAdmin(ModelViewCore, model=RevokedToken):
    icon = "fa-solid fa-ban"
    column_list = [RevokedToken.created_datetime, RevokedToken.username, RevokedToken.token]


class RecordAdmin(ModelViewCore, model=Record):
    icon = "fa-solid fa-clock-rotate-left"

    # Permissions
    can_create = False
    can_edit = False
    can_delete = False

    # List page
    column_searchable_list = [Record.model_type, Record.model_id]
