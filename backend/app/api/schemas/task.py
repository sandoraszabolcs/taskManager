from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.task import TaskStatus


class CreateTaskRequest(BaseModel):
    title: str
    description: str | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    retry_count: int
    error_message: str | None
    created_at: datetime
    updated_at: datetime