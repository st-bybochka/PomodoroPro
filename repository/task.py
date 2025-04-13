from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Tasks
from schemas import TaskCreateSchema


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(self) -> list[Tasks]:
        async with self.session as session:
            result = await session.execute(select(Tasks))
            task: list[Tasks] = result.scalars().all()
        return task

    async def get_task_by_id(self, task_id: int) -> Tasks | None:
        async with self.session as session:
            result = await session.execute(select(Tasks).where(Tasks.id == task_id))
            task: Tasks = result.scalar_one_or_none()
        return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        async with self.session as session:
            task_model = Tasks(
                name=task.name,
                pomodoro_count=task.pomodoro_count,
                category_id=task.category_id,
                user_id=user_id
            )

            session.add(task_model)
            await session.commit()

            return task_model.id

    async def get_user_task(self, user_id: int, task_id: int) -> Tasks | None:
        async with self.session as session:
            result = await session.execute(select(Tasks).where(Tasks.user_id == user_id, Tasks.id == task_id))
            task: Tasks = result.scalar_one_or_none()
            return task

    async def delete_task(self, task_id: int, user_id: int) -> None:
        async with self.session as session:
            await session.execute(delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id))
            await session.commit()

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> Tasks | None:
        async with self.session as session:
            stmt = (
                update(Tasks)
                .where(Tasks.id == task_id, Tasks.user_id == user_id)  # Проверка и пользователя
                .values(name=name)
                .returning(Tasks)
            )

            result = await session.execute(stmt)
            task = result.scalar_one_or_none()
            await session.commit()
            return task
