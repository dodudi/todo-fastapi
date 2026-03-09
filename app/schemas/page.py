from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class Page(BaseModel):
    page: int
    size: int
    total_count: int
    has_next: bool

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)