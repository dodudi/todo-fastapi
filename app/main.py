from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import create_db_and_tables
from app.routers import todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(todos.router)