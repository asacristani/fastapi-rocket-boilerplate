from datetime import datetime

from sqlmodel import Field, SQLModel

from app.core.db.session import db


class Record(SQLModel, table=True):
    """Model for storing change records in the rest of models"""

    # TODO: Use enums instead of str for source and action?
    id: int | None = Field(default=None, primary_key=True)
    created_datetime: datetime = datetime.now()
    model_type: str
    model_id: int
    source: str  # Source of the change [API | ADMIN]
    action: str  # Action that caused the record
    # [CREATE | UPDATE | SOFT_DELETE | HARD_DELETE]
    owner: str | None  # Username of the owner who caused the action if applies

    def save(self):
        """Method to save in the DB for creating"""
        return db.update(self)
