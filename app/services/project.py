from sqlmodel import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate


def create_project(data: ProjectCreate, session: Session) -> Project:
    project = Project(**data.model_dump())
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def get_projects(session) -> list[Project]:
    projects = session.query(Project).all()
    return projects
