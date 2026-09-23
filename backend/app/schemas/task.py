import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.task import TaskEventType, TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None
    status: TaskStatus
    retry_count: int
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class TaskEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    event_type: TaskEventType
    created_at: datetime
    metadata: dict | None = Field(default=None, validation_alias="metadata_")


class TaskDetail(TaskRead):
    events: list[TaskEventRead]


class TaskList(BaseModel):
    items: list[TaskRead]
    total: int


class Metrics(BaseModel):
    total: int
    by_status: dict[TaskStatus, int]
    queue_length: int
