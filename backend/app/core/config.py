from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "dev"
    log_level: str = "INFO"

    secret_key: str = "change_me"
    access_token_expire_minutes: int = 1440

    admin_email: str = "admin@example.com"
    admin_password: str = "admin12345"

    database_url: str = "postgresql+asyncpg://tsp:tsp@localhost:5432/tsp"

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    bot_token: str = ""
    api_base_url: str = "http://localhost:8000"


settings = Settings()
