// ============================================================
// Dice Chess — Legal Move Generation
// ============================================================

import { Piece, PieceType, Color, Square, Move, GameState } from './types';
import { getPieceAt, isInBounds, findPieces, cloneBoard, setPieceAt, findKing, oppositeColor, squaresEqual } from './board';
import { isSquareAttacked } from './validation';

// ── Pawn Moves ──────────────────────────────────────────────

function getPawnMoves(board: (Piece | null)[][], square: Square, color: Color, enPassantTarget: Square | null): Move[] {
    const moves: Move[] = [];
    const [row, col] = square;
    const direction = color === Color.WHITE ? -1 : 1;
    const startRow = color === Color.WHITE ? 6 : 1;
    const promoRow = color === Color.WHITE ? 0 : 7;

    // Forward one
    const oneAhead: Square = [row + direction, col];
    if (isInBounds(oneAhead[0], oneAhead[1]) && !getPieceAt(board, oneAhead)) {
        if (oneAhead[0] === promoRow) {
            for (const promo of [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]) {
                moves.push({ from: square, to: oneAhead, piece: PieceType.PAWN, promotion: promo });
            }
        } else {
            moves.push({ from: square, to: oneAhead, piece: PieceType.PAWN });
        }

        // Forward two from start
        if (row === startRow) {
            const twoAhead: Square = [row + 2 * direction, col];
            if (!getPieceAt(board, twoAhead)) {
                moves.push({ from: square, to: twoAhead, piece: PieceType.PAWN });
            }
        }
    }

    // Diagonal captures
    for (const dc of [-1, 1]) {
        const target: Square = [row + direction, col + dc];
        if (!isInBounds(target[0], target[1])) continue;

        const targetPiece = getPieceAt(board, target);
        if (targetPiece && targetPiece.color !== color) {
            if (target[0] === promoRow) {
                for (const promo of [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]) {
                    moves.push({ from: square, to: target, piece: PieceType.PAWN, captured: targetPiece.type, promotion: promo });
                }
            } else {
                moves.push({ from: square, to: target, piece: PieceType.PAWN, captured: targetPiece.type });
            }
        }

        // En passant
        if (enPassantTarget && squaresEqual(target, enPassantTarget)) {
            moves.push({ from: square, to: target, piece: PieceType.PAWN, captured: PieceType.PAWN, enPassant: true });
        }
    }

    return moves;
}

// ── Sliding Pieces (Rook, Bishop, Queen) ────────────────────

function getSlidingMoves(board: (Piece | null)[][], square: Square, color: Color, directions: [number, number][], pieceType: PieceType): Move[] {
    const moves: Move[] = [];
    const [row, col] = square;

    for (const [dr, dc] of directions) {
        let r = row + dr;
        let c = col + dc;
        while (isInBounds(r, c)) {
            const target = getPieceAt(board, [r, c]);
            if (target) {
                if (target.color !== color) {
                    moves.push({ from: square, to: [r, c], piece: pieceType, captured: target.type });
                }
                break;
            }
            moves.push({ from: square, to: [r, c], piece: pieceType });
            r += dr;
            c += dc;
        }
    }

    return moves;
}

function getRookMoves(board: (Piece | null)[][], square: Square, color: Color): Move[] {
    return getSlidingMoves(board, square, color, [[0, 1], [0, -1], [1, 0], [-1, 0]], PieceType.ROOK);
}

function getBishopMoves(board: (Piece | null)[][], square: Square, color: Color): Move[] {
    return getSlidingMoves(board, square, color, [[1, 1], [1, -1], [-1, 1], [-1, -1]], PieceType.BISHOP);
}

function getQueenMoves(board: (Piece | null)[][], square: Square, color: Color): Move[] {
    return getSlidingMoves(board, square, color, [
        [0, 1], [0, -1], [1, 0], [-1, 0],
        [1, 1], [1, -1], [-1, 1], [-1, -1],
    ], PieceType.QUEEN);
}

// ── Knight Moves ────────────────────────────────────────────

function getKnightMoves(board: (Piece | null)[][], square: Square, color: Color): Move[] {
    const moves: Move[] = [];
    const [row, col] = square;
    const offsets: [number, number][] = [
        [-2, -1], [-2, 1], [-1, -2], [-1, 2],
        [1, -2], [1, 2], [2, -1], [2, 1],
    ];

    for (const [dr, dc] of offsets) {
        const r = row + dr;
        const c = col + dc;
        if (!isInBounds(r, c)) continue;
        const target = getPieceAt(board, [r, c]);
        if (target && target.color === color) continue;
        moves.push({
            from: square,
            to: [r, c],
            piece: PieceType.KNIGHT,
            captured: target?.type,
        });
    }

    return moves;
}

// ── King Moves ──────────────────────────────────────────────

function getKingBasicMoves(board: (Piece | null)[][], square: Square, color: Color): Move[] {
    const moves: Move[] = [];
    const [row, col] = square;
    const offsets: [number, number][] = [
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1], [0, 1],
        [1, -1], [1, 0], [1, 1],
    ];

    for (const [dr, dc] of offsets) {
        const r = row + dr;
        const c = col + dc;
        if (!isInBounds(r, c)) continue;
        const target = getPieceAt(board, [r, c]);
        if (target && target.color === color) continue;
        moves.push({
            from: square,
            to: [r, c],
            piece: PieceType.KING,
            captured: target?.type,
        });
    }

    return moves;
}

function getCastlingMoves(state: GameState, color: Color): Move[] {
    const moves: Move[] = [];
    const row = color === Color.WHITE ? 7 : 0;
    const enemyColor = oppositeColor(color);

    // Can't castle while in check
    if (isSquareAttacked(state.board, findKing(state.board, color)!, enemyColor)) {
        return moves;
    }

    const kingSide = color === Color.WHITE ? state.castlingRights.whiteKingside : state.castlingRights.blackKingside;
    const queenSide = color === Color.WHITE ? state.castlingRights.whiteQueenside : state.castlingRights.blackQueenside;

    // Kingside: king moves from e to g, rook from h to f
    if (kingSide) {
        const pathClear = !getPieceAt(state.board, [row, 5]) && !getPieceAt(state.board, [row, 6]);
        const pathSafe = !isSquareAttacked(state.board, [row, 5], enemyColor) &&
            !isSquareAttacked(state.board, [row, 6], enemyColor);
        if (pathClear && pathSafe) {
            moves.push({ from: [row, 4], to: [row, 6], piece: PieceType.KING, castling: 'kingside' });
        }
    }

    // Queenside: king moves from e to c, rook from a to d
    if (queenSide) {
        const pathClear = !getPieceAt(state.board, [row, 3]) && !getPieceAt(state.board, [row, 2]) && !getPieceAt(state.board, [row, 1]);
        const pathSafe = !isSquareAttacked(state.board, [row, 3], enemyColor) &&
            !isSquareAttacked(state.board, [row, 2], enemyColor);
        if (pathClear && pathSafe) {
            moves.push({ from: [row, 4], to: [row, 2], piece: PieceType.KING, castling: 'queenside' });
        }
    }

    return moves;
}

// ── Pseudo-Legal & Legal Move Generation ────────────────────

/** Get pseudo-legal moves for a single piece (doesn't check if king is left in check) */
export function getPseudoLegalMoves(board: (Piece | null)[][], square: Square, piece: Piece, enPassantTarget: Square | null): Move[] {
    switch (piece.type) {
        case PieceType.PAWN: return getPawnMoves(board, square, piece.color, enPassantTarget);
        case PieceType.KNIGHT: return getKnightMoves(board, square, piece.color);
        case PieceType.BISHOP: return getBishopMoves(board, square, piece.color);
        case PieceType.ROOK: return getRookMoves(board, square, piece.color);
        case PieceType.QUEEN: return getQueenMoves(board, square, piece.color);
        case PieceType.KING: return getKingBasicMoves(board, square, piece.color);
    }
}

/** Apply a move to a cloned board (for checking legality) */
export function applyMoveToBoard(board: (Piece | null)[][], move: Move): (Piece | null)[][] {
    const newBoard = cloneBoard(board);
    const piece = getPieceAt(newBoard, move.from)!;

    // Clear the source
    setPieceAt(newBoard, move.from, null);

    // Handle en passant capture
    if (move.enPassant) {
        const capturedPawnRow = move.from[0]; // captured pawn is on the same row as the moving pawn
        setPieceAt(newBoard, [capturedPawnRow, move.to[1]], null);
    }

    // Handle castling
    if (move.castling) {
        const row = move.from[0];
        if (move.castling === 'kingside') {
            setPieceAt(newBoard, [row, 7], null); // remove rook
            setPieceAt(newBoard, [row, 5], { type: PieceType.ROOK, color: piece.color }); // place rook
        } else {
            setPieceAt(newBoard, [row, 0], null);
            setPieceAt(newBoard, [row, 3], { type: PieceType.ROOK, color: piece.color });
        }
    }

    // Handle promotion
    if (move.promotion) {
        setPieceAt(newBoard, move.to, { type: move.promotion, color: piece.color });
    } else {
        setPieceAt(newBoard, move.to, piece);
    }

    return newBoard;
}

/** Get all legal moves for a color (filters pseudo-legal moves that leave king in check) */
export function getAllLegalMoves(state: GameState, color: Color): Move[] {
    const moves: Move[] = [];
    const pieces = findPieces(state.board, color);

    for (const { piece, square } of pieces) {
        const pieceMoves = getPseudoLegalMoves(state.board, square, piece, state.enPassantTarget);
        for (const move of pieceMoves) {
            const newBoard = applyMoveToBoard(state.board, move);
            const kingPos = findKing(newBoard, color);
            if (kingPos && !isSquareAttacked(newBoard, kingPos, oppositeColor(color))) {
                moves.push(move);
            }
        }
    }

    // Add castling moves (king-specific)
    const castlingMoves = getCastlingMoves(state, color);
    moves.push(...castlingMoves);

    return moves;
}

/** Get legal moves for a specific piece at a square */
export function getLegalMovesForSquare(state: GameState, square: Square): Move[] {
    const piece = getPieceAt(state.board, square);
    if (!piece) return [];

    const allMoves: Move[] = [];

    // Regular moves
    const pieceMoves = getPseudoLegalMoves(state.board, square, piece, state.enPassantTarget);
    for (const move of pieceMoves) {
        const newBoard = applyMoveToBoard(state.board, move);
        const kingPos = findKing(newBoard, piece.color);
        if (kingPos && !isSquareAttacked(newBoard, kingPos, oppositeColor(piece.color))) {
            allMoves.push(move);
        }
    }

    // Castling (only for king)
    if (piece.type === PieceType.KING) {
        const castlingMoves = getCastlingMoves(state, piece.color);
        allMoves.push(...castlingMoves);
    }

    return allMoves;
}
