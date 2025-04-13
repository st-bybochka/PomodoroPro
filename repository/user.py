from sqlalchemy import insert, select
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserProfile
from schemas import UserCreateSchema


@dataclass
class UserRepository:
    session: AsyncSession

    async def get_google_user(self, google_id: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.google_id == google_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user.model_dump()
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
