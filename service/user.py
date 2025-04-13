from dataclasses import dataclass

from schemas import UserLoginSchema
from repository import UserRepository
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str):

        user = await self.user_repository.create_user(username, password)
        access_token = await self.auth_service.generate_access_token(user.id)

        return UserLoginSchema(user_id=user.id, access_token=access_token)
