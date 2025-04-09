from repository.base import BaseRepository
from database import Tasks
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Tasks)
