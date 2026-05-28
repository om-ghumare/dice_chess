// ============================================================
// Dice Chess — Dice Mechanic
// ============================================================

import { PieceType, Color, GameState, Square } from './types';
import { findPieces } from './board';
import { getLegalMovesForSquare } from './moves';

/**
 * Get all piece types of the given color that have at least one legal move.
 * This is what faces appear on the dice.
 */
export function getAvailablePieceTypes(state: GameState, color: Color): PieceType[] {
    const pieces = findPieces(state.board, color);
    const typesWithMoves = new Set<PieceType>();

    for (const { piece, square } of pieces) {
        if (typesWithMoves.has(piece.type)) continue; // already know this type has moves
        const moves = getLegalMovesForSquare(state, square);
        if (moves.length > 0) {
            typesWithMoves.add(piece.type);
        }
    }

    return Array.from(typesWithMoves);
}

/**
 * Roll the dice — randomly select from available piece types.
 * Returns null if no moves available (shouldn't happen normally — indicates checkmate/stalemate).
 */
export function rollDice(state: GameState, color: Color): PieceType | null {
    const available = getAvailablePieceTypes(state, color);
    if (available.length === 0) return null;
    const index = Math.floor(Math.random() * available.length);
    return available[index];
}

/**
 * Get all squares containing pieces of the dice-rolled type that have legal moves.
 * These are the pieces the player can choose from.
 */
export function getHighlightedPieces(state: GameState, color: Color, pieceType: PieceType): Square[] {
    const pieces = findPieces(state.board, color);
    const highlighted: Square[] = [];

    for (const { piece, square } of pieces) {
        if (piece.type !== pieceType) continue;
        const moves = getLegalMovesForSquare(state, square);
        if (moves.length > 0) {
            highlighted.push(square);
        }
    }

    return highlighted;
}
