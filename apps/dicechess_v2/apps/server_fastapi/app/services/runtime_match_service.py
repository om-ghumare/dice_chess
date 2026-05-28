from __future__ import annotations

import random

from app.core.store import MATCHES, RUNTIME_MATCHES
from dice_chess_engine import MoveCommand, PieceType, apply_move, create_initial_state, roll_dice, serialize_state


def create_runtime(match_id: str, white_user_id: str, black_user_id: str) -> None:
    state = create_initial_state()
    RUNTIME_MATCHES[match_id] = {
        "state_obj": state,
        "seq": 0,
        "white_user_id": white_user_id,
        "black_user_id": black_user_id,
    }
    if match_id in MATCHES:
        MATCHES[match_id].state = serialize_state(state)


def get_runtime(match_id: str) -> dict | None:
    return RUNTIME_MATCHES.get(match_id)


def state_payload(match_id: str) -> dict:
    runtime = RUNTIME_MATCHES[match_id]
    return {
        "match_id": match_id,
        "seq": runtime["seq"],
        "state": serialize_state(runtime["state_obj"]),
    }


def player_color(runtime: dict, user_id: str) -> str | None:
    if runtime["white_user_id"] == user_id and runtime["black_user_id"] == user_id:
        # Local pass-and-play: same user controls both colors.
        return "both"
    if runtime["white_user_id"] == user_id:
        return "white"
    if runtime["black_user_id"] == user_id:
        return "black"
    return None


def is_player_turn(runtime: dict, user_id: str) -> bool:
    color = player_color(runtime, user_id)
    if color == "both":
        return True
    if color is None:
        return False
    return runtime["state_obj"].turn.active_color.value == color


def roll_for_turn(match_id: str) -> dict:
    runtime = RUNTIME_MATCHES[match_id]
    dice = roll_dice(runtime["state_obj"], random.Random())
    runtime["seq"] += 1
    if match_id in MATCHES:
        MATCHES[match_id].state = serialize_state(runtime["state_obj"])
    return {
        "match_id": match_id,
        "seq": runtime["seq"],
        "piece_type": dice.selected_piece_type.value,
        "eligible_piece_types": [x.value for x in dice.eligible_piece_types],
    }


def apply_move_for_turn(match_id: str, src: tuple[int, int], dst: tuple[int, int], promotion: str | None) -> tuple[bool, dict]:
    runtime = RUNTIME_MATCHES[match_id]
    state = runtime["state_obj"]
    move = MoveCommand(
        src=src,
        dst=dst,
        promotion=PieceType(promotion) if promotion else None,
    )
    result = apply_move(state, move)
    if not result.ok:
        return False, {"code": result.error.code, "message": result.error.message}
    runtime["state_obj"] = result.state
    runtime["seq"] += 1
    serialized = serialize_state(result.state)
    if match_id in MATCHES:
        MATCHES[match_id].state = serialized
        MATCHES[match_id].events.append({"src": list(src), "dst": list(dst), "promotion": promotion})
    return True, {"match_id": match_id, "seq": runtime["seq"], "state": serialized}
