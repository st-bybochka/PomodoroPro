from dataclasses import dataclass
from fastapi import Response, Request
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.repository import UserRepository
from app.config import settings
from app.exceptions import (UserNotFoundException, UserIncorrectLoginOrPasswordException,
                            TokenMissingException, TokenNotCorrectException, UserBlockedException)
from app.schemas import UserLoginSchema, UserResponseSchema
from app.models import UserProfile
from app.schemas import UserSchema

from app.service.hash_service import HashService
from app.service.token_service import JwtTokenService


@dataclass
class AuthService:
    user_repository: UserRepository
    token_service: JwtTokenService
    hash_service: HashService
    settings: settings

    async def login(self, data: UserLoginSchema, response: Response) -> UserResponseSchema:
        user = await self._authenticate_user(data)
        await self._check_block_status(user)
        tokens = await self.generate_tokens(user.id, response)
        return UserResponseSchema(user_id=user.id, access_token=tokens["access_token"], refresh_token=tokens["refresh_token"])

    async def generate_tokens(self, user_id: int, response: Response) -> dict:
        access_token = await self.token_service.create_access_token(user_id)
        refresh_token = await self.token_service.create_refresh_token(user_id)

        response.set_cookie(key="access_token", value=str(access_token), httponly=True, secure=True)
        response.set_cookie(key="refresh_token", value=str(refresh_token), httponly=True, secure=True)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def _authenticate_user(self, data: UserLoginSchema) -> UserProfile:
        user = await self.user_repository.get_user_by_email(data.email)
        if not user:
            raise UserNotFoundException(f"User with email {data.email} not found.")
        if not self.hash_service.verify_hash_password(data.password, user.password):
            await self._register_failed_attempt(user)
            raise UserIncorrectLoginOrPasswordException
        return user

    async def _register_failed_attempt(self, user: UserSchema) -> None:

        user.login_attempts += 1
        if user.login_attempts >= 5:
            user.block_until = datetime.utcnow() + timedelta(minutes=5)
            user.login_attempts = 0
        await self.user_repository.update_user(user)

    async def _check_block_status(self, user: UserSchema) -> None:
        if user.block_until and user.block_until > datetime.utcnow():
            raise UserBlockedException("User is blocked. Try again later.")

    async def refresh_access_token(self, request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise TokenMissingException

        user_id = await self.token_service.decode_token(refresh_token)

        access_token = await self.token_service.create_access_token(user_id)
        response.set_cookie(key="access_token", value=access_token, httponly=True)

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def logout(self, response: Response):

        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")

    async def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (datetime.utcnow() + timedelta(hours=30)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "exp": expire_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.ALGORITHM
        )
        return token

    async def get_user_id_from_access_token(self, access_token: str) -> int:

        if not access_token:
            raise TokenMissingException

        try:
            payload = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.ALGORITHM]
            )

        except JWTError:
            raise TokenNotCorrectException

        return payload["user_id"]
