from fastapi import APIRouter, Depends, HTTPException

from exceptions import UserNoCorrectPassword, UserNotFoundException
from schemas import UserLoginSchema, UserCreateSchema
from service import AuthService
from dependencies import get_auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=UserLoginSchema)
async def login(data: UserCreateSchema,
                auth_service: AuthService = Depends(get_auth_service)):

    try:

        return await auth_service.login(data.username, data.password)

    except UserNoCorrectPassword as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )

    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
