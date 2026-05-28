from __future__ import annotations

import secrets
import string
from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def room_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(6))


@dataclass
class UserRecord:
    user_id: str
    display_name: str
    provider: str
    created_at: str = field(default_factory=utc_now_iso)


@dataclass
class MatchRecord:
    match_id: str
    white_user_id: str
    black_user_id: str
    state: dict
    events: list[dict] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)
    finished_at: str | None = None


USERS: dict[str, UserRecord] = {}
TOKENS: dict[str, str] = {}
ROOMS: dict[str, list[str]] = {}
QUEUE: list[str] = []
MATCHES: dict[str, MatchRecord] = {}
RUNTIME_MATCHES: dict[str, dict] = {}
