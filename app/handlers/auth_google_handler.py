from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse

from app.dependencies import get_auth_google_service
from app.service.auth_google_service import AuthGoogleService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/login/google",
            response_class=RedirectResponse
            )
async def google_login(
        auth_google_service: AuthGoogleService = Depends(get_auth_google_service)
):
    redirect_url = await auth_google_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get("/callback")
async def google_auth(
        response: Response,
        code: str,
        auth_google_service: AuthGoogleService = Depends(get_auth_google_service),

):
    return await auth_google_service.google_auth(code=code, response=response)
