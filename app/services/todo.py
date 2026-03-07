from fastapi import HTTPException
from sqlmodel import Session

from app.models.todo import Todo
from app.schemas.todo import TodoCreate


def get_todo(todo_id: int, session: Session) -> Todo:
    todo: Todo | None = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def create_todo(data: TodoCreate, session: Session) -> Todo:
    todo = Todo(**data.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def delete_todo(todo_id: int, session: Session) -> None:
    session.delete(get_todo(todo_id, session))
    session.commit()
