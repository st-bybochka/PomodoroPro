from dataclasses import dataclass
from fastapi import Response

from app.client import GoogleScient
from app.repository import UserRepository
from app.service import hash_service, AuthService
from app.service.token_service import JwtTokenService
from app.schemas import UserLoginGoogleSchema, UserResponseSchema, UserSchema
from app.config import settings


@dataclass
class AuthGoogleService:
    user_repository: UserRepository
    hash_service: hash_service.HashService
    google_client: GoogleScient
    token_service: JwtTokenService
    auth_service: AuthService

    async def get_google_redirect_url(self) -> str:
        return settings.google_redirect_uri

    async def google_auth(self, code: str, response: Response) -> UserResponseSchema:

        user_data = await self._fetch_google_user_info(code)
        user = await self._get_or_create_user_from_google(user_data)
        tokens = await self._generate_auth_tokens(user.id, response)
        return self._build_user_response(user.id, tokens)

    async def _fetch_google_user_info(self, code: str):
        return await self.google_client.get_user_info(code)

    async def _get_or_create_user_from_google(self, user_data: UserLoginGoogleSchema):

        user = await self.user_repository.get_google_user(google_id=user_data.google_id)
        if user:
            self._log_message("User exists. Logging in...")
            return user

        self._log_message("New user created.")
        return await self.user_repository.create_user(UserSchema(
            google_id=user_data.google_id,
            email=user_data.email)
        )

    async def _generate_auth_tokens(self, user_id: int, response: Response):

        return await self.auth_service.generate_tokens(user_id, response)

    def _build_user_response(self, user_id: int, tokens: dict) -> UserResponseSchema:

        return UserResponseSchema(
            user_id=user_id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )

    def _log_message(self, message: str):
        print(message)
