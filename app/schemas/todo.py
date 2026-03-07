from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.models.enums import TodoPriority, TodoStatus
from app.schemas.page import Page


class TodoCreate(BaseModel):
    title: str
    description: str
    status: TodoStatus
    priority: TodoPriority


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TodoStatus
    priority: TodoPriority
    created_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TodoStatus | None = None
    priority: TodoPriority | None = None


class TodoListResponse(BaseModel):
    data: list[TodoResponse]
    metadata: Page

# 각 나라 LocalDate + Timezone -> ISO 8601 표준
# 2026-03-10T14:00:00+09:00
# class Todo(BaseModel):
#     title: str
#     description: str
#     status: str
#     priority: str
#     created_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
#     updated_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# @field_validator("create_dt", "update_dt")
# def convert_to_utc(cls, v):
#     if v.tzinfo is None:
#         raise ValueError("timezone 정보가 필요합니다")
#
#     return v.astimezone(timezone.utc)
