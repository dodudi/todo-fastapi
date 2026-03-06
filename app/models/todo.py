from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    status: str
    priority: str
    created_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


