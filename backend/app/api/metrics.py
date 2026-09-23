from fastapi import APIRouter, Depends

from app.api.deps import get_task_service
from app.schemas.task import Metrics
from app.services.task_service import TaskService

router = APIRouter()


@router.get("", response_model=Metrics)
async def get_metrics(service: TaskService = Depends(get_task_service)):
    return await service.get_metrics()
