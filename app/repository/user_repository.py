from pydantic import EmailStr
from sqlalchemy import insert, select
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserProfile
from app.schemas import UserSchema


@dataclass
class UserRepository:
    session: AsyncSession

    async def get_google_user(self, google_id: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.google_id == google_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, user: UserSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user.model_dump()
        ).returning(UserProfile.id)

        result = await self.session.execute(query)
        user_id = result.scalar_one()
        await self.session.commit()
        return await self.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: EmailStr) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_user(self, user: UserSchema) -> None:
        self.session.add(user)
        await self.session.commit()
