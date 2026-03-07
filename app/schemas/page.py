from pydantic import BaseModel


class Page(BaseModel):
    page: int
    size: int
    total_count: int
    has_next: bool
