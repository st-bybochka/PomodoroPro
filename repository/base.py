from typing import Any
from sqlalchemy import select, insert, delete as sa_delete, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def get_all(self, **filters):
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, model_id: int):
        stmt = select(self.model).where(self.model.id == model_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, **data: Any):
        stmt = insert(self.model).values(**data)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, model_id: int, **update_data: Any):
        stmt = sa_update(self.model).where(self.model.id == model_id).values(**update_data)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, model_id: int):
        stmt = sa_delete(self.model).where(self.model.id == model_id)
        await self.session.execute(stmt)
        await self.session.commit()
