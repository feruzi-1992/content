from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Smart School Fees Management"
    environment: str = "dev"
    database_url: str = "sqlite+aiosqlite:///./school_fees.db"
    echo_sql: bool = False
    secret_key: str = "dev-secret"  # replace in production


@lru_cache
def get_settings() -> Settings:
    return Settings()  # reads from env if set