'use client';

import React from 'react';
import Link from 'next/link';
import { GamePhase } from '@/engine/types';
import { useGame } from '@/hooks/useGame';
import Board from '@/components/Board';
import Dice from '@/components/Dice';
import GameHUD from '@/components/GameHUD';
import PromotionModal from '@/components/PromotionModal';
import GameOverModal from '@/components/GameOverModal';

export default function LocalPlayPage() {
    const { state, rollDice, handleSquareClick, handlePromotion, reset, promotionPending } = useGame();

    return (
        <div className="game-layout" id="local-game">
            <Link href="/" className="back-button" id="back-btn">← Back</Link>

            <div className="game-sidebar">
                <GameHUD state={state} />
                <Dice
                    currentTurn={state.currentTurn}
                    diceResult={state.diceResult}
                    canRoll={state.phase === GamePhase.ROLL_DICE}
                    onRoll={rollDice}
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
