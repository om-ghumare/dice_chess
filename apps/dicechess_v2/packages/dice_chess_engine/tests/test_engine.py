import random

from dice_chess_engine import MoveCommand, PieceType, apply_move, create_initial_state, replay_history, roll_dice


def test_initial_roll_has_eligible_types():
    state = create_initial_state()
    result = roll_dice(state, random.Random(1))
    assert result.selected_piece_type in result.eligible_piece_types
    assert len(result.eligible_piece_types) > 0


def test_wrong_piece_type_rejected():
    state = create_initial_state()
    state.turn.rolled_piece_type = PieceType.KNIGHT
    move = MoveCommand(src=(4, 6), dst=(4, 5))
    result = apply_move(state, move)
    assert not result.ok
    assert result.error.code == "WRONG_PIECE_TYPE"


def test_legal_pawn_move_accepted():
    state = create_initial_state()
    state.turn.rolled_piece_type = PieceType.PAWN
    move = MoveCommand(src=(4, 6), dst=(4, 4))
    result = apply_move(state, move)
    assert result.ok
    assert (4, 4) in result.state.board


def test_replay_matches_final_state():
    state = create_initial_state()
    state.turn.rolled_piece_type = PieceType.PAWN
    step1 = apply_move(state, MoveCommand(src=(4, 6), dst=(4, 4)))
    assert step1.ok
    s1 = step1.state
    s1.turn.rolled_piece_type = PieceType.PAWN
    step2 = apply_move(s1, MoveCommand(src=(4, 1), dst=(4, 3)))
    assert step2.ok
    final_state = step2.state

    replayed = replay_history(final_state.history)
    assert len(replayed.board) == len(final_state.board)
    assert replayed.turn.active_color == final_state.turn.active_color
