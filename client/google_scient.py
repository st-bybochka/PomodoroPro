import requests
from dataclasses import dataclass

from schemas.auth import GoogleUserData
from settings import settings

@dataclass
class GoogleScient:

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code)
        user_info = requests.get(settings.GOOGLE_USER_INFO_URI,
                                 headers={"Authorization": f"Bearer {access_token}"})
        return GoogleUserData(**user_info.json(), access_token=access_token)


    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }

        response = requests.post(settings.GOOGLE_TOKEN_URI, data=data)
        print(response.json())
        return response.json()["access_token"]



