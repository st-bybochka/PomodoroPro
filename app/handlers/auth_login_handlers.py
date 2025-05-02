from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse

from app.exceptions import UserIncorrectLoginOrPasswordException, UserNotFoundException
from app.schemas import UserLoginSchema, UserResponseSchema
from app.service import AuthService
from app.dependencies import get_auth_login_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=UserResponseSchema)
async def login(
        response: Response,
        data: UserLoginSchema,
        auth_service: AuthService = Depends(get_auth_login_service),

) -> UserResponseSchema:

    try:

        return await auth_service.login(data, response)

    except UserIncorrectLoginOrPasswordException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )

    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
@router.get("/logout")
async def logout(
        response: Response,
        auth_service: AuthService = Depends(get_auth_login_service),
):
    return await auth_service.logout(response)