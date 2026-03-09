from datetime import datetime, timezone

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_dt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ProjectListResponse(BaseModel):
    data: list[ProjectResponse]