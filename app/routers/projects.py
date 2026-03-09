from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services import project as project_service

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("", response_model=ProjectResponse)
def create_project(project: ProjectCreate, session: Session = Depends(get_session)):
    new_project: Project = project_service.create_project(project, session)
    return ProjectResponse(**new_project.model_dump())
