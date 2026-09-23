from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://tasks:tasks@localhost:5434/tasks"
    redis_url: str = "redis://localhost:6380/0"
    task_queue_name: str = "tasks:queue"
    external_api_failure_rate: float = 0.2


settings = Settings()
