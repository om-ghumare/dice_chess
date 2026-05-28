'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import Link from 'next/link';
import { GameState, GamePhase, PieceType, Color, Square, AIDifficulty, Move } from '@/engine/types';
import { GameManager } from '@/engine/game';
import { getPieceAt, squaresEqual } from '@/engine/board';
import { getLegalMovesForSquare } from '@/engine/moves';
import { rollDice, getHighlightedPieces } from '@/engine/dice';
import { getBestAIMove } from '@/engine/ai';
import {
    playMoveSound, playCaptureSound, playCheckSound,
    playCheckmateSound, playDiceRollSound, playSelectSound, playDrawSound
} from '@/engine/sounds';
import Board from '@/components/Board';
import Dice from '@/components/Dice';
import GameHUD from '@/components/GameHUD';
import PromotionModal from '@/components/PromotionModal';
import GameOverModal from '@/components/GameOverModal';

export default function AIPlayPage() {
    const gameRef = useRef(new GameManager());
    const [state, setState] = useState<GameState>(gameRef.current.getState());
    const [promotionPending, setPromotionPending] = useState<{ from: Square; to: Square } | null>(null);
    const [difficulty, setDifficulty] = useState<AIDifficulty>('medium');
    const aiThinkingRef = useRef(false);
    const [aiThinking, setAiThinking] = useState(false);

    // AI plays black
    const AI_COLOR = Color.BLACK;

    // AI turn handler
    useEffect(() => {
        const currentState = gameRef.current.getState();
        if (currentState.currentTurn === AI_COLOR && currentState.phase === GamePhase.ROLL_DICE && !aiThinkingRef.current) {
            aiThinkingRef.current = true;
            setAiThinking(true);

            const timer1 = setTimeout(() => {
                const freshState = gameRef.current.getState();
                // Double-check it's still AI's turn to roll
                if (freshState.currentTurn !== AI_COLOR || freshState.phase !== GamePhase.ROLL_DICE) {
                    aiThinkingRef.current = false;
                    setAiThinking(false);
                    return;
                }

                const rolledState = gameRef.current.handleRollDice();
                playDiceRollSound();
                setState({ ...rolledState });

                const timer2 = setTimeout(() => {
                    const prevState = gameRef.current.getState();
                    if (prevState.diceResult) {
                        const bestMove = getBestAIMove(prevState, AI_COLOR, prevState.diceResult, difficulty);
                        if (bestMove) {
                            gameRef.current.handleSelectPiece(bestMove.from);

                            let newState: GameState;
                            if (bestMove.promotion) {
                                newState = gameRef.current.handlePromotion(bestMove.from, bestMove.to, bestMove.promotion);
                            } else {
                                newState = gameRef.current.handleMove(bestMove.to);
                            }

                            // Play appropriate sound
                            if (newState.phase === GamePhase.GAME_OVER) {
                                newState.winner === 'draw' ? playDrawSound() : playCheckmateSound();
                            } else if (newState.isCheck) {
                                playCheckSound();
                            } else if (
                                newState.capturedPieces.white.length > prevState.capturedPieces.white.length ||
                                newState.capturedPieces.black.length > prevState.capturedPieces.black.length
                            ) {
                                playCaptureSound();
                            } else {
                                playMoveSound();
                            }

                            setState({ ...newState });
                        }
                    }
                    aiThinkingRef.current = false;
                    setAiThinking(false);
                }, 600);

                return () => clearTimeout(timer2);
            }, 800);

            return () => {
                clearTimeout(timer1);
            };
        }
    }, [state, difficulty]);

    const handleRollDice = useCallback(() => {
        const newState = gameRef.current.handleRollDice();
        playDiceRollSound();
        setState({ ...newState });
    }, []);

    const handleSquareClick = useCallback((square: Square) => {
        const currentState = gameRef.current.getState();

        // Don't allow interaction during AI's turn
        if (currentState.currentTurn === AI_COLOR) return;
        if (currentState.phase === GamePhase.GAME_OVER) return;
        if (currentState.phase === GamePhase.ROLL_DICE) return;

        if (!currentState.selectedSquare) {
            const newState = gameRef.current.handleSelectPiece(square);
            if (newState.selectedSquare) playSelectSound();
            setState({ ...newState });
            return;
        }

        // Check if clicking another valid piece
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

        // Check promotion
        const legalMoves = getLegalMovesForSquare(currentState, currentState.selectedSquare);
        const promoMoves = legalMoves.filter(m => squaresEqual(m.to, square) && m.promotion);

        if (promoMoves.length > 0) {
            setPromotionPending({ from: currentState.selectedSquare, to: square });
            return;
        }

        const prevState = { ...currentState };
        const newState = gameRef.current.handleMove(square);
        if (newState.moveHistory.length > currentState.moveHistory.length) {
            if (newState.phase === GamePhase.GAME_OVER) {
                newState.winner === 'draw' ? playDrawSound() : playCheckmateSound();
            } else if (newState.isCheck) {
                playCheckSound();
            } else if (
                newState.capturedPieces.white.length > currentState.capturedPieces.white.length ||
                newState.capturedPieces.black.length > currentState.capturedPieces.black.length
            ) {
                playCaptureSound();
            } else {
                playMoveSound();
            }
        }
        setState({ ...newState });
    }, []);

    const handlePromotion = useCallback((from: Square, to: Square, pieceType: PieceType) => {
        const currentState = gameRef.current.getState();
        const newState = gameRef.current.handlePromotion(from, to, pieceType);
        setPromotionPending(null);
        if (newState.phase === GamePhase.GAME_OVER) {
            newState.winner === 'draw' ? playDrawSound() : playCheckmateSound();
        } else if (newState.isCheck) {
            playCheckSound();
        } else {
            playMoveSound();
        }
        setState({ ...newState });
    }, []);

    const reset = useCallback(() => {
        const newState = gameRef.current.reset();
        setPromotionPending(null);
        setAiThinking(false);
        setState({ ...newState });
    }, []);

    const canRoll = state.phase === GamePhase.ROLL_DICE && state.currentTurn !== AI_COLOR;

    return (
        <div className="game-layout" id="ai-game">
            <Link href="/" className="back-button" id="back-btn">← Back</Link>

            <div className="game-sidebar">
                <div className="difficulty-selector">
                    {(['easy', 'medium', 'hard'] as AIDifficulty[]).map((d) => (
                        <button
                            key={d}
                            className={`difficulty-btn ${difficulty === d ? 'active' : ''}`}
                            onClick={() => setDifficulty(d)}
                            id={`difficulty-${d}`}
                        >
                            {d.charAt(0).toUpperCase() + d.slice(1)}
                        </button>
                    ))}
                </div>

                <GameHUD state={state} />

                {aiThinking && (
                    <div className="status-banner info">🤖 AI is thinking...</div>
                )}

                <Dice
                    currentTurn={state.currentTurn}
                    diceResult={state.diceResult}
                    canRoll={canRoll}
                    onRoll={handleRollDice}
                />
            </div>

            <Board state={state} onSquareClick={handleSquareClick} />

            {promotionPending && (
                <PromotionModal
                    color={state.currentTurn}
                    from={promotionPending.from}
                    to={promotionPending.to}
                    onSelect={handlePromotion}
                />
            )}

            {state.phase === GamePhase.GAME_OVER && (
                <GameOverModal
                    winner={state.winner}
                    onRematch={reset}
                    onExit={() => window.location.href = '/'}
                />
            )}
        </div>
    );
}
