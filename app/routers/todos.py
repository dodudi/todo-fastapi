from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.todo import TodoCreate, TodoResponse
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
