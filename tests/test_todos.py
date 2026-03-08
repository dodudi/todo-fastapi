import pytest
from sqlalchemy import create_engine, StaticPool
from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture
def session():
    engin = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engin)
    with Session(engin) as session:
        yield session


@pytest.fixture
def client(session):
    app.dependency_overrides[Session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_todo(client):
    response = client.post("/todos", json={
        "title": "test todo",
        "priority": "low",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test todo"
    assert data["priority"] == "low"
