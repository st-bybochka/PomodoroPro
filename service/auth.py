from dataclasses import dataclass

from jose import jwt, JWTError
from datetime import datetime, timedelta


from models import UserProfile
from repository import UserRepository
from schemas import UserLoginSchema
from exceptions import UserNotFoundException, UserNoCorrectPassword, TokenExpired, TokenNotCorrect
from settings import settings



@dataclass
class AuthService:
    user_repository: UserRepository
    settings: settings
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
        if payload["exp"] < datetime.utcnow().timestamp():
            raise TokenExpired
        return payload["user_id"]