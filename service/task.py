from dataclasses import dataclass

from repository import TaskRepository, TaskCache
from schemas import TaskSchema

@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_tasks(self) -> list[TaskSchema]:
        if tasks := self.task_cache.get_tasks():
            return tasks

        else:

            tasks = await self.task_repository.get_all()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks)
            return tasks_schema
