// ============================================================
// Dice Chess — Check / Checkmate / Stalemate Detection
// ============================================================

import { Piece, PieceType, Color, Square, GameState } from './types';
import { getPieceAt, isInBounds, findKing, findPieces, oppositeColor } from './board';
import { getPseudoLegalMoves, applyMoveToBoard } from './moves';

/**
 * Check if a square is attacked by any piece of the given attacker color.
 * This is a raw check (doesn't recurse into legal move computation).
 */
export function isSquareAttacked(board: (Piece | null)[][], square: Square, attackerColor: Color): boolean {
    const [row, col] = square;

    // Check pawn attacks
    const pawnDir = attackerColor === Color.WHITE ? 1 : -1; // pawns of attackerColor attack in this direction
    for (const dc of [-1, 1]) {
        const pr = row + pawnDir;
        const pc = col + dc;
        if (isInBounds(pr, pc)) {
            const p = getPieceAt(board, [pr, pc]);
            if (p && p.type === PieceType.PAWN && p.color === attackerColor) return true;
        }
    }

    // Check knight attacks
    const knightOffsets: [number, number][] = [
        [-2, -1], [-2, 1], [-1, -2], [-1, 2],
        [1, -2], [1, 2], [2, -1], [2, 1],
    ];
    for (const [dr, dc] of knightOffsets) {
        const r = row + dr;
        const c = col + dc;
        if (isInBounds(r, c)) {
            const p = getPieceAt(board, [r, c]);
            if (p && p.type === PieceType.KNIGHT && p.color === attackerColor) return true;
        }
    }

    // Check king attacks (adjacent squares)
    const kingOffsets: [number, number][] = [
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1], [0, 1],
        [1, -1], [1, 0], [1, 1],
    ];
    for (const [dr, dc] of kingOffsets) {
        const r = row + dr;
        const c = col + dc;
        if (isInBounds(r, c)) {
            const p = getPieceAt(board, [r, c]);
            if (p && p.type === PieceType.KING && p.color === attackerColor) return true;
        }
    }

    // Check sliding piece attacks (rook/queen on ranks/files, bishop/queen on diagonals)
    const rookDirs: [number, number][] = [[0, 1], [0, -1], [1, 0], [-1, 0]];
    for (const [dr, dc] of rookDirs) {
        let r = row + dr;
        let c = col + dc;
        while (isInBounds(r, c)) {
            const p = getPieceAt(board, [r, c]);
            if (p) {
                if (p.color === attackerColor && (p.type === PieceType.ROOK || p.type === PieceType.QUEEN)) {
                    return true;
                }
                break;
            }
            r += dr;
            c += dc;
        }
    }

    const bishopDirs: [number, number][] = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
    for (const [dr, dc] of bishopDirs) {
        let r = row + dr;
        let c = col + dc;
        while (isInBounds(r, c)) {
            const p = getPieceAt(board, [r, c]);
            if (p) {
                if (p.color === attackerColor && (p.type === PieceType.BISHOP || p.type === PieceType.QUEEN)) {
                    return true;
                }
                break;
            }
            r += dr;
            c += dc;
        }
    }

    return false;
}

/** Check if the given color's king is in check */
export function isInCheck(board: (Piece | null)[][], color: Color): boolean {
    const kingPos = findKing(board, color);
    if (!kingPos) return false;
    return isSquareAttacked(board, kingPos, oppositeColor(color));
}

/** Check if the given color has any legal moves */
export function hasLegalMoves(state: GameState, color: Color): boolean {
    const pieces = findPieces(state.board, color);

    for (const { piece, square } of pieces) {
        const pieceMoves = getPseudoLegalMoves(state.board, square, piece, state.enPassantTarget);
        for (const move of pieceMoves) {
            const newBoard = applyMoveToBoard(state.board, move);
            const kingPos = findKing(newBoard, color);
            if (kingPos && !isSquareAttacked(newBoard, kingPos, oppositeColor(color))) {
                return true;
            }
        }
    }
    return false;
}

/** Check if it's checkmate for the given color */
export function isCheckmate(state: GameState, color: Color): boolean {
    return isInCheck(state.board, color) && !hasLegalMoves(state, color);
}

/** Check if it's stalemate for the given color */
export function isStalemate(state: GameState, color: Color): boolean {
    return !isInCheck(state.board, color) && !hasLegalMoves(state, color);
}
