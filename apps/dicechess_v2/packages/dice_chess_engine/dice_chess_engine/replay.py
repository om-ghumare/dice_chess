from __future__ import annotations

from .engine import apply_move, create_initial_state
from .types import GameState, MoveCommand, PieceType


def serialize_state(state: GameState) -> dict:
    board = [
        {"x": x, "y": y, "kind": p.kind.value, "color": p.color.value}
        for (x, y), p in sorted(state.board.items(), key=lambda i: (i[0][1], i[0][0]))
    ]
    return {
        "board": board,
        "turn": {
            "active_color": state.turn.active_color.value,
            "rolled_piece_type": state.turn.rolled_piece_type.value if state.turn.rolled_piece_type else None,
            "move_number": state.turn.move_number,
        },
        "castling_flags": {
            "white_king_moved": state.white_king_moved,
            "black_king_moved": state.black_king_moved,
            "white_rook_a_moved": state.white_rook_a_moved,
            "white_rook_h_moved": state.white_rook_h_moved,
            "black_rook_a_moved": state.black_rook_a_moved,
            "black_rook_h_moved": state.black_rook_h_moved,
        },
        "en_passant_target": state.en_passant_target,
        "winner": state.winner.value if state.winner else None,
        "is_stalemate": state.is_stalemate,
    }


def replay_history(events: list[dict]) -> GameState:
    state = create_initial_state()
    for event in events:
        rolled = event.get("rolled_piece_type")
        if rolled:
            state.turn.rolled_piece_type = PieceType(rolled)
        move = MoveCommand(
            src=tuple(event["src"]),
            dst=tuple(event["dst"]),
            promotion=PieceType(event["promotion"]) if event.get("promotion") else None,
        )
        result = apply_move(state, move)
        if not result.ok:
            raise ValueError(f"Invalid event during replay: {result.error.code}")
        state = result.state
    return state
