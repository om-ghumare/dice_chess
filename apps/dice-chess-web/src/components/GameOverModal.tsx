'use client';

import React from 'react';
import { Color } from '@/engine/types';

interface GameOverModalProps {
    winner: Color | 'draw' | null;
    onRematch: () => void;
    onExit: () => void;
}

export default function GameOverModal({ winner, onRematch, onExit }: GameOverModalProps) {
    const title = winner === 'draw'
        ? 'Draw!'
        : winner === Color.WHITE
            ? 'White Wins!'
            : 'Black Wins!';

    const subtitle = winner === 'draw'
        ? 'The game ended in a stalemate.'
        : `${winner === Color.WHITE ? 'White' : 'Black'} delivered checkmate!`;

    return (
        <div className="modal-overlay" id="game-over-modal">
            <div className="modal-content">
                <div style={{ fontSize: '3rem', marginBottom: 12 }}>
                    {winner === 'draw' ? '🤝' : '👑'}
                </div>
                <div className="modal-title">{title}</div>
                <div className="modal-subtitle">{subtitle}</div>
                <div className="modal-buttons">
                    <button className="btn-primary" onClick={onRematch} id="rematch-btn">
                        🔄 Rematch
                    </button>
                    <button className="btn-secondary" onClick={onExit} id="exit-btn">
                        ← Exit
                    </button>
                </div>
            </div>
        </div>
    );
}
