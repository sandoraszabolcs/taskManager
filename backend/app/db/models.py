import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.domain.task import TaskEventType, TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"), default=TaskStatus.PENDING
    )
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Optimistic concurrency: SQLAlchemy adds "WHERE version = :old" to UPDATEs
    # and raises StaleDataError if another writer got there first.
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    events: Mapped[list["TaskEvent"]] = relationship(
        back_populates="task", cascade="all, delete-orphan", passive_deletes=True,
        order_by="TaskEvent.created_at",
    )

    __mapper_args__ = {"version_id_col": version}
    __table_args__ = (
        # List/filter by status, newest first
        Index("ix_tasks_status_created_at", "status", "created_at"),
    )


class TaskEvent(Base):
    """Append-only audit history of a task."""

    __tablename__ = "task_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), index=True
    )
    event_type: Mapped[TaskEventType] = mapped_column(Enum(TaskEventType, name="task_event_type"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # "metadata" is reserved on declarative classes, so the attribute is metadata_
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    task: Mapped[Task] = relationship(back_populates="events")
