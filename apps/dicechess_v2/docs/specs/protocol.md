# Protocol and Invariants

## REST endpoints

- `POST /auth/guest`
- `POST /auth/google`
- `POST /auth/refresh`
- `GET /profile/me`
- `PATCH /profile/me`
- `POST /rooms`
- `POST /rooms/{room_code}/join`
- `POST /matchmaking/enqueue`
- `POST /matchmaking/dequeue`
- `GET /matches`
- `GET /matches/{match_id}`

## WebSocket channels

- `/ws/lobby`
- `/ws/match/{match_id}`

## WebSocket event payloads

- `lobby.queue_join`: `{ "queue": "ranked|casual" }`
- `lobby.queue_found`: `{ "match_id": "...", "opponent_id": "..." }`
- `room.created`: `{ "room_code": "ABC123" }`
- `room.joined`: `{ "room_code": "ABC123", "players": [...] }`
- `match.state`: `{ "match_id": "...", "state": {...}, "seq": 12 }`
- `match.roll_request`: `{ "match_id": "...", "requested_by": "player_id" }`
- `match.roll_result`: `{ "piece_type": "bishop", "eligible_piece_types": [...] }`
- `match.move_submit`: `{ "from": [x, y], "to": [x, y], "promotion": "queen|null" }`
- `match.move_result`: `{ "ok": true, "state": {...}, "seq": 13 }`
- `match.end`: `{ "result": "white_win|black_win|draw", "reason": "checkmate|stalemate|resign|disconnect" }`
- `match.resync`: `{ "state": {...}, "seq": 99 }`
- `presence.ping`: `{ "ts": 123456789 }`
- `error`: `{ "code": "INVALID_MOVE", "message": "..." }`

## Invariants

- Server is authoritative for online state transitions.
- `seq` increases by 1 on every accepted state transition.
- Duplicate `match.move_submit` with same idempotency key is safe.
- A move is valid only if it matches active dice-selected piece type.
- Client may optimistically render but must reconcile to server `match.state`.
