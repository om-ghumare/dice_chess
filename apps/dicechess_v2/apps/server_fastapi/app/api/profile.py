from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import current_user_id
from app.core.store import USERS
from app.schemas.profile import ProfilePatchRequest, ProfileResponse

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=ProfileResponse)
def get_me(user_id: str = Depends(current_user_id)) -> ProfileResponse:
    record = USERS.get(user_id)
    if not record:
        raise HTTPException(status_code=404, detail="User not found")
    return ProfileResponse(user_id=record.user_id, display_name=record.display_name, provider=record.provider)


@router.patch("/me", response_model=ProfileResponse)
def patch_me(payload: ProfilePatchRequest, user_id: str = Depends(current_user_id)) -> ProfileResponse:
    record = USERS.get(user_id)
    if not record:
        raise HTTPException(status_code=404, detail="User not found")
    record.display_name = payload.display_name.strip() or record.display_name
    return ProfileResponse(user_id=record.user_id, display_name=record.display_name, provider=record.provider)
