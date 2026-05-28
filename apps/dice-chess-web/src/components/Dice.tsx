'use client';

import React, { useState, useCallback } from 'react';
import { PieceType, Color } from '@/engine/types';
import { PieceIcon } from './Piece';

interface DiceProps {
    currentTurn: Color;
    diceResult: PieceType | null;
    canRoll: boolean;
    onRoll: () => void;
}

const PIECE_NAMES: Record<PieceType, string> = {
    [PieceType.PAWN]: 'Pawn',
    [PieceType.KNIGHT]: 'Knight',
    [PieceType.BISHOP]: 'Bishop',
    [PieceType.ROOK]: 'Rook',
    [PieceType.QUEEN]: 'Queen',
    [PieceType.KING]: 'King',
};

const ALL_TYPES: PieceType[] = [
    PieceType.PAWN, PieceType.KNIGHT, PieceType.BISHOP,
    PieceType.ROOK, PieceType.QUEEN, PieceType.KING,
];

export default function Dice({ currentTurn, diceResult, canRoll, onRoll }: DiceProps) {
    const [isRolling, setIsRolling] = useState(false);
    const [animType, setAnimType] = useState<PieceType>(PieceType.PAWN);

    const handleRoll = useCallback(() => {
        if (!canRoll || isRolling) return;
        setIsRolling(true);

        // Animate through random faces
        let count = 0;
        const interval = setInterval(() => {
            setAnimType(ALL_TYPES[Math.floor(Math.random() * ALL_TYPES.length)]);
            count++;
            if (count > 10) {
                clearInterval(interval);
                setIsRolling(false);
                onRoll();
            }
        }, 80);
    }, [canRoll, isRolling, onRoll]);

    const displayType = isRolling ? animType : diceResult;

    return (
        <div className="dice-container" id="dice-component">
            <div className={`dice-face ${isRolling ? 'rolling' : ''}`}>
                {displayType ? (
                    <PieceIcon type={displayType} color={currentTurn} size={70} />
                ) : (
                    <span style={{ fontSize: '2rem', opacity: 0.3 }}>🎲</span>
                )}
            </div>

            {diceResult && !isRolling && (
                <div className="dice-label">{PIECE_NAMES[diceResult]}</div>
            )}

            {canRoll && (
                <button
                    className="roll-button"
                    onClick={handleRoll}
                    disabled={isRolling}
                    id="roll-dice-btn"
                >
                    {isRolling ? 'Rolling...' : '🎲 Roll Dice'}
                </button>
            )}
        </div>
    );
}
