from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.annotation import Annotated
from fastapi.responses import RedirectResponse

from exceptions import UserNoCorrectPassword, UserNotFoundException
from schemas import UserLoginSchema, UserCreateSchema
from service import AuthService
from dependencies import get_auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=UserLoginSchema)
async def login(
        data: UserCreateSchema,
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

@router.get("/login/google",
            response_class=RedirectResponse
            )
async def google_login(
        auth_service: AuthService = Depends(get_auth_service)
):
    redirect_url = await auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)

@router.get("/callback")
async def google_auth(
        code: str,
        auth_service: AuthService = Depends(get_auth_service),

):
    return await auth_service.google_auth(code=code)
