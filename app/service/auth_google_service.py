from dataclasses import dataclass
from fastapi import Response

from app.client import GoogleScient
from app.repository import UserRepository
from app.service import hash_service, AuthService
from app.service.hash_service import HashService
from app.service.token_service import JwtTokenService

from app.schemas import UserLoginGoogleSchema, UserResponseSchema
from app.config import settings


@dataclass
class AuthGoogleService:
    user_repository: UserRepository
    hash_service: HashService
    google_client: GoogleScient
    token_service: JwtTokenService
    auth_service: AuthService

    async def get_google_redirect_url(self) -> str:
        return settings.google_redirect_uri

    async def google_auth(self, code: str, response: Response):
        user_data = await self.google_client.get_user_info(code)

        if user := await self.user_repository.get_google_user(google_id=user_data.google_id):
            tokens = await self.auth_service.generate_tokens(user.id, response)
            print("User exists. Logging in...")
            return UserResponseSchema(user_id=user.id, access_token=tokens["access_token"], refresh_token=tokens["refresh_token"])

        create_user_data = UserLoginGoogleSchema(
            google_id=user_data.google_id,
            email=user_data.email
        )

        created_user = await self.user_repository.create_user(create_user_data)

        tokens = await self.auth_service.generate_tokens(created_user.id, response)

        print("New user created.")
        return UserResponseSchema(user_id=created_user.id, access_token=tokens["access_token"], refresh_token=tokens["refresh_token"])
