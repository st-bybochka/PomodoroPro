import string
from dataclasses import dataclass
from random import choice

from schemas import UserLoginSchema
from repository import UserRepository


@dataclass
class UserService:
    user_repository: UserRepository


    async def create_user(self, username: str, password: str):
        access_token = self.generate_access_token()
        user = await self.user_repository.create_user(username, password, access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def generate_access_token() -> str:
        return "".join(choice(string.ascii_uppercase + string.digits) for _ in range(10))