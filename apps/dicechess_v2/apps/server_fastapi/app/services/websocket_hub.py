from __future__ import annotations

from collections import defaultdict

from fastapi import WebSocket


class WebSocketHub:
    def __init__(self) -> None:
        self.lobby_connections: set[WebSocket] = set()
        self.match_connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect_lobby(self, ws: WebSocket) -> None:
        await ws.accept()
        self.lobby_connections.add(ws)

    async def connect_match(self, match_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self.match_connections[match_id].add(ws)

    def disconnect_lobby(self, ws: WebSocket) -> None:
        self.lobby_connections.discard(ws)

    def disconnect_match(self, match_id: str, ws: WebSocket) -> None:
        self.match_connections[match_id].discard(ws)

    async def broadcast_lobby(self, payload: dict) -> None:
        stale: list[WebSocket] = []
        for ws in self.lobby_connections:
            try:
                await ws.send_json(payload)
            except Exception:
                stale.append(ws)
        for ws in stale:
            self.disconnect_lobby(ws)

    async def broadcast_match(self, match_id: str, payload: dict) -> None:
        stale: list[WebSocket] = []
        for ws in self.match_connections[match_id]:
            try:
                await ws.send_json(payload)
            except Exception:
                stale.append(ws)
        for ws in stale:
            self.disconnect_match(match_id, ws)
