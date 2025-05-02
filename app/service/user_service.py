from dataclasses import dataclass
from fastapi import Response
from pydantic import EmailStr

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

        await self._check_user_already_registered(user.email)
        hashed_password = self._hash_user_password(user.password)
        created_user = await self._create_user_record(user.email, hashed_password)
        tokens = await self._generate_user_tokens(created_user.id, response)
        return self._build_user_response(created_user.id, tokens)

    async def _check_user_already_registered(self, email: EmailStr):
        existing_user = await self.user_repository.get_user_by_email(email)
        if existing_user:
            raise UserAlreadyRegisteredException

    def _hash_user_password(self, password: str) -> str:
        return self.hash_service.get_hash_password(password)

    async def _create_user_record(self, email: EmailStr, hashed_password: str):

        user_data = UserLoginSchema(
            email=email,
            password=hashed_password
        )
        return await self.user_repository.create_user(user_data)

    async def _generate_user_tokens(self, user_id: int, response: Response) -> dict:
        return await self.auth_service.generate_tokens(user_id, response)

    def _build_user_response(self, user_id: int, tokens: dict) -> UserResponseSchema:

        return UserResponseSchema(
            user_id=user_id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )

