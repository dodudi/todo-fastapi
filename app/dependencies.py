# 공통 의존성 (DB 세션, 인증 등)
from fastapi import HTTPException
from fastapi.params import Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.project import Project


def get_project_or_404(project_id: int, session: Session = Depends(get_session)) -> Project:
    project: Project | None = session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
