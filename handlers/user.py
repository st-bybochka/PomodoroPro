from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from schemas import UserLoginSchema, UserCreateSchema
from service import UserService
from dependencies import get_user_service

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/", response_model=UserLoginSchema)
async def create_user(user_data: UserCreateSchema,
                      user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.create_user(user_data.username, user_data.password)
