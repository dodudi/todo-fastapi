import pytest
from sqlalchemy import create_engine, StaticPool
from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient

from app.db.session import get_session
from app.main import app


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


project = {
    "title": "test project",
    "description": "test project description",
}

todo = {
    "title": "test todo",
    "description": "test description",
    "priority": "low"
}


def test_create_todo(client):
    response = client.post("/projects", json=project)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "test project"
    assert data["description"] == "test project description"


def test_create_todo_with_project(client):
    project_response = client.post("/projects", json=project)
    project_id = project_response.json()["id"]

    todo_response = client.post(f"/projects/{project_id}/todos", json=todo)
    assert todo_response.status_code == 200

    json = todo_response.json()
    assert json["title"] == todo.get("title")
    assert json["description"] == todo.get("description")
    assert json["priority"] == "low"
    assert json["projectId"] == project_id


def test_create_todo_with_project_404(client):
    project_response = client.post("/projects", json=project)
    project_id_add_one = project_response.json()["id"] + 1

    todo_response = client.post(f"/projects/{project_id_add_one}/todos", json=todo)
    assert todo_response.status_code == 404