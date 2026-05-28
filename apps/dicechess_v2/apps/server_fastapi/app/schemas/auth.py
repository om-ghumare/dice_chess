from pydantic import BaseModel


class GuestAuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str


class GoogleAuthRequest(BaseModel):
    id_token: str


class RefreshRequest(BaseModel):
    refresh_token: str
