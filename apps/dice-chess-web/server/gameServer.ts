// ============================================================
// Dice Chess — WebSocket Game Server (Socket.IO)
// ============================================================
// Run with: npx ts-node --esm server/gameServer.ts
// Or: node --loader ts-node/esm server/gameServer.ts

import { createServer } from 'http';
import { Server, Socket } from 'socket.io';

interface Room {
    id: string;
    white: string | null;
    black: string | null;
    spectators: string[];
    state: any; // GameState from client
    createdAt: number;
}

const httpServer = createServer();
const io = new Server(httpServer, {
    cors: {
        origin: ['http://localhost:3000', 'http://localhost:3001'],
        methods: ['GET', 'POST'],
    },
});

const rooms = new Map<string, Room>();

function generateRoomCode(): string {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let code = '';
    for (let i = 0; i < 5; i++) {
        code += chars[Math.floor(Math.random() * chars.length)];
    }
    return code;
}

function cleanupOldRooms() {
    const now = Date.now();
    const TWO_HOURS = 2 * 60 * 60 * 1000;
    for (const [id, room] of rooms) {
        if (now - room.createdAt > TWO_HOURS) {
            rooms.delete(id);
        }
    }
}

// Clean up every 30 minutes
setInterval(cleanupOldRooms, 30 * 60 * 1000);

io.on('connection', (socket: Socket) => {
    console.log(`🔌 Connected: ${socket.id}`);

    // ── Create Room ───────────────────────────────────────
    socket.on('create-room', (callback: (response: any) => void) => {
        let code = generateRoomCode();
        while (rooms.has(code)) {
            code = generateRoomCode();
        }

        const room: Room = {
            id: code,
            white: socket.id,
            black: null,
            spectators: [],
            state: null,
            createdAt: Date.now(),
        };

        rooms.set(code, room);
        socket.join(code);

        console.log(`🏠 Room ${code} created by ${socket.id}`);
        callback({ success: true, roomCode: code, color: 'white' });
    });

    // ── Join Room ─────────────────────────────────────────
    socket.on('join-room', (roomCode: string, callback: (response: any) => void) => {
        const room = rooms.get(roomCode.toUpperCase());

        if (!room) {
            callback({ success: false, error: 'Room not found' });
            return;
        }

        if (room.white && room.black) {
            // Room full — join as spectator
            room.spectators.push(socket.id);
            socket.join(roomCode);
            callback({ success: true, roomCode, color: 'spectator' });
            return;
        }

        // Assign to empty color
        if (!room.white) {
            room.white = socket.id;
        } else {
            room.black = socket.id;
        }

        socket.join(roomCode);

        const assignedColor = room.white === socket.id ? 'white' : 'black';
        console.log(`🎮 ${socket.id} joined room ${roomCode} as ${assignedColor}`);
        callback({ success: true, roomCode, color: assignedColor });

        // Notify the room that both players are ready
        if (room.white && room.black) {
            io.to(roomCode).emit('game-ready', {
                white: room.white,
                black: room.black,
            });
        }
    });

    // ── Game State Sync ───────────────────────────────────
    socket.on('roll-dice', (roomCode: string, diceResult: any) => {
        socket.to(roomCode).emit('opponent-rolled', diceResult);
    });

    socket.on('select-piece', (roomCode: string, square: any) => {
        socket.to(roomCode).emit('opponent-selected', square);
    });

    socket.on('make-move', (roomCode: string, move: any) => {
        socket.to(roomCode).emit('opponent-moved', move);
    });

    socket.on('promote', (roomCode: string, data: any) => {
        socket.to(roomCode).emit('opponent-promoted', data);
    });

    socket.on('sync-state', (roomCode: string, state: any) => {
        const room = rooms.get(roomCode);
        if (room) {
            room.state = state;
            socket.to(roomCode).emit('state-synced', state);
        }
    });

    socket.on('rematch-request', (roomCode: string) => {
        socket.to(roomCode).emit('rematch-requested', socket.id);
    });

    socket.on('rematch-accept', (roomCode: string) => {
        io.to(roomCode).emit('rematch-accepted');
    });

    // ── Disconnect ────────────────────────────────────────
    socket.on('disconnect', () => {
        console.log(`❌ Disconnected: ${socket.id}`);

        // Clean up the player from rooms
        for (const [code, room] of rooms) {
            if (room.white === socket.id) {
                room.white = null;
                io.to(code).emit('opponent-disconnected', 'white');
            } else if (room.black === socket.id) {
                room.black = null;
                io.to(code).emit('opponent-disconnected', 'black');
            } else {
                room.spectators = room.spectators.filter(id => id !== socket.id);
            }

            // Delete empty rooms
            if (!room.white && !room.black && room.spectators.length === 0) {
                rooms.delete(code);
                console.log(`🗑️ Room ${code} deleted (empty)`);
            }
        }
    });
});

const PORT = parseInt(process.env.PORT || '3001', 10);
httpServer.listen(PORT, () => {
    console.log(`🚀 Dice Chess WebSocket server running on port ${PORT}`);
});
