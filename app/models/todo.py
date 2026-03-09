from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

from app.models.enums import TodoPriority


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    status: bool = Field(default=False, index=True)
    priority: TodoPriority

    deleted_dt: datetime | None = Field(default=None, index=True)
    created_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
