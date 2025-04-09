from sqlalchemy import insert, select
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserProfile


@dataclass
class UserRepository:
    session: AsyncSession

    async def create_user(self, username: str, password: str, access_token: str) -> UserProfile:
        query = insert(UserProfile).values(
            username=username,
            password=password,
            access_token=access_token
        ).returning(UserProfile.id)

        result = await self.session.execute(query)
        user_id = result.scalar_one()
        await self.session.commit()
        return await self.get_user(user_id)


    async def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
