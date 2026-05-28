from __future__ import annotations

import copy
import random

from .types import (
    ApplyMoveResult,
    Color,
    DiceRollResult,
    GameState,
    MoveCommand,
    MoveValidationError,
    Piece,
    PieceType,
    Square,
    TurnContext,
)


def create_initial_state() -> GameState:
    board: dict[Square, Piece] = {}
    back = [
        PieceType.ROOK,
        PieceType.KNIGHT,
        PieceType.BISHOP,
        PieceType.QUEEN,
        PieceType.KING,
        PieceType.BISHOP,
        PieceType.KNIGHT,
        PieceType.ROOK,
    ]
    for x, kind in enumerate(back):
        board[(x, 7)] = Piece(kind=kind, color=Color.WHITE)
        board[(x, 0)] = Piece(kind=kind, color=Color.BLACK)
        board[(x, 6)] = Piece(kind=PieceType.PAWN, color=Color.WHITE)
        board[(x, 1)] = Piece(kind=PieceType.PAWN, color=Color.BLACK)
    return GameState(board=board, turn=TurnContext(active_color=Color.WHITE))


def in_bounds(square: Square) -> bool:
    return 0 <= square[0] <= 7 and 0 <= square[1] <= 7


def find_king(board: dict[Square, Piece], color: Color) -> Square | None:
    for sq, piece in board.items():
        if piece.color == color and piece.kind == PieceType.KING:
            return sq
    return None


def pseudo_legal_moves(state: GameState, src: Square) -> list[Square]:
    if src not in state.board:
        return []
    piece = state.board[src]
    x, y = src
    moves: list[Square] = []

    def add_ray(dx: int, dy: int) -> None:
        cx, cy = x + dx, y + dy
        while in_bounds((cx, cy)):
            target = state.board.get((cx, cy))
            if target is None:
                moves.append((cx, cy))
            else:
                if target.color != piece.color:
                    moves.append((cx, cy))
                break
            cx += dx
            cy += dy

    if piece.kind == PieceType.PAWN:
        step = -1 if piece.color == Color.WHITE else 1
        start_rank = 6 if piece.color == Color.WHITE else 1
        one = (x, y + step)
        two = (x, y + 2 * step)
        if in_bounds(one) and one not in state.board:
            moves.append(one)
            if y == start_rank and two not in state.board:
                moves.append(two)
        for dx in (-1, 1):
            cap = (x + dx, y + step)
            if in_bounds(cap):
                target = state.board.get(cap)
                if target is not None and target.color != piece.color:
                    moves.append(cap)
                if state.en_passant_target == cap:
                    moves.append(cap)
    elif piece.kind == PieceType.KNIGHT:
        for dx, dy in [
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
            (-1, 2),
        ]:
            dst = (x + dx, y + dy)
            if in_bounds(dst):
                target = state.board.get(dst)
                if target is None or target.color != piece.color:
                    moves.append(dst)
    elif piece.kind == PieceType.BISHOP:
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            add_ray(dx, dy)
    elif piece.kind == PieceType.ROOK:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            add_ray(dx, dy)
    elif piece.kind == PieceType.QUEEN:
        for dx, dy in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]:
            add_ray(dx, dy)
    else:  # king
        for dx, dy in [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        ]:
            dst = (x + dx, y + dy)
            if in_bounds(dst):
                target = state.board.get(dst)
                if target is None or target.color != piece.color:
                    moves.append(dst)
        moves.extend(_castle_targets(state, src))
    return moves


def _castle_targets(state: GameState, src: Square) -> list[Square]:
    if src not in state.board:
        return []
    king = state.board[src]
    if king.kind != PieceType.KING:
        return []
    if king.color == Color.WHITE:
        if state.white_king_moved or src != (4, 7):
            return []
        return _castle_targets_for_color(state, Color.WHITE)
    if state.black_king_moved or src != (4, 0):
        return []
    return _castle_targets_for_color(state, Color.BLACK)


def _castle_targets_for_color(state: GameState, color: Color) -> list[Square]:
    rank = 7 if color == Color.WHITE else 0
    results: list[Square] = []
    # kingside
    rook_h_moved = state.white_rook_h_moved if color == Color.WHITE else state.black_rook_h_moved
    if not rook_h_moved:
        if all((f, rank) not in state.board for f in (5, 6)):
            if not is_square_attacked(state, (4, rank), color.opposite()):
                if not is_square_attacked(state, (5, rank), color.opposite()):
                    if not is_square_attacked(state, (6, rank), color.opposite()):
                        rook = state.board.get((7, rank))
                        if rook and rook.color == color and rook.kind == PieceType.ROOK:
                            results.append((6, rank))
    # queenside
    rook_a_moved = state.white_rook_a_moved if color == Color.WHITE else state.black_rook_a_moved
    if not rook_a_moved:
        if all((f, rank) not in state.board for f in (1, 2, 3)):
            if not is_square_attacked(state, (4, rank), color.opposite()):
                if not is_square_attacked(state, (3, rank), color.opposite()):
                    if not is_square_attacked(state, (2, rank), color.opposite()):
                        rook = state.board.get((0, rank))
                        if rook and rook.color == color and rook.kind == PieceType.ROOK:
                            results.append((2, rank))
    return results


def is_square_attacked(state: GameState, square: Square, by_color: Color) -> bool:
    for src, piece in state.board.items():
        if piece.color != by_color:
            continue
        if piece.kind == PieceType.PAWN:
            step = -1 if piece.color == Color.WHITE else 1
            for dx in (-1, 1):
                if (src[0] + dx, src[1] + step) == square:
                    return True
            continue
        if square in pseudo_legal_moves_without_castle(state, src):
            return True
    return False


def pseudo_legal_moves_without_castle(state: GameState, src: Square) -> list[Square]:
    moves = pseudo_legal_moves(state, src)
    piece = state.board.get(src)
    if piece and piece.kind == PieceType.KING:
        rank = 7 if piece.color == Color.WHITE else 0
        moves = [m for m in moves if m not in {(6, rank), (2, rank)}]
    return moves


def apply_move_unchecked(state: GameState, move: MoveCommand) -> GameState:
    nxt = copy.deepcopy(state)
    piece = nxt.board.pop(move.src)
    captured = nxt.board.pop(move.dst, None)
    nxt.en_passant_target = None

    # en passant capture
    if piece.kind == PieceType.PAWN and move.src[0] != move.dst[0] and captured is None:
        cap_y = move.dst[1] + (1 if piece.color == Color.WHITE else -1)
        nxt.board.pop((move.dst[0], cap_y), None)

    # castling rook movement
    if piece.kind == PieceType.KING and abs(move.dst[0] - move.src[0]) == 2:
        rank = 7 if piece.color == Color.WHITE else 0
        if move.dst[0] == 6:
            rook_src, rook_dst = (7, rank), (5, rank)
        else:
            rook_src, rook_dst = (0, rank), (3, rank)
        rook = nxt.board.pop(rook_src)
        nxt.board[rook_dst] = rook

    # set en passant target after double-step
    if piece.kind == PieceType.PAWN and abs(move.dst[1] - move.src[1]) == 2:
        mid_y = (move.dst[1] + move.src[1]) // 2
        nxt.en_passant_target = (move.src[0], mid_y)

    # promotion
    if piece.kind == PieceType.PAWN and move.dst[1] in (0, 7):
        promote_to = move.promotion or PieceType.QUEEN
        piece = Piece(kind=promote_to, color=piece.color)

    nxt.board[move.dst] = piece

    # movement flags
    if piece.color == Color.WHITE:
        if piece.kind == PieceType.KING:
            nxt.white_king_moved = True
        if move.src == (0, 7):
            nxt.white_rook_a_moved = True
        if move.src == (7, 7):
            nxt.white_rook_h_moved = True
    else:
        if piece.kind == PieceType.KING:
            nxt.black_king_moved = True
        if move.src == (0, 0):
            nxt.black_rook_a_moved = True
        if move.src == (7, 0):
            nxt.black_rook_h_moved = True

    # captured rook flags
    if captured and captured.kind == PieceType.ROOK:
        if move.dst == (0, 7):
            nxt.white_rook_a_moved = True
        if move.dst == (7, 7):
            nxt.white_rook_h_moved = True
        if move.dst == (0, 0):
            nxt.black_rook_a_moved = True
        if move.dst == (7, 0):
            nxt.black_rook_h_moved = True

    nxt.turn.active_color = nxt.turn.active_color.opposite()
    nxt.turn.rolled_piece_type = None
    if nxt.turn.active_color == Color.WHITE:
        nxt.turn.move_number += 1
    return nxt


def in_check(state: GameState, color: Color) -> bool:
    king_sq = find_king(state.board, color)
    if king_sq is None:
        return True
    return is_square_attacked(state, king_sq, color.opposite())


def legal_moves_for_square(state: GameState, src: Square) -> list[Square]:
    piece = state.board.get(src)
    if not piece or piece.color != state.turn.active_color:
        return []
    legal: list[Square] = []
    for dst in pseudo_legal_moves(state, src):
        nxt = apply_move_unchecked(state, MoveCommand(src=src, dst=dst))
        if not in_check(nxt, piece.color):
            legal.append(dst)
    return legal


def legal_moves(state: GameState) -> dict[Square, list[Square]]:
    result: dict[Square, list[Square]] = {}
    for src, piece in state.board.items():
        if piece.color != state.turn.active_color:
            continue
        dests = legal_moves_for_square(state, src)
        if dests:
            result[src] = dests
    return result


def eligible_piece_types(state: GameState) -> list[PieceType]:
    found: list[PieceType] = []
    for src, moves in legal_moves(state).items():
        if not moves:
            continue
        kind = state.board[src].kind
        if kind not in found:
            found.append(kind)
    return found


def roll_dice(state: GameState, rng: random.Random | None = None) -> DiceRollResult:
    rng = rng or random.Random()
    eligible = eligible_piece_types(state)
    if not eligible:
        return DiceRollResult(selected_piece_type=PieceType.KING, eligible_piece_types=tuple())
    selected = eligible[rng.randrange(0, len(eligible))]
    state.turn.rolled_piece_type = selected
    return DiceRollResult(selected_piece_type=selected, eligible_piece_types=tuple(eligible))


def apply_move(state: GameState, move: MoveCommand) -> ApplyMoveResult:
    piece = state.board.get(move.src)
    if piece is None:
        return ApplyMoveResult(False, state, MoveValidationError("NO_PIECE", "No piece at source square"))
    if piece.color != state.turn.active_color:
        return ApplyMoveResult(False, state, MoveValidationError("WRONG_COLOR", "Piece is not active player color"))
    if state.turn.rolled_piece_type is None:
        return ApplyMoveResult(False, state, MoveValidationError("NO_ROLL", "Dice must be rolled first"))
    if piece.kind != state.turn.rolled_piece_type:
        return ApplyMoveResult(
            False,
            state,
            MoveValidationError("WRONG_PIECE_TYPE", "Move does not match dice-selected piece type"),
        )
    legal = legal_moves_for_square(state, move.src)
    if move.dst not in legal:
        return ApplyMoveResult(False, state, MoveValidationError("ILLEGAL_MOVE", "Move is not legal"))

    nxt = apply_move_unchecked(state, move)
    nxt.history.append(
        {
            "active_color_before": state.turn.active_color.value,
            "rolled_piece_type": state.turn.rolled_piece_type.value if state.turn.rolled_piece_type else None,
            "src": move.src,
            "dst": move.dst,
            "promotion": move.promotion.value if move.promotion else None,
        }
    )

    active_has_moves = bool(legal_moves(nxt))
    if not active_has_moves:
        if in_check(nxt, nxt.turn.active_color):
            nxt.winner = nxt.turn.active_color.opposite()
            nxt.is_stalemate = False
        else:
            nxt.winner = None
            nxt.is_stalemate = True
    return ApplyMoveResult(True, nxt, None)
