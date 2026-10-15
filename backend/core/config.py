from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "DataQGuard"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/dataqguard"
    
    # Redis (for Celery)
    REDIS_URL: str = "redis://redis:6379/0"
    
    # ClickHouse (for metrics)
    CLICKHOUSE_HOST: str = "clickhouse"
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_DATABASE: str = "dataqguard"
    
    # Default admin
    DEFAULT_ADMIN_EMAIL: str = "admin@dataqguard.com"
    DEFAULT_ADMIN_PASSWORD: str = "admin123"
    
    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
