// ============================================================
// Dice Chess — Type Definitions
// ============================================================

export enum PieceType {
  PAWN = 'pawn',
  KNIGHT = 'knight',
  BISHOP = 'bishop',
  ROOK = 'rook',
  QUEEN = 'queen',
  KING = 'king',
}

export enum Color {
  WHITE = 'white',
  BLACK = 'black',
}

export interface Piece {
  type: PieceType;
  color: Color;
}

/** Board position: [row, col] where row 0 = top (black's back rank), col 0 = left */
export type Square = [number, number];

export interface Move {
  from: Square;
  to: Square;
  piece: PieceType;
  captured?: PieceType;
  promotion?: PieceType;
  castling?: 'kingside' | 'queenside';
  enPassant?: boolean;
}

export enum GamePhase {
  ROLL_DICE = 'roll_dice',
  SELECT_PIECE = 'select_piece',
  GAME_OVER = 'game_over',
}

export interface CastlingRights {
  whiteKingside: boolean;
  whiteQueenside: boolean;
  blackKingside: boolean;
  blackQueenside: boolean;
}

export interface GameState {
  board: (Piece | null)[][];
  currentTurn: Color;
  phase: GamePhase;
  diceResult: PieceType | null;
  castlingRights: CastlingRights;
  enPassantTarget: Square | null;
  moveHistory: Move[];
  capturedPieces: { white: PieceType[]; black: PieceType[] };
  isCheck: boolean;
  winner: Color | 'draw' | null;
  halfMoveClock: number;
  fullMoveNumber: number;
  /** Squares of pieces that can be moved (after dice roll) */
  highlightedPieces: Square[];
  /** Valid destination squares for the currently selected piece */
  validMoves: Square[];
  /** Currently selected piece square */
  selectedSquare: Square | null;
  /** Last move for highlighting */
  lastMove: Move | null;
}

export type GameMode = 'local' | 'ai' | 'online';

export type AIDifficulty = 'easy' | 'medium' | 'hard';
