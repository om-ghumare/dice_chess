'use client';

import React from 'react';
import { PieceType, Color, Square, GameState } from '@/engine/types';
import { getPieceAt, squaresEqual } from '@/engine/board';
import PieceSVG from './Piece';

interface BoardProps {
    state: GameState;
    onSquareClick: (square: Square) => void;
    flipped?: boolean;
}

export default function Board({ state, onSquareClick, flipped = false }: BoardProps) {
    const { board, selectedSquare, validMoves, highlightedPieces, lastMove, isCheck } = state;

    const rows = flipped ? [7, 6, 5, 4, 3, 2, 1, 0] : [0, 1, 2, 3, 4, 5, 6, 7];
    const cols = flipped ? [7, 6, 5, 4, 3, 2, 1, 0] : [0, 1, 2, 3, 4, 5, 6, 7];

    const isKingInCheck = (row: number, col: number): boolean => {
        if (!isCheck) return false;
        const piece = board[row][col];
        return piece !== null && piece.type === PieceType.KING && piece.color === state.currentTurn;
    };

    return (
        <div className="chess-board" id="chess-board">
            {rows.map((row) =>
                cols.map((col) => {
                    const square: Square = [row, col];
                    const piece = board[row][col];
                    const isLight = (row + col) % 2 === 0;
                    const isSelected = selectedSquare && squaresEqual(square, selectedSquare);
                    const isValidMove = validMoves.some(m => squaresEqual(m, square));
                    const isHighlighted = highlightedPieces.some(s => squaresEqual(s, square));
                    const isLastMoveSquare = lastMove && (squaresEqual(square, lastMove.from) || squaresEqual(square, lastMove.to));
                    const isCheckSquare = isKingInCheck(row, col);
                    const isCapture = isValidMove && piece !== null;

                    const classes = [
                        'chess-square',
                        isLight ? 'light' : 'dark',
                        isSelected ? 'selected' : '',
                        isHighlighted ? 'highlighted' : '',
                        isLastMoveSquare ? 'last-move' : '',
                        isCheckSquare ? 'in-check' : '',
                    ].filter(Boolean).join(' ');

                    return (
                        <div
                            key={`${row}-${col}`}
                            className={classes}
                            onClick={() => onSquareClick(square)}
                            id={`square-${row}-${col}`}
                        >
                            {piece && (
                                <PieceSVG type={piece.type} color={piece.color} />
                            )}
                            {isValidMove && !isCapture && (
                                <div className="valid-move-dot" />
                            )}
                            {isValidMove && isCapture && (
                                <div className="valid-move-capture" />
                            )}
                        </div>
                    );
                })
            )}
        </div>
    );
}
