// ============================================================
// Dice Chess — AI Engine (Minimax with Alpha-Beta Pruning)
// ============================================================

import { GameState, PieceType, Color, Move, Square, AIDifficulty } from './types';
import { cloneBoard, findPieces, oppositeColor, getPieceAt, setPieceAt, findKing, squaresEqual } from './board';
import { getAllLegalMoves, getLegalMovesForSquare, applyMoveToBoard } from './moves';
import { isSquareAttacked, isInCheck } from './validation';
import { rollDice, getHighlightedPieces, getAvailablePieceTypes } from './dice';

// ── Piece Values ────────────────────────────────────────────

const PIECE_VALUES: Record<PieceType, number> = {
    [PieceType.PAWN]: 100,
    [PieceType.KNIGHT]: 320,
    [PieceType.BISHOP]: 330,
    [PieceType.ROOK]: 500,
    [PieceType.QUEEN]: 900,
    [PieceType.KING]: 20000,
};

// ── Positional Tables (from white's perspective, flipped for black) ─

const PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0],
];

const KNIGHT_TABLE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50],
];

const BISHOP_TABLE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 10, 5, 10, 10, 5, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20],
];

const ROOK_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0],
];

const QUEEN_TABLE = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20],
];

const KING_TABLE = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20],
];

const POSITION_TABLES: Record<PieceType, number[][]> = {
    [PieceType.PAWN]: PAWN_TABLE,
    [PieceType.KNIGHT]: KNIGHT_TABLE,
    [PieceType.BISHOP]: BISHOP_TABLE,
    [PieceType.ROOK]: ROOK_TABLE,
    [PieceType.QUEEN]: QUEEN_TABLE,
    [PieceType.KING]: KING_TABLE,
};

// ── Evaluation ──────────────────────────────────────────────

function getPositionalValue(piece: PieceType, row: number, col: number, color: Color): number {
    const table = POSITION_TABLES[piece];
    // For black, flip the table vertically
    const r = color === Color.WHITE ? row : 7 - row;
    return table[r][col];
}

function evaluateBoard(board: (Piece | null)[][]): number {
    let score = 0;

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const piece = board[row][col];
            if (!piece) continue;

            const materialValue = PIECE_VALUES[piece.type];
            const positionalValue = getPositionalValue(piece.type, row, col, piece.color);
            const total = materialValue + positionalValue;

            if (piece.color === Color.WHITE) {
                score += total;
            } else {
                score -= total;
            }
        }
    }

    return score;
}

// ── Minimax with Alpha-Beta ─────────────────────────────────

function minimax(
    state: GameState,
    depth: number,
    alpha: number,
    beta: number,
    isMaximizing: boolean,
): number {
    if (depth === 0) {
        return evaluateBoard(state.board);
    }

    const color = isMaximizing ? Color.WHITE : Color.BLACK;
    const moves = getAllLegalMoves(state, color);

    if (moves.length === 0) {
        if (isInCheck(state.board, color)) {
            // Checkmate — worst possible score
            return isMaximizing ? -Infinity : Infinity;
        }
        return 0; // Stalemate
    }

    if (isMaximizing) {
        let maxEval = -Infinity;
        for (const move of moves) {
            const newBoard = applyMoveToBoard(state.board, move);
            const newState: GameState = {
                ...state,
                board: newBoard,
                enPassantTarget: move.piece === PieceType.PAWN && Math.abs(move.to[0] - move.from[0]) === 2
                    ? [(move.from[0] + move.to[0]) / 2, move.from[1]]
                    : null,
            };
            const evalScore = minimax(newState, depth - 1, alpha, beta, false);
            maxEval = Math.max(maxEval, evalScore);
            alpha = Math.max(alpha, evalScore);
            if (beta <= alpha) break;
        }
        return maxEval;
    } else {
        let minEval = Infinity;
        for (const move of moves) {
            const newBoard = applyMoveToBoard(state.board, move);
            const newState: GameState = {
                ...state,
                board: newBoard,
                enPassantTarget: move.piece === PieceType.PAWN && Math.abs(move.to[0] - move.from[0]) === 2
                    ? [(move.from[0] + move.to[0]) / 2, move.from[1]]
                    : null,
            };
            const evalScore = minimax(newState, depth - 1, alpha, beta, true);
            minEval = Math.min(minEval, evalScore);
            beta = Math.min(beta, evalScore);
            if (beta <= alpha) break;
        }
        return minEval;
    }
}

// ── Public API ──────────────────────────────────────────────

const DEPTH_MAP: Record<AIDifficulty, number> = {
    easy: 1,
    medium: 2,
    hard: 3,
};

/**
 * Get the best move for the AI given the current game state and dice result.
 * The AI only considers moves for pieces of the rolled type.
 */
export function getBestAIMove(state: GameState, aiColor: Color, diceResult: PieceType, difficulty: AIDifficulty): Move | null {
    const depth = DEPTH_MAP[difficulty];
    const isMaximizing = aiColor === Color.WHITE;

    // Get all pieces of the rolled type that have legal moves
    const pieces = findPieces(state.board, aiColor);
    const candidateMoves: Move[] = [];

    for (const { piece, square } of pieces) {
        if (piece.type !== diceResult) continue;
        const moves = getLegalMovesForSquare(state, square);
        candidateMoves.push(...moves);
    }

    if (candidateMoves.length === 0) return null;

    // Shuffle for variety when moves have equal evaluation
    for (let i = candidateMoves.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [candidateMoves[i], candidateMoves[j]] = [candidateMoves[j], candidateMoves[i]];
    }

    let bestMove: Move | null = null;
    let bestEval = isMaximizing ? -Infinity : Infinity;

    for (const move of candidateMoves) {
        const newBoard = applyMoveToBoard(state.board, move);
        const newState: GameState = {
            ...state,
            board: newBoard,
            enPassantTarget: move.piece === PieceType.PAWN && Math.abs(move.to[0] - move.from[0]) === 2
                ? [(move.from[0] + move.to[0]) / 2, move.from[1]]
                : null,
        };

        const evalScore = minimax(newState, depth - 1, -Infinity, Infinity, !isMaximizing);

        if (isMaximizing ? evalScore > bestEval : evalScore < bestEval) {
            bestEval = evalScore;
            bestMove = move;
        }
    }

    return bestMove;
}

/**
 * Perform the AI's complete turn: roll dice, pick best move.
 * Returns the dice result and the chosen move.
 */
export function performAITurn(state: GameState, aiColor: Color, difficulty: AIDifficulty): { diceResult: PieceType; move: Move } | null {
    const diceResult = rollDice(state, aiColor);
    if (!diceResult) return null;

    const move = getBestAIMove(state, aiColor, diceResult, difficulty);
    if (!move) return null;

    return { diceResult, move };
}
