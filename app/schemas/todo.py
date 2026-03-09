from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.enums import TodoPriority
from app.schemas.page import Page


class TodoFilter(BaseModel):
    title: str | None = None
    status: bool | None = None
    priority: TodoPriority | None = None
    is_deleted: bool | None = None

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, use_enum_values=True)

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    priority: TodoPriority = TodoPriority.low


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: bool
    priority: TodoPriority
    deleted_dt: datetime | None = None
    created_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: bool | None = None
    priority: TodoPriority | None = None

    @field_validator("status")
    @classmethod
    def status_must_not_be_none(cls, v: bool | None) -> bool:
        if v is None:
            raise ValueError("status는 null이 될 수 없습니다")
        return v


class TodoListResponse(BaseModel):
    data: list[TodoResponse]
    metadata: Page

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

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
