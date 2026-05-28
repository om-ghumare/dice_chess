from __future__ import annotations

import secrets
import uuid

from app.core.store import TOKENS, USERS, UserRecord


def _token() -> str:
    return secrets.token_urlsafe(24)


def create_guest_user() -> tuple[str, str, str]:
    user_id = str(uuid.uuid4())
    USERS[user_id] = UserRecord(user_id=user_id, display_name=f"Guest-{user_id[:6]}", provider="guest")
    access = _token()
    refresh = _token()
    TOKENS[access] = user_id
    TOKENS[refresh] = user_id
    return access, refresh, user_id


def create_google_user(id_token: str) -> tuple[str, str, str]:
    # Stub validator for v1 scaffold.
    user_id = f"google-{id_token[-12:]}"
    if user_id not in USERS:
        USERS[user_id] = UserRecord(user_id=user_id, display_name=f"Google-{user_id[-6:]}", provider="google")
    access = _token()
    refresh = _token()
    TOKENS[access] = user_id
    TOKENS[refresh] = user_id
    return access, refresh, user_id


def refresh_tokens(refresh_token: str) -> tuple[str, str, str]:
    user_id = TOKENS.get(refresh_token)
    if not user_id:
        raise ValueError("Invalid refresh token")
    access = _token()
    refresh = _token()
    TOKENS[access] = user_id
    TOKENS[refresh] = user_id
    return access, refresh, user_id


def resolve_user(access_token: str) -> str:
    user_id = TOKENS.get(access_token)
    if not user_id:
        raise ValueError("Unauthorized")
    return user_id
