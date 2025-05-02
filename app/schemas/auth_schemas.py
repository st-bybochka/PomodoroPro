from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    google_id: str = Field(..., alias="id")
    email: str
    verified_email: bool
    access_token: str
