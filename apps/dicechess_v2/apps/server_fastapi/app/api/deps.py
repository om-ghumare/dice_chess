from fastapi import Header, HTTPException

from app.services.auth_service import resolve_user


def current_user_id(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        return resolve_user(token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
