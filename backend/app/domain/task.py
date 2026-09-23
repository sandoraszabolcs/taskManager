from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskEventType(StrEnum):
    CREATED = "CREATED"
    PROCESSING_STARTED = "PROCESSING_STARTED"
    EXTERNAL_API_CALLED = "EXTERNAL_API_CALLED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


@dataclass
class Task:
    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    retry_count: int
    error_message: str | None
    created_at: datetime
    updated_at: datetime


@dataclass
class TaskEvent:
    id: UUID
    task_id: UUID
    event_type: TaskEventType
    metadata: dict[str, object] | None
    created_at: datetime

