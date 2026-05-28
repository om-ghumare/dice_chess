'use client';

import React from 'react';
import { PieceType, Color, GameState, GamePhase } from '@/engine/types';
import { PieceIcon } from './Piece';

interface GameHUDProps {
    state: GameState;
}

const PIECE_ORDER: PieceType[] = [
    PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP,
    PieceType.KNIGHT, PieceType.PAWN,
];

const PIECE_VALUES: Record<PieceType, number> = {
    [PieceType.PAWN]: 1,
    [PieceType.KNIGHT]: 3,
    [PieceType.BISHOP]: 3,
    [PieceType.ROOK]: 5,
    [PieceType.QUEEN]: 9,
    [PieceType.KING]: 0,
};

function sortCaptured(pieces: PieceType[]): PieceType[] {
    return [...pieces].sort((a, b) => PIECE_VALUES[b] - PIECE_VALUES[a]);
}

function getMaterialAdvantage(captured: { white: PieceType[]; black: PieceType[] }): number {
    const whiteValue = captured.white.reduce((sum, p) => sum + PIECE_VALUES[p], 0);
    const blackValue = captured.black.reduce((sum, p) => sum + PIECE_VALUES[p], 0);
    return whiteValue - blackValue; // positive = white captured more (white is ahead)
}

export default function GameHUD({ state }: GameHUDProps) {
    const { currentTurn, capturedPieces, isCheck, phase } = state;
    const advantage = getMaterialAdvantage(capturedPieces);

    return (
        <div className="game-hud" id="game-hud">
            {/* Turn Indicator */}
            <div className="turn-indicator">
                <div className={`turn-dot ${currentTurn}`} />
                <span>
                    {phase === GamePhase.GAME_OVER
                        ? 'Game Over'
                        : `${currentTurn === Color.WHITE ? 'White' : 'Black'}'s Turn`}
                </span>
            </div>

            {/* Check Warning */}
            {isCheck && phase !== GamePhase.GAME_OVER && (
                <div className="status-banner check">⚠️ Check!</div>
            )}

            {/* Phase indicator */}
            {phase === GamePhase.ROLL_DICE && (
                <div className="status-banner info">Roll the dice to begin</div>
            )}
            {phase === GamePhase.SELECT_PIECE && state.diceResult && (
                <div className="status-banner info">
                    Select a {state.diceResult} to move
                </div>
            )}

            {/* Black's captured pieces (pieces white captured FROM black) */}
            <div className="captured-section">
                <div className="captured-label">
                    Black&apos;s Captured
                    {advantage > 0 && <span style={{ color: '#10b981', marginLeft: 8 }}>+{advantage}</span>}
                </div>
                <div className="captured-pieces">
                    {sortCaptured(capturedPieces.white).map((piece, i) => (
                        <PieceIcon key={`bw-${i}`} type={piece} color={Color.BLACK} size={22} />
                    ))}
                </div>
            </div>

            {/* White's captured pieces (pieces black captured FROM white) */}
            <div className="captured-section">
                <div className="captured-label">
                    White&apos;s Captured
                    {advantage < 0 && <span style={{ color: '#10b981', marginLeft: 8 }}>+{Math.abs(advantage)}</span>}
                </div>
                <div className="captured-pieces">
                    {sortCaptured(capturedPieces.black).map((piece, i) => (
                        <PieceIcon key={`bk-${i}`} type={piece} color={Color.WHITE} size={22} />
                    ))}
                </div>
            </div>

            {/* Move count */}
            <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', textAlign: 'center' }}>
                Move {state.fullMoveNumber}
            </div>
        </div>
    );
}
