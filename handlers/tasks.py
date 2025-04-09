from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated

from schemas import TaskSchema, TaskReadSchema, TaskUpdateSchema
from repository import TaskRepository
from dependencies import get_task_repository, get_task_service
from service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/", response_model=List[TaskReadSchema])
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
):
    return await task_service.get_tasks()



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
        task: TaskSchema,
        repo: TaskRepository = Depends(get_task_repository)
):
    await repo.add(**task.dict())


@router.patch("/{task_id}")
async def update_task(
        task_id: int,
        update_data: TaskUpdateSchema,
        repo: TaskRepository = Depends(get_task_repository)
):

    if not update_data.dict(exclude_unset=True):
        raise HTTPException(
            status_code=400,
            detail="No data to update")

    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task withid {task_id} not found")

    await repo.update(task_id, **update_data.dict(exclude_unset=True))
    return {"messsage": f"Task updated successfully, task_id {task_id}"}


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        repo: TaskRepository = Depends(get_task_repository)
):
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found")

    await repo.delete(task_id)
