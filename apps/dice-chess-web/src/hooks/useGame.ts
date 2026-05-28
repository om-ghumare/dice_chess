'use client';

import { useState, useCallback, useRef } from 'react';
import { GameState, GamePhase, PieceType, Color, Square, Move, AIDifficulty } from '@/engine/types';
import { GameManager } from '@/engine/game';
import { getPieceAt, squaresEqual } from '@/engine/board';
import { getLegalMovesForSquare } from '@/engine/moves';
import {
    playMoveSound, playCaptureSound, playCheckSound,
    playCheckmateSound, playDiceRollSound, playSelectSound, playDrawSound
} from '@/engine/sounds';

interface UseGameReturn {
    state: GameState;
    rollDice: () => void;
    handleSquareClick: (square: Square) => void;
    handlePromotion: (from: Square, to: Square, pieceType: PieceType) => void;
    reset: () => void;
    promotionPending: { from: Square; to: Square } | null;
}

export function useGame(): UseGameReturn {
    const gameRef = useRef(new GameManager());
    const [state, setState] = useState<GameState>(gameRef.current.getState());
    const [promotionPending, setPromotionPending] = useState<{ from: Square; to: Square } | null>(null);

    const rollDice = useCallback(() => {
        const newState = gameRef.current.handleRollDice();
        playDiceRollSound();
        setState({ ...newState });
    }, []);

    const playMoveResultSounds = useCallback((prevState: GameState, newState: GameState) => {
        // Check game over first
        if (newState.phase === GamePhase.GAME_OVER) {
            if (newState.winner === 'draw') {
                playDrawSound();
            } else {
                playCheckmateSound();
            }
            return;
        }

        // Check
        if (newState.isCheck) {
            playCheckSound();
            return;
        }

        // Capture (compare captured pieces count)
        const prevWhiteCaptures = prevState.capturedPieces.white.length;
        const prevBlackCaptures = prevState.capturedPieces.black.length;
        const newWhiteCaptures = newState.capturedPieces.white.length;
        const newBlackCaptures = newState.capturedPieces.black.length;

        if (newWhiteCaptures > prevWhiteCaptures || newBlackCaptures > prevBlackCaptures) {
            playCaptureSound();
            return;
        }

        // Normal move
        playMoveSound();
    }, []);

    const handleSquareClick = useCallback((square: Square) => {
        const currentState = gameRef.current.getState();

        if (currentState.phase === GamePhase.GAME_OVER) return;
        if (currentState.phase === GamePhase.ROLL_DICE) return;

        // If no piece is selected yet, try to select one
        if (!currentState.selectedSquare) {
            const newState = gameRef.current.handleSelectPiece(square);
            if (newState.selectedSquare) playSelectSound();
            setState({ ...newState });
            return;
        }

        // Check if clicking on another valid piece to select
        const piece = getPieceAt(currentState.board, square);
        if (piece && piece.color === currentState.currentTurn && piece.type === currentState.diceResult) {
            const isHighlighted = currentState.highlightedPieces.some(s => squaresEqual(s, square));
            if (isHighlighted && !squaresEqual(square, currentState.selectedSquare)) {
                const newState = gameRef.current.handleSelectPiece(square);
                playSelectSound();
                setState({ ...newState });
                return;
            }
        }

        // Check if this is a promotion move
        const legalMoves = getLegalMovesForSquare(currentState, currentState.selectedSquare);
        const promoMoves = legalMoves.filter(m => squaresEqual(m.to, square) && m.promotion);

        if (promoMoves.length > 0) {
            setPromotionPending({ from: currentState.selectedSquare, to: square });
            return;
        }

        // Try to move
        const newState = gameRef.current.handleMove(square);
        if (newState.moveHistory.length > currentState.moveHistory.length) {
            playMoveResultSounds(currentState, newState);
        }
        setState({ ...newState });
    }, [playMoveResultSounds]);

    const handlePromotion = useCallback((from: Square, to: Square, pieceType: PieceType) => {
        const currentState = gameRef.current.getState();
        const newState = gameRef.current.handlePromotion(from, to, pieceType);
        setPromotionPending(null);
        playMoveResultSounds(currentState, newState);
        setState({ ...newState });
    }, [playMoveResultSounds]);

    const reset = useCallback(() => {
        const newState = gameRef.current.reset();
        setPromotionPending(null);
        setState({ ...newState });
    }, []);

    return { state, rollDice, handleSquareClick, handlePromotion, reset, promotionPending };
}
