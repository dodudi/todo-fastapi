import datetime

from fastapi import HTTPException
from sqlmodel import Session, select, func, col

from app.models.todo import Todo
from app.schemas.page import Page
from app.schemas.todo import TodoCreate, TodoUpdate, TodoFilter


def get_todo(todo_id: int, session: Session) -> Todo:
    todo: Todo | None = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def get_todos(page: int, size: int, todo_filter: TodoFilter, session: Session) -> tuple[list[Todo], Page]:
    filters = []

    if todo_filter.title:
        filters.append(Todo.title.contains(todo_filter.title))

    if todo_filter.status is not None:
        filters.append(Todo.status == todo_filter.status)

    if todo_filter.priority is not None:
        filters.append(Todo.priority == todo_filter.priority)

    if todo_filter.is_deleted is True:
        filters.append(Todo.deleted_dt.is_not(None))
    elif todo_filter.is_deleted is False:
        filters.append(Todo.deleted_dt.is_(None))

    query = select(Todo).where(*filters)
    total = session.exec(select(func.count()).select_from(Todo).where(*filters)).one()
    offset = page * size
    items = session.exec(query.offset(offset).limit(size)).all()

    metadata = Page(
        page=page,
        size=size,
        total_count=total,
        has_next=offset + size < total
    )

    return list(items), metadata


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
    todo = session.get(Todo, todo_id)
    todo.deleted_dt = datetime.datetime.now(datetime.UTC)
    session.commit()
