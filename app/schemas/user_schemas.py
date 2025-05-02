from typing import Annotated

from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import datetime

from app.validators import PasswordValidator


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    password: Annotated[str, Field(None)]
    login_attempts: Annotated[int, Field(default=0)]
    block_until: Annotated[datetime, Field(None)]
    google_id: Annotated[str, Field(None)]


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        return PasswordValidator.validate_password(value)

    class Config:
        from_attributes = True


class UserLoginGoogleSchema(BaseModel):
    google_id: str
    email: EmailStr


    class Config:
        from_attributes = True


class UserResponseSchema(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True
