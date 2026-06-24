from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql://postgres:postgres@localhost:5432/stepwise'
    TEST_DATABASE_URL: str = 'postgresql://postgres:postgres@localhost:5432/stepwise_test'
    REDIS_URL: str = 'redis://localhost:6379'
    SECRET_KEY: str = 'secret-key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CONTAINER_POOL_SIZE: int = 5
    CODE_TIMEOUT_SECONDS: int = 10
    CODE_MEMORY_LIMIT_MB: int = 256
    WORKER_STREAM: str = 'stepwise:worker'
    WORKER_GROUP: str = 'workers'
    WORKER_CONSUMER: str = 'worker-1'

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()