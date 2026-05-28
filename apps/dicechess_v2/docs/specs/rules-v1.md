# Dice Chess Rules v1 (Preserved Behavior Contract)

This spec captures the v1 gameplay behavior to preserve from legacy code.

## Board and setup

- Standard 8x8 chess board.
- Standard initial chess placement.

## Turn structure

1. Active player rolls dice.
2. Dice result selects a piece type (`pawn`, `knight`, `bishop`, `rook`, `queen`, `king`).
3. Player must move a legal piece of that type.
4. If no legal move exists for that type, reroll from eligible piece types.
5. Turn passes after a successful legal move.

## Legal move constraints

- Standard chess move patterns for each piece.
- No move may leave own king in check.
- Castling is allowed if king/rook unmoved, path empty, and king path not in check.
- En passant allowed on immediate reply turn after double pawn advance.
- Promotion occurs on last rank (default options: bishop/knight/rook/queen).

## End conditions

- Checkmate: current player in check and no legal move.
- Stalemate: current player not in check and no legal move.
- King capture is not used as terminal condition; check/checkmate logic is authoritative.

## Dice eligibility

- Dice choices are limited to piece types that currently have at least one legal move.
- If no piece type has legal moves:
  - checkmate if in check
  - stalemate otherwise

## Determinism requirements

- Engine behavior must be deterministic given:
  - current state
  - dice face
  - chosen move
- Event replay must rebuild final state exactly.
