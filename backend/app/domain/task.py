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

    def start_processing(self) -> None:
        if self.status != TaskStatus.PENDING:
            raise ValueError(
                "Only pending tasks can start processing"
            )

        self.status = TaskStatus.PROCESSING
        self.error_message = None

    def complete(self) -> None:
        if self.status != TaskStatus.PROCESSING:
            raise ValueError(
                "Only processing tasks can be completed"
            )

        self.status = TaskStatus.COMPLETED
        self.error_message = None

    def fail(self, error_message: str) -> None:
        if self.status != TaskStatus.PROCESSING:
            raise ValueError(
                "Only processing tasks can fail"
            )

        self.status = TaskStatus.FAILED
        self.error_message = error_message

    def retry(self) -> None:
        if self.status != TaskStatus.FAILED:
            raise ValueError(
                "Only failed tasks can be retried"
            )

        self.retry_count += 1
        self.status = TaskStatus.PENDING
        self.error_message = None
