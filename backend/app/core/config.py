import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    app_env: str
    database_url: str


@lru_cache
def get_settings() -> Settings:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        database_url=database_url,
    )
