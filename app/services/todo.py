from sqlmodel import Session

from app.models.todo import Todo
from app.schemas.todo import TodoCreate


def create_todo(data: TodoCreate, session: Session) -> Todo:
    todo = Todo(**data.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
