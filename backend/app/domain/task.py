"""Task status state machine. Pure Python, no ORM/framework imports."""
import enum


class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskEventType(str, enum.Enum):
    CREATED = "CREATED"
    PROCESSING_STARTED = "PROCESSING_STARTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRIED = "RETRIED"


ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.PENDING: {TaskStatus.PROCESSING},
    TaskStatus.PROCESSING: {TaskStatus.COMPLETED, TaskStatus.FAILED},
    TaskStatus.FAILED: {TaskStatus.PENDING},  # retry
    TaskStatus.COMPLETED: set(),
}


class InvalidTransition(Exception):
    pass


def can_transition(current: TaskStatus, target: TaskStatus) -> bool:
    return target in ALLOWED_TRANSITIONS[current]


def ensure_transition(current: TaskStatus, target: TaskStatus) -> None:
    if not can_transition(current, target):
        raise InvalidTransition(f"{current} -> {target}")


def can_retry(status: TaskStatus) -> bool:
    return status == TaskStatus.FAILED
