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


todo = {
    "title": "test todo",
    "description": "test description",
    "priority": "low",
}

update_todo = {
    "title": "updated title",
    "status": True,
}


def test_create_todo(client):
    response = client.post("/todos", json=todo)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test todo"
    assert data["priority"] == "low"


def test_read_todo(client):
    create = client.post("/todos", json=todo)
    todo_id = create.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "test todo"
    assert data["description"] == "test description"
    assert data["priority"] == "low"


def test_update_todo(client):
    create = client.post("/todos", json=todo)
    todo_id = create.json()["id"]

    response = client.patch(f"/todos/{todo_id}", json=update_todo)
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "updated title"
    assert data["status"] is True
