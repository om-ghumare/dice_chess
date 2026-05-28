from pydantic import BaseModel


class ProfileResponse(BaseModel):
    user_id: str
    display_name: str
    provider: str
    wins: int = 0
    losses: int = 0
    draws: int = 0


class ProfilePatchRequest(BaseModel):
    display_name: str
