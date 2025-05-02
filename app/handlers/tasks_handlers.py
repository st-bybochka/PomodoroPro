from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from app.exceptions import TaskNotFound
from app.schemas import TaskSchema, TaskCreateSchema
from app.dependencies import get_task_service, get_request_user_id
from app.service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/")
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
):
    return await task_service.get_tasks()



@router.post("/",
             response_model=TaskSchema
)
async def create_task(
        body: TaskCreateSchema,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    task = await task_service.create_task(body, user_id)
    return task


@router.patch("/{task_id}",
              response_model=TaskSchema)
async def update_task(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        return await task_service.update_task_name(task_id, name, user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )




@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        await task_service.delete_task(task_id, user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail)
