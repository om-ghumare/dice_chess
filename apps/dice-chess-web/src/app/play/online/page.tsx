'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import Link from 'next/link';
import { io, Socket } from 'socket.io-client';
import { GameState, GamePhase, PieceType, Color, Square } from '@/engine/types';
import { GameManager } from '@/engine/game';
import { getPieceAt, squaresEqual } from '@/engine/board';
import { getLegalMovesForSquare } from '@/engine/moves';
import {
    playMoveSound, playCaptureSound, playCheckSound,
    playCheckmateSound, playDiceRollSound, playSelectSound, playDrawSound
} from '@/engine/sounds';
import Board from '@/components/Board';
import Dice from '@/components/Dice';
import GameHUD from '@/components/GameHUD';
import PromotionModal from '@/components/PromotionModal';
import GameOverModal from '@/components/GameOverModal';

type ConnectionStatus = 'lobby' | 'connecting' | 'waiting' | 'playing' | 'disconnected';

export default function OnlinePlayPage() {
    const socketRef = useRef<Socket | null>(null);
    const gameRef = useRef(new GameManager());
    const roomCodeRef = useRef('');
    const myColorRef = useRef<Color | null>(null);

    const [state, setState] = useState<GameState>(gameRef.current.getState());
    const [promotionPending, setPromotionPending] = useState<{ from: Square; to: Square } | null>(null);
    const [inputCode, setInputCode] = useState('');
    const [status, setStatus] = useState<ConnectionStatus>('lobby');
    const [displayRoomCode, setDisplayRoomCode] = useState('');
    const [displayColor, setDisplayColor] = useState<Color | null>(null);
    const [error, setError] = useState('');

    // Helper: broadcast state to opponent after any action
    const syncToOpponent = useCallback((newState: GameState, eventType: string) => {
        const code = roomCodeRef.current;
        if (code && socketRef.current) {
            socketRef.current.emit('sync-state', code, { state: newState, eventType });
        }
    }, []);

    // Connect to WebSocket server
    const connectSocket = useCallback(() => {
        if (socketRef.current?.connected) return socketRef.current;

        const socket = io('http://localhost:3001', {
            transports: ['websocket', 'polling'],
        });

        socket.on('connect', () => {
            console.log('Connected to game server');
            setError('');
        });

        socket.on('connect_error', () => {
            setError('Cannot connect to game server. Make sure the server is running on port 3001.');
            setStatus('lobby');
        });

        socket.on('game-ready', () => {
            setStatus('playing');
            const newState = gameRef.current.reset();
            setState({ ...newState });
        });

        // Receive full state from opponent
        socket.on('state-synced', (data: { state: GameState; eventType: string }) => {
            const prevState = gameRef.current.getState();
            gameRef.current.loadState(data.state);
            setState({ ...data.state });

            // Play appropriate sound based on event type
            if (data.eventType === 'roll') {
                playDiceRollSound();
            } else if (data.eventType === 'move') {
                if (data.state.phase === GamePhase.GAME_OVER) {
                    data.state.winner === 'draw' ? playDrawSound() : playCheckmateSound();
                } else if (data.state.isCheck) {
                    playCheckSound();
                } else if (
                    data.state.capturedPieces.white.length > prevState.capturedPieces.white.length ||
                    data.state.capturedPieces.black.length > prevState.capturedPieces.black.length
                ) {
                    playCaptureSound();
                } else {
                    playMoveSound();
                }
            }
        });

        socket.on('opponent-disconnected', () => {
            setStatus('disconnected');
        });

        socket.on('rematch-requested', () => {
            socket.emit('rematch-accept', roomCodeRef.current);
        });

        socket.on('rematch-accepted', () => {
            const newState = gameRef.current.reset();
            setState({ ...newState });
            setStatus('playing');
        });

        socketRef.current = socket;
        return socket;
    }, []);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            socketRef.current?.disconnect();
        };
    }, []);

    const handleCreateRoom = useCallback(() => {
        setStatus('connecting');
        const socket = connectSocket();
        socket.emit('create-room', (response: any) => {
            if (response.success) {
                roomCodeRef.current = response.roomCode;
                myColorRef.current = Color.WHITE;
                setDisplayRoomCode(response.roomCode);
                setDisplayColor(Color.WHITE);
                setStatus('waiting');
            } else {
                setError('Failed to create room');
                setStatus('lobby');
            }
        });
    }, [connectSocket]);

    const handleJoinRoom = useCallback(() => {
        if (inputCode.length < 4) return;
        setStatus('connecting');
        const socket = connectSocket();
        socket.emit('join-room', inputCode, (response: any) => {
            if (response.success) {
                const color = response.color === 'white' ? Color.WHITE : Color.BLACK;
                roomCodeRef.current = response.roomCode;
                myColorRef.current = color;
                setDisplayRoomCode(response.roomCode);
                setDisplayColor(color);
                if (response.color === 'spectator') {
                    setStatus('playing');
                } else {
                    setStatus('waiting');
                }
            } else {
                setError(response.error || 'Failed to join room');
                setStatus('lobby');
            }
        });
    }, [inputCode, connectSocket]);

    // Game interaction handlers
    const isMyTurn = displayColor !== null && state.currentTurn === displayColor;

    const handleRollDice = useCallback(() => {
        const gs = gameRef.current.getState();
        if (myColorRef.current === null || gs.currentTurn !== myColorRef.current) return;
        if (gs.phase !== GamePhase.ROLL_DICE) return;
        const newState = gameRef.current.handleRollDice();
        playDiceRollSound();
        setState({ ...newState });
        syncToOpponent(newState, 'roll');
    }, [syncToOpponent]);

    const handleSquareClick = useCallback((square: Square) => {
        const currentState = gameRef.current.getState();
        if (myColorRef.current === null || currentState.currentTurn !== myColorRef.current) return;
        if (currentState.phase === GamePhase.GAME_OVER) return;
        if (currentState.phase === GamePhase.ROLL_DICE) return;

        // Select a piece
        if (!currentState.selectedSquare) {
            const newState = gameRef.current.handleSelectPiece(square);
            if (newState.selectedSquare) playSelectSound();
            setState({ ...newState });
            return;
        }

        // Switch to different piece
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

        // Make move — save counts BEFORE handleMove (GameManager mutates in-place)
        const prevMoveCount = currentState.moveHistory.length;
        const prevWhiteCaptures = currentState.capturedPieces.white.length;
        const prevBlackCaptures = currentState.capturedPieces.black.length;

        const newState = gameRef.current.handleMove(square);
        if (newState.moveHistory.length > prevMoveCount) {
            syncToOpponent(newState, 'move');

            if (newState.phase === GamePhase.GAME_OVER) {
                newState.winner === 'draw' ? playDrawSound() : playCheckmateSound();
            } else if (newState.isCheck) {
                playCheckSound();
            } else if (
                newState.capturedPieces.white.length > prevWhiteCaptures ||
                newState.capturedPieces.black.length > prevBlackCaptures
            ) {
                playCaptureSound();
            } else {
                playMoveSound();
            }
        }
        setState({ ...newState });
    }, [syncToOpponent]);

    const handlePromotion = useCallback((from: Square, to: Square, pieceType: PieceType) => {
        const newState = gameRef.current.handlePromotion(from, to, pieceType);
        setPromotionPending(null);
        syncToOpponent(newState, 'move');

        if (newState.phase === GamePhase.GAME_OVER) {
            newState.winner === 'draw' ? playDrawSound() : playCheckmateSound();
        } else if (newState.isCheck) {
            playCheckSound();
        } else {
            playMoveSound();
        }
        setState({ ...newState });
    }, [syncToOpponent]);

    const handleRematch = useCallback(() => {
        socketRef.current?.emit('rematch-request', roomCodeRef.current);
    }, []);

    // ── Lobby UI ────────────────────────────────────────────
    if (status === 'lobby' || status === 'connecting') {
        return (
            <div className="landing-hero" id="online-game">
                <Link href="/" className="back-button" id="back-btn">← Back</Link>
                <h1 className="landing-title" style={{ fontSize: 'clamp(2rem, 4vw, 3rem)' }}>
                    🌐 <span className="highlight">Online</span> Play
                </h1>
                <p className="landing-subtitle">
                    Play Dice Chess with friends. Create a room or join with a code.
                </p>
                <div className="rules-card" style={{ maxWidth: 400, width: '100%' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                        <button className="btn-primary" style={{ width: '100%', fontSize: '1.1rem', padding: '16px' }}
                            onClick={handleCreateRoom} disabled={status === 'connecting'} id="create-room-btn">
                            {status === 'connecting' ? '⏳ Connecting...' : '🏠 Create Room'}
                        </button>
                        <div style={{ textAlign: 'center', color: 'var(--color-text-muted)', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: 2 }}>or</div>
                        <div style={{ display: 'flex', gap: 8 }}>
                            <input type="text" placeholder="Room code..." value={inputCode}
                                onChange={(e) => setInputCode(e.target.value.toUpperCase())} maxLength={5}
                                style={{ flex: 1, padding: '14px 16px', background: 'var(--color-bg-secondary)', border: '2px solid rgba(139, 92, 246, 0.3)', borderRadius: 'var(--radius-md)', color: 'var(--color-text-primary)', fontFamily: 'var(--font-heading)', fontSize: '1.1rem', letterSpacing: 4, textAlign: 'center', outline: 'none' }}
                                id="room-code-input" />
                            <button className="btn-primary" onClick={handleJoinRoom} disabled={inputCode.length < 4 || status === 'connecting'} id="join-room-btn">Join</button>
                        </div>
                        {error && <div className="status-banner check">{error}</div>}
                    </div>
                </div>
            </div>
        );
    }

    // ── Waiting for Opponent ────────────────────────────────
    if (status === 'waiting') {
        return (
            <div className="landing-hero" id="online-waiting">
                <Link href="/" className="back-button" id="back-btn">← Back</Link>
                <h1 className="landing-title" style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)' }}>
                    Waiting for opponent...
                </h1>
                <div className="rules-card" style={{ maxWidth: 400, width: '100%', textAlign: 'center' }}>
                    <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: 2, marginBottom: 16 }}>Share this code</div>
                    <div style={{ fontSize: '2.5rem', fontFamily: 'var(--font-heading)', fontWeight: 800, letterSpacing: 8, color: 'var(--color-accent-gold)', marginBottom: 16 }}>{displayRoomCode}</div>
                    <div style={{ fontSize: '0.9rem', color: 'var(--color-text-secondary)' }}>
                        You are playing as <strong>{displayColor === Color.WHITE ? 'White' : 'Black'}</strong>
                    </div>
                </div>
            </div>
        );
    }

    // ── Disconnected ────────────────────────────────────────
    if (status === 'disconnected') {
        return (
            <div className="landing-hero" id="online-disconnected">
                <Link href="/" className="back-button" id="back-btn">← Back</Link>
                <div className="modal-content" style={{ position: 'relative' }}>
                    <div style={{ fontSize: '3rem', marginBottom: 12 }}>😢</div>
                    <div className="modal-title">Opponent Disconnected</div>
                    <div className="modal-subtitle">Your opponent left the game.</div>
                    <div className="modal-buttons">
                        <button className="btn-primary" onClick={() => { setStatus('lobby'); roomCodeRef.current = ''; setDisplayRoomCode(''); }}>← Back to Lobby</button>
                    </div>
                </div>
            </div>
        );
    }

    // ── Active Game ─────────────────────────────────────────
    const flipped = displayColor === Color.BLACK;

    return (
        <div className="game-layout" id="online-game-playing">
            <Link href="/" className="back-button" id="back-btn">← Back</Link>

            <div className="game-sidebar">
                <div className="status-banner info" style={{ fontSize: '0.8rem' }}>
                    Room: <strong>{displayRoomCode}</strong> · You: <strong>{displayColor === Color.WHITE ? 'White' : 'Black'}</strong>
                </div>
                <GameHUD state={state} />
                {!isMyTurn && state.phase !== GamePhase.GAME_OVER && (
                    <div className="status-banner info">⏳ Opponent&apos;s turn</div>
                )}
                <Dice
                    currentTurn={state.currentTurn}
                    diceResult={state.diceResult}
                    canRoll={isMyTurn && state.phase === GamePhase.ROLL_DICE}
                    onRoll={handleRollDice}
                />
            </div>

            <Board state={state} onSquareClick={handleSquareClick} flipped={flipped} />

            {promotionPending && (
                <PromotionModal color={state.currentTurn} from={promotionPending.from} to={promotionPending.to} onSelect={handlePromotion} />
            )}

            {state.phase === GamePhase.GAME_OVER && (
                <GameOverModal winner={state.winner} onRematch={handleRematch} onExit={() => { socketRef.current?.disconnect(); window.location.href = '/'; }} />
            )}
        </div>
    );
}
