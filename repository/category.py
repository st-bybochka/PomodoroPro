from sqlalchemy.ext.asyncio import AsyncSession

from repository import BaseRepository
from models import Categories


class CategoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Categories)
