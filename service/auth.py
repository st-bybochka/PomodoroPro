from dataclasses import dataclass

from models import UserProfile
from repository import UserRepository
from schemas import UserLoginSchema
from exceptions import UserNotFoundException, UserNoCorrectPassword

@dataclass
class AuthService:
    user_repository: UserRepository

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)

        self.is_validate_auth_user(user, password)

        return UserLoginSchema(user_id=user.id, access_token=user.access_token)


    @staticmethod
    def is_validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNoCorrectPassword


