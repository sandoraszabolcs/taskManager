from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.sqlalchemy_task_event_repository import (
    SqlAlchemyTaskEventRepository,
)
from app.repositories.sqlalchemy_task_repository import (
    SqlAlchemyTaskRepository,
)


class SqlAlchemyUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.tasks = SqlAlchemyTaskRepository(session)
        self.events = SqlAlchemyTaskEventRepository(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
