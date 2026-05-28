// ============================================================
// Dice Chess — Game State Machine
// ============================================================

import { GameState, GamePhase, PieceType, Color, Square, Move } from './types';
import { createInitialState, cloneBoard, getPieceAt, setPieceAt, oppositeColor, findKing, squaresEqual, cloneCastlingRights } from './board';
import { rollDice, getHighlightedPieces } from './dice';
import { getLegalMovesForSquare, applyMoveToBoard } from './moves';
import { isInCheck, isCheckmate, isStalemate } from './validation';

export class GameManager {
    private state: GameState;

    constructor() {
        this.state = createInitialState();
    }

    getState(): GameState {
        return this.state;
    }

    /** Reset to initial state */
    reset(): GameState {
        this.state = createInitialState();
        return this.state;
    }

    /** Load a specific state (for multiplayer sync) */
    loadState(state: GameState): void {
        this.state = state;
    }

    /** Roll the dice for the current player */
    handleRollDice(): GameState {
        if (this.state.phase !== GamePhase.ROLL_DICE) return this.state;

        const result = rollDice(this.state, this.state.currentTurn);

        if (result === null) {
            // No moves available — check for checkmate or stalemate
            if (isInCheck(this.state.board, this.state.currentTurn)) {
                this.state.winner = oppositeColor(this.state.currentTurn);
            } else {
                this.state.winner = 'draw';
            }
            this.state.phase = GamePhase.GAME_OVER;
            return this.state;
        }

        this.state.diceResult = result;
        this.state.phase = GamePhase.SELECT_PIECE;
        this.state.highlightedPieces = getHighlightedPieces(this.state, this.state.currentTurn, result);
        this.state.selectedSquare = null;
        this.state.validMoves = [];

        return this.state;
    }

    /** Select a piece to move (must match dice result) */
    handleSelectPiece(square: Square): GameState {
        if (this.state.phase !== GamePhase.SELECT_PIECE) return this.state;

        const piece = getPieceAt(this.state.board, square);
        if (!piece) return this.state;
        if (piece.color !== this.state.currentTurn) return this.state;
        if (piece.type !== this.state.diceResult) return this.state;

        // Check if this piece is in the highlighted list
        const isHighlighted = this.state.highlightedPieces.some(s => squaresEqual(s, square));
        if (!isHighlighted) return this.state;

        // Get valid moves for this piece
        const moves = getLegalMovesForSquare(this.state, square);
        this.state.selectedSquare = square;
        this.state.validMoves = moves.map(m => m.to);

        return this.state;
    }

    /** Attempt a move to the target square */
    handleMove(targetSquare: Square): GameState {
        if (!this.state.selectedSquare) return this.state;

        const legalMoves = getLegalMovesForSquare(this.state, this.state.selectedSquare);
        const move = legalMoves.find(m => squaresEqual(m.to, targetSquare));

        if (!move) {
            // If clicking on another highlighted piece, select that instead
            const piece = getPieceAt(this.state.board, targetSquare);
            if (piece && piece.color === this.state.currentTurn && piece.type === this.state.diceResult) {
                return this.handleSelectPiece(targetSquare);
            }
            return this.state;
        }

        // Check if this is a promotion move (need to show promotion dialog)
        if (move.piece === PieceType.PAWN && move.promotion) {
            // Default to queen promotion — the UI should call handlePromotion for other choices
            return this.executeMove({ ...move, promotion: PieceType.QUEEN });
        }

        return this.executeMove(move);
    }

    /** Execute a promotion with a specific piece type */
    handlePromotion(from: Square, to: Square, promotionType: PieceType): GameState {
        const move: Move = {
            from,
            to,
            piece: PieceType.PAWN,
            promotion: promotionType,
            captured: getPieceAt(this.state.board, to)?.type,
        };

        return this.executeMove(move);
    }

    /** Execute a validated move */
    private executeMove(move: Move): GameState {
        const piece = getPieceAt(this.state.board, move.from)!;

        // Track captures
        if (move.captured) {
            if (this.state.currentTurn === Color.WHITE) {
                this.state.capturedPieces.white.push(move.captured);
            } else {
                this.state.capturedPieces.black.push(move.captured);
            }
        }

        // En passant capture
        if (move.enPassant) {
            const capturedPawnRow = move.from[0];
            setPieceAt(this.state.board, [capturedPawnRow, move.to[1]], null);
            if (this.state.currentTurn === Color.WHITE) {
                this.state.capturedPieces.white.push(PieceType.PAWN);
            } else {
                this.state.capturedPieces.black.push(PieceType.PAWN);
            }
        }

        // Move the piece
        setPieceAt(this.state.board, move.from, null);

        if (move.promotion) {
            setPieceAt(this.state.board, move.to, { type: move.promotion, color: piece.color });
        } else {
            setPieceAt(this.state.board, move.to, piece);
        }

        // Handle castling rook movement
        if (move.castling) {
            const row = move.from[0];
            if (move.castling === 'kingside') {
                const rook = getPieceAt(this.state.board, [row, 7]);
                setPieceAt(this.state.board, [row, 7], null);
                setPieceAt(this.state.board, [row, 5], rook);
            } else {
                const rook = getPieceAt(this.state.board, [row, 0]);
                setPieceAt(this.state.board, [row, 0], null);
                setPieceAt(this.state.board, [row, 3], rook);
            }
        }

        // Update castling rights
        this.updateCastlingRights(move);

        // Update en passant target
        if (move.piece === PieceType.PAWN && Math.abs(move.to[0] - move.from[0]) === 2) {
            const epRow = (move.from[0] + move.to[0]) / 2;
            this.state.enPassantTarget = [epRow, move.from[1]];
        } else {
            this.state.enPassantTarget = null;
        }

        // Record move
        this.state.moveHistory.push(move);
        this.state.lastMove = move;

        // Switch turn
        this.state.currentTurn = oppositeColor(this.state.currentTurn);

        // Update check status
        this.state.isCheck = isInCheck(this.state.board, this.state.currentTurn);

        // Check for game end
        if (isCheckmate(this.state, this.state.currentTurn)) {
            this.state.winner = oppositeColor(this.state.currentTurn);
            this.state.phase = GamePhase.GAME_OVER;
        } else if (isStalemate(this.state, this.state.currentTurn)) {
            this.state.winner = 'draw';
            this.state.phase = GamePhase.GAME_OVER;
        } else {
            this.state.phase = GamePhase.ROLL_DICE;
        }

        // Clear selection
        this.state.diceResult = null;
        this.state.selectedSquare = null;
        this.state.validMoves = [];
        this.state.highlightedPieces = [];

        // Update move count
        if (this.state.currentTurn === Color.WHITE) {
            this.state.fullMoveNumber++;
        }

        return this.state;
    }

    private updateCastlingRights(move: Move): void {
        // King moved — lose both castling rights
        if (move.piece === PieceType.KING) {
            if (move.from[0] === 7) {
                this.state.castlingRights.whiteKingside = false;
                this.state.castlingRights.whiteQueenside = false;
            } else if (move.from[0] === 0) {
                this.state.castlingRights.blackKingside = false;
                this.state.castlingRights.blackQueenside = false;
            }
        }

        // Rook moved — lose that side's castling right
        if (move.piece === PieceType.ROOK) {
            if (squaresEqual(move.from, [7, 7])) this.state.castlingRights.whiteKingside = false;
            if (squaresEqual(move.from, [7, 0])) this.state.castlingRights.whiteQueenside = false;
            if (squaresEqual(move.from, [0, 7])) this.state.castlingRights.blackKingside = false;
            if (squaresEqual(move.from, [0, 0])) this.state.castlingRights.blackQueenside = false;
        }

        // Rook captured — lose that side's castling right
        if (move.captured === PieceType.ROOK) {
            if (squaresEqual(move.to, [7, 7])) this.state.castlingRights.whiteKingside = false;
            if (squaresEqual(move.to, [7, 0])) this.state.castlingRights.whiteQueenside = false;
            if (squaresEqual(move.to, [0, 7])) this.state.castlingRights.blackKingside = false;
            if (squaresEqual(move.to, [0, 0])) this.state.castlingRights.blackQueenside = false;
        }
    }
}
