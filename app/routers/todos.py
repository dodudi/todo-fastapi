from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session
from starlette import status

from app.db.session import get_session
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services import todo as todo_service

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


@router.get("/{todo_id}", response_model=TodoResponse)
def read_item(todo_id: int, session: Session = Depends(get_session)):
    return todo_service.get_todo(todo_id, session)


@router.post("", response_model=TodoResponse)
def create_item(todo: TodoCreate, session: Session = Depends(get_session)):
    create_todo = todo_service.create_todo(todo, session)
    return TodoResponse(**create_todo.model_dump())


@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_item(todo_id: int, todo: TodoUpdate, session: Session = Depends(get_session)):
    update_todo = todo_service.update_todo(todo_id, todo, session)
    return TodoResponse(**update_todo.model_dump())


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(todo_id: int, session: Session = Depends(get_session)):
    todo_service.delete_todo(todo_id, session)
    return
