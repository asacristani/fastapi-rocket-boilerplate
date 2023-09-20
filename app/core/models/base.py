from datetime import datetime

from sqlmodel import Field, SQLModel

from app.core.db.session import db

from .record import Record


class ModelCore(SQLModel):
    """Base model for the API
    Include:
    - Created and modified dates
    - Bool deleted for soft delete
    - CRUD methods
    """

    id: int | None = Field(default=None, primary_key=True)
    created_datetime: datetime = datetime.now()
    modified_datetime: datetime = datetime.now()
    deleted: bool = False

    def save(
        self,
        source: str = "API",
        action: str = "CREATE",
        owner: str | None = None,
    ):
        """Method to save in the DB for creating or updating"""
        self.modified_datetime = datetime.now()
        model = db.update(self)

        Record(
            model_type=self.__class__.__name__,
            model_id=model.id,
            source=source,
            action=action,
            owner=owner,
        ).save()

        return model

    def delete(
        self, source: str = "API", owner: str | None = None, hard: bool = False
    ) -> bool:
        """Soft delete: mark object as deleted in DB"""
        if hard:
            db.delete(self)
            action = "HARD_DELETE"
        else:
            self.deleted = True
            action = "SOFT_DELETE"
            if not self.save():
                return False

        Record(
            model_type=self.__class__.__name__,
            model_id=self.id,
            source=source,
            action=action,
            owner=owner,
        ).save()

        return True

    @classmethod
    def get_one(cls, value: any, key: any = None) -> any:
        """
        Get one item based in key/value
        - value: the value of the field
        - key: the name of the field (default "id") [optional]
        """
        if not key:
            key = cls.id
        return db.get_one(cls, key=key, value=value)

    @classmethod
    def get_all(cls, offset: int = 0, limit: int = 100, order_by: any = None):
        """
        Return a list of items
        Params:
        - offset: the first element to be retrieved (default 0) [optional]
        - limit: the max amount of elements to be retrieved
         (default 100) [optional]
        - order_by: the field key to order by (default "id") [optional]
        - str_match: the value to be used for searching in
         any field (default "") [optional]
        """
        if not order_by:
            order_by = cls.id
        return db.get_all(
            model=cls, offset=offset, limit=limit, order_by=order_by
        )

    @classmethod
    def count(cls):
        """Count the number of models are in the DB"""
        return db.count(model=cls)
