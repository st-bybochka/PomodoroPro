from fastapi import APIRouter, Depends, Response
from typing import Annotated

from app.schemas import UserLoginSchema
from app.service import UserService
from app.dependencies import get_user_service

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/create")
async def create_user(
        response: Response,
        user_data: UserLoginSchema,
        user_service: Annotated[UserService, Depends(get_user_service)]
                      ):
    return await user_service.create_user(user_data, response)
