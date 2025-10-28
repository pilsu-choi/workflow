from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/workflow_scratch_2"
    )
    DEBUG: bool = False
    API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_config():
    return Settings()
