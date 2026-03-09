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
    "title": "test todo",
    "description": "test description",
}


def test_create_todo(client):
    response = client.post("/projects", json=project)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test todo"
    assert data["description"] == "test description"
