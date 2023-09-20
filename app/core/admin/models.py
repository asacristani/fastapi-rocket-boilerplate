from typing import Any

from sqladmin import ModelView
from sqladmin._queries import Query
from starlette.requests import Request

from app.core.models.record import Record

source = "ADMIN"


class ModelViewCore(ModelView):
    """ModelView custom base for sqladmin modelviews
    Main reasons for this:
    - Create records with the changes
    - Modify delete for soft_delete
    """

    # List page
    column_list = "__all__"

    # Pagination options
    page_size = 100
    page_size_options = [25, 50, 100, 200]

    async def insert_model(self, request: Request, data: dict) -> Any:
        model = await Query(self).insert(data)

        Record(
            model_type=self.model.__name__,
            model_id=model.id,
            source=source,
            action="CREATE",
            owner=request.session.get("username"),
        ).save()

        return model

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        model = await Query(self).update(pk, data)

        Record(
            model_type=self.model.__name__,
            model_id=model.id,
            source=source,
            action="UPDATE",
            owner=request.session.get("username"),
        ).save()

        return model

    async def delete_model(self, request: Request, pk: Any) -> None:
        """Overwrite default delete method for
        safe_delete/reverse_delete methods"""
        model: object = await self.get_object_for_edit(pk)
        if model.deleted:
            deleted = False
            action_description = "REVERSE_DELETE"
        else:
            deleted = True
            action_description = "SOFT_DELETE"

        data = {"deleted": deleted}
        await Query(self).update(pk, data)

        Record(
            model_type=self.model.__name__,
            model_id=pk,
            source=source,
            action=action_description,
            owner=request.session.get("username"),
        ).save()
