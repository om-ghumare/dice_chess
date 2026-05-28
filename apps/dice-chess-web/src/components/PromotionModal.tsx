'use client';

import React from 'react';
import { PieceType, Color, Square } from '@/engine/types';
import PieceSVG from './Piece';

interface PromotionModalProps {
    color: Color;
    from: Square;
    to: Square;
    onSelect: (from: Square, to: Square, pieceType: PieceType) => void;
}

const PROMOTION_PIECES: PieceType[] = [
    PieceType.QUEEN,
    PieceType.ROOK,
    PieceType.BISHOP,
    PieceType.KNIGHT,
];

export default function PromotionModal({ color, from, to, onSelect }: PromotionModalProps) {
    return (
        <div className="modal-overlay" id="promotion-modal">
            <div className="modal-content">
                <div className="modal-title">Promote Pawn</div>
                <div className="modal-subtitle">Choose your new piece</div>
                <div className="promotion-options">
                    {PROMOTION_PIECES.map((type) => (
                        <button
                            key={type}
                            className="promotion-option"
                            onClick={() => onSelect(from, to, type)}
                            id={`promote-${type}`}
                        >
                            <PieceSVG type={type} color={color} size={50} />
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
