from dataclasses import dataclass
from os import access

from jose import jwt, JWTError
from datetime import datetime, timedelta

from client import GoogleScient
from models import UserProfile
from repository import UserRepository
from schemas import UserLoginSchema, UserCreateSchema
from exceptions import UserNotFoundException, UserNoCorrectPassword, TokenExpired, TokenNotCorrect
from settings import settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: settings
    google_client: GoogleScient

    async def get_google_redirect_url(self) -> str:
        return settings.google_redirect_uri

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code)

        # Проверяем, существует ли пользователь в базе по токену доступа Google
        if user := await self.user_repository.get_google_user(google_id=user_data.google_id):
            access_token = await self.generate_access_token(user.id)
            print("User exists. Logging in...")
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        # Создаем нового пользователя
        create_user_data = UserCreateSchema(
            google_id=user_data.google_id,  # Используем google_id, корректно смапленное Pydantic
            google_access_token=user_data.access_token,
            email=user_data.email
        )

        created_user = await self.user_repository.create_user(create_user_data)
        access_token = await self.generate_access_token(created_user.id)
        print("New user created.")
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)

        self.is_validate_auth_user(user, password)
        access_token = await self.generate_access_token(user.id)

        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def is_validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNoCorrectPassword

    async def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (datetime.utcnow() + timedelta(hours=30)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "exp": expire_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.ALGORITHM
        )
        return token

    async def get_user_id_from_access_token(self, access_token: str) -> int:

        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.ALGORITHM])

        except JWTError:
            raise TokenNotCorrect

        return payload["user_id"]
