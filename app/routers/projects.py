from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies import get_project_or_404
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectListResponse
from app.schemas.todo import TodoResponse, TodoCreate
from app.services import project as project_service
from app.services import todo as todo_service

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("", response_model=ProjectResponse)
def create_project(project: ProjectCreate, session: Session = Depends(get_session)):
    new_project: Project = project_service.create_project(project, session)
    return ProjectResponse(**new_project.model_dump())


@router.post("/{project_id}/todos", response_model=TodoResponse)
def create_project_todo(todo: TodoCreate, project: Project = Depends(get_project_or_404), session: Session = Depends(get_session)):
    new_todo = todo_service.create_project_todo(project.id, todo, session)
    return TodoResponse(**new_todo.model_dump())

@router.get("")
def get_projects(session: Session = Depends(get_session)):
    projects = project_service.get_projects(session)
    return ProjectListResponse(
        data=[ProjectResponse.model_validate(project, from_attributes=True) for project in projects]
    )
