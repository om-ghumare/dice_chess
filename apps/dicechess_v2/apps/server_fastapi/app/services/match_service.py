from __future__ import annotations

import uuid

from app.core.store import MATCHES, MatchRecord
from dice_chess_engine import create_initial_state, serialize_state
from app.services.runtime_match_service import create_runtime


def create_match(white_user_id: str, black_user_id: str) -> MatchRecord:
    match_id = str(uuid.uuid4())
    initial = serialize_state(create_initial_state())
    record = MatchRecord(
        match_id=match_id,
        white_user_id=white_user_id,
        black_user_id=black_user_id,
        state=initial,
    )
    MATCHES[match_id] = record
    create_runtime(match_id, white_user_id, black_user_id)
    return record
