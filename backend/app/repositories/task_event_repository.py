from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import TaskEventModel
from app.domain.task import TaskEvent, TaskEventType


class SqlAlchemyTaskEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        task_id: UUID,
        event_type: TaskEventType,
        metadata: dict[str, object] | None = None,
    ) -> TaskEvent:
        model = TaskEventModel(
            id=uuid4(),
            task_id=task_id,
            event_type=event_type,
            metadata=metadata,
        )

        self._session.add(model)
        await self._session.flush()

        return self._to_domain(model)

    async def list_for_task(
        self,
        task_id: UUID,
    ) -> list[TaskEvent]:
        result = await self._session.execute(
            select(TaskEventModel)
            .where(TaskEventModel.task_id == task_id)
            .order_by(TaskEventModel.created_at.asc())
        )

        return [
            self._to_domain(model)
            for model in result.scalars().all()
        ]

    @staticmethod
    def _to_domain(
        model: TaskEventModel,
    ) -> TaskEvent:
        return TaskEvent(
            id=model.id,
            task_id=model.task_id,
            event_type=model.event_type,
            metadata=model.metadata,
            created_at=model.created_at,
        )

