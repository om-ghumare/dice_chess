from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Color(str, Enum):
    WHITE = "white"
    BLACK = "black"

    def opposite(self) -> "Color":
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class PieceType(str, Enum):
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


@dataclass(frozen=True)
class Piece:
    kind: PieceType
    color: Color


Square = tuple[int, int]


@dataclass(frozen=True)
class MoveCommand:
    src: Square
    dst: Square
    promotion: PieceType | None = None


@dataclass(frozen=True)
class DiceRollResult:
    selected_piece_type: PieceType
    eligible_piece_types: tuple[PieceType, ...]


@dataclass(frozen=True)
class MoveValidationError:
    code: str
    message: str


@dataclass
class TurnContext:
    active_color: Color
    rolled_piece_type: PieceType | None = None
    move_number: int = 1


@dataclass
class GameState:
    board: dict[Square, Piece]
    turn: TurnContext
    white_king_moved: bool = False
    black_king_moved: bool = False
    white_rook_a_moved: bool = False
    white_rook_h_moved: bool = False
    black_rook_a_moved: bool = False
    black_rook_h_moved: bool = False
    en_passant_target: Square | None = None
    winner: Color | None = None
    is_stalemate: bool = False
    history: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class ApplyMoveResult:
    ok: bool
    state: GameState
    error: MoveValidationError | None = None
