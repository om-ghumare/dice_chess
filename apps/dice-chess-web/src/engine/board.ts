// ============================================================
// Dice Chess — Board Representation & Utilities
// ============================================================

import { Piece, PieceType, Color, Square, CastlingRights, GameState, GamePhase } from './types';

/** Create the standard initial chess board */
export function createInitialBoard(): (Piece | null)[][] {
    const board: (Piece | null)[][] = Array.from({ length: 8 }, () =>
        Array(8).fill(null)
    );

    // Black pieces (row 0)
    const backRank: PieceType[] = [
        PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
        PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK,
    ];

    for (let col = 0; col < 8; col++) {
        board[0][col] = { type: backRank[col], color: Color.BLACK };
        board[1][col] = { type: PieceType.PAWN, color: Color.BLACK };
        board[6][col] = { type: PieceType.PAWN, color: Color.WHITE };
        board[7][col] = { type: backRank[col], color: Color.WHITE };
    }

    return board;
}

/** Deep clone the board */
export function cloneBoard(board: (Piece | null)[][]): (Piece | null)[][] {
    return board.map(row =>
        row.map(cell => (cell ? { ...cell } : null))
    );
}

/** Get the piece at a given square */
export function getPieceAt(board: (Piece | null)[][], square: Square): Piece | null {
    const [row, col] = square;
    if (row < 0 || row > 7 || col < 0 || col > 7) return null;
    return board[row][col];
}

/** Set a piece at a given square */
export function setPieceAt(board: (Piece | null)[][], square: Square, piece: Piece | null): void {
    const [row, col] = square;
    board[row][col] = piece;
}

/** Check if a square is within bounds */
export function isInBounds(row: number, col: number): boolean {
    return row >= 0 && row <= 7 && col >= 0 && col <= 7;
}

/** Find all squares containing pieces of a given color */
export function findPieces(board: (Piece | null)[][], color: Color): { piece: Piece; square: Square }[] {
    const result: { piece: Piece; square: Square }[] = [];
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const piece = board[row][col];
            if (piece && piece.color === color) {
                result.push({ piece, square: [row, col] });
            }
        }
    }
    return result;
}

/** Find the king's position for a given color */
export function findKing(board: (Piece | null)[][], color: Color): Square | null {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const piece = board[row][col];
            if (piece && piece.type === PieceType.KING && piece.color === color) {
                return [row, col];
            }
        }
    }
    return null;
}

/** Create the initial game state */
export function createInitialState(): GameState {
    return {
        board: createInitialBoard(),
        currentTurn: Color.WHITE,
        phase: GamePhase.ROLL_DICE,
        diceResult: null,
        castlingRights: {
            whiteKingside: true,
            whiteQueenside: true,
            blackKingside: true,
            blackQueenside: true,
        },
        enPassantTarget: null,
        moveHistory: [],
        capturedPieces: { white: [], black: [] },
        isCheck: false,
        winner: null,
        halfMoveClock: 0,
        fullMoveNumber: 1,
        highlightedPieces: [],
        validMoves: [],
        selectedSquare: null,
        lastMove: null,
    };
}

/** Get the opposite color */
export function oppositeColor(color: Color): Color {
    return color === Color.WHITE ? Color.BLACK : Color.WHITE;
}

/** Compare two squares for equality */
export function squaresEqual(a: Square, b: Square): boolean {
    return a[0] === b[0] && a[1] === b[1];
}

/** Clone the full castling rights */
export function cloneCastlingRights(rights: CastlingRights): CastlingRights {
    return { ...rights };
}
