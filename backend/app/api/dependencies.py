from collections.abc import AsyncGenerator
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal, get_db_session
from app.domain.unit_of_work import UnitOfWork
from app.repositories.slalchemy_unit_of_work import SqlAlchemyUnitOfWork
from app.services.task_service import TaskService


async def get_unit_of_work(
    session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[UnitOfWork, None]:
    yield SqlAlchemyUnitOfWork(session)


async def get_task_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> TaskService:
    return TaskService(uow)
