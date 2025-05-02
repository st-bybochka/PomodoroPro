from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Literal

from app.config import settings


class JwtTokenService:

    async def create_token(self, user_id: int, token_type: Literal["access", "refresh"]) -> str:
        if token_type == "access":
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        elif token_type == "refresh":
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode = {"user_id": user_id, "exp": expire}
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    async def create_access_token(self, user_id: int) -> str:
        return await self.create_token(user_id, "access")

    async def create_refresh_token(self, user_id: int) -> str:
        return await self.create_token(user_id, "refresh")

    async def decode_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = payload["user_id"]

            if user_id is None:
                raise JWTError
            return user_id
        except JWTError:
            raise ValueError("Invalid token")
