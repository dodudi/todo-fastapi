from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/todo_db"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
