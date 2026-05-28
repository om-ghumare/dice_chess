from __future__ import annotations

from app.core.store import QUEUE
from app.services.match_service import create_match


def enqueue_user(user_id: str) -> dict:
    if user_id not in QUEUE:
        QUEUE.append(user_id)
    if len(QUEUE) >= 2:
        white = QUEUE.pop(0)
        black = QUEUE.pop(0)
        match = create_match(white, black)
        return {"matched": True, "match_id": match.match_id, "white_user_id": white, "black_user_id": black}
    return {"matched": False}


def dequeue_user(user_id: str) -> None:
    while user_id in QUEUE:
        QUEUE.remove(user_id)
