from dataclasses import dataclass
from fastapi import Response

from app.exceptions import UserAlreadyRegisteredException
from app.schemas import UserLoginSchema
from app.repository import UserRepository
from app.schemas import UserResponseSchema
from app.service.hash_service import HashService
from app.service.token_service import JwtTokenService
from app.service.auth_login_service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService
    token_service: JwtTokenService
    hash_service: HashService

    async def create_user(self, user: UserLoginSchema, response: Response) -> UserResponseSchema:
        existing_user = await self.user_repository.get_user_by_email(user.email)
        if existing_user:
            raise UserAlreadyRegisteredException

        hashed_password = self.hash_service.get_hash_password(user.password)

        hash_user = UserLoginSchema(
            email=user.email,
            password=hashed_password
        )

        created_user = await self.user_repository.create_user(hash_user)

        tokens = await self.auth_service.generate_tokens(created_user.id, response)

        return UserResponseSchema(
            user_id=created_user.id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"])
