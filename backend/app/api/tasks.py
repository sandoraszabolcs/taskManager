import uuid

from fastapi import APIRouter, Depends, Response

from app.api.deps import get_task_service
from app.domain.task import TaskStatus
from app.schemas.task import TaskCreate, TaskDetail, TaskList, TaskRead
from app.services.task_service import TaskService

router = APIRouter()


@router.post("", response_model=TaskRead, status_code=201)
async def create_task(data: TaskCreate, service: TaskService = Depends(get_task_service)):
    return await service.create_task(data)


@router.get("", response_model=TaskList)
async def list_tasks(
    status: TaskStatus | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
    service: TaskService = Depends(get_task_service),
):
    return await service.list_tasks(status=status, search=search, limit=limit, offset=offset)


@router.get("/{task_id}", response_model=TaskDetail)
async def get_task(task_id: uuid.UUID, service: TaskService = Depends(get_task_service)):
    return await service.get_task(task_id)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: uuid.UUID, service: TaskService = Depends(get_task_service)):
    await service.delete_task(task_id)
    return Response(status_code=204)


@router.post("/{task_id}/process", response_model=TaskRead, status_code=202)
async def process_task(task_id: uuid.UUID, service: TaskService = Depends(get_task_service)):
    return await service.trigger_processing(task_id)


@router.post("/{task_id}/retry", response_model=TaskRead, status_code=202)
async def retry_task(task_id: uuid.UUID, service: TaskService = Depends(get_task_service)):
    return await service.retry_task(task_id)
