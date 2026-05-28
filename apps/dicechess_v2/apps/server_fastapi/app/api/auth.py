from fastapi import APIRouter, HTTPException

from app.schemas.auth import GoogleAuthRequest, GuestAuthResponse, RefreshRequest
from app.services.auth_service import create_google_user, create_guest_user, refresh_tokens

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/guest", response_model=GuestAuthResponse)
def auth_guest() -> GuestAuthResponse:
    access, refresh, user_id = create_guest_user()
    return GuestAuthResponse(access_token=access, refresh_token=refresh, user_id=user_id)


@router.post("/google", response_model=GuestAuthResponse)
def auth_google(payload: GoogleAuthRequest) -> GuestAuthResponse:
    if not payload.id_token:
        raise HTTPException(status_code=400, detail="id_token required")
    access, refresh, user_id = create_google_user(payload.id_token)
    return GuestAuthResponse(access_token=access, refresh_token=refresh, user_id=user_id)


@router.post("/refresh", response_model=GuestAuthResponse)
def auth_refresh(payload: RefreshRequest) -> GuestAuthResponse:
    try:
        access, refresh, user_id = refresh_tokens(payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return GuestAuthResponse(access_token=access, refresh_token=refresh, user_id=user_id)
