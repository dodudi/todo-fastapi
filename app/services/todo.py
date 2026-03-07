from fastapi import HTTPException
from sqlmodel import Session, select, func

from app.models.todo import Todo
from app.schemas.page import Page
from app.schemas.todo import TodoCreate, TodoUpdate


def get_todo(todo_id: int, session: Session) -> Todo:
    todo: Todo | None = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def get_todos(page: int, size: int, session: Session) -> tuple[list[Todo], Page]:
    total = session.exec(select(func.count()).select_from(Todo)).one()
    items = list(session.exec(select(Todo).offset(page * size).limit(size)).all())
    metadata = Page(page=page, size=size, total_count=total, has_next=(page + 1) * size < total)
    return items, metadata


def create_todo(data: TodoCreate, session: Session) -> Todo:
    todo = Todo(**data.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def update_todo(todo_id: int, data: TodoUpdate, session: Session) -> Todo:
    todo: Todo | None = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    session.commit()
    session.refresh(todo)
    return todo


def delete_todo(todo_id: int, session: Session) -> None:
    session.delete(get_todo(todo_id, session))
    session.commit()
