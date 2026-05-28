from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

from app.services.auth_service import resolve_user
from app.services.runtime_match_service import (
    apply_move_for_turn,
    get_runtime,
    is_player_turn,
    player_color,
    roll_for_turn,
    state_payload,
)
from app.services.websocket_hub import WebSocketHub

router = APIRouter(tags=["websocket"])
hub = WebSocketHub()


@router.websocket("/ws/lobby")
async def ws_lobby(websocket: WebSocket) -> None:
    await hub.connect_lobby(websocket)
    await websocket.send_json({"type": "presence.ping", "payload": {"status": "connected"}})
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")
            if event_type == "presence.ping":
                await websocket.send_json({"type": "presence.pong", "payload": {"ok": True}})
            else:
                await hub.broadcast_lobby({"type": "lobby.event", "payload": data})
    except WebSocketDisconnect:
        hub.disconnect_lobby(websocket)


@router.websocket("/ws/match/{match_id}")
async def ws_match(match_id: str, websocket: WebSocket) -> None:
    token = websocket.query_params.get("token", "")
    try:
        user_id = resolve_user(token)
    except Exception:
        await websocket.accept()
        await websocket.send_json({"type": "error", "payload": {"code": "UNAUTHORIZED", "message": "Invalid token"}})
        await websocket.close()
        return

    runtime = get_runtime(match_id)
    if runtime is None:
        await websocket.accept()
        await websocket.send_json({"type": "error", "payload": {"code": "MATCH_NOT_FOUND", "message": "Match not found"}})
        await websocket.close()
        return
    if player_color(runtime, user_id) is None:
        await websocket.accept()
        await websocket.send_json({"type": "error", "payload": {"code": "FORBIDDEN", "message": "Not a match participant"}})
        await websocket.close()
        return

    await hub.connect_match(match_id, websocket)
    await websocket.send_json({"type": "match.state", "payload": state_payload(match_id)})
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")
            payload = data.get("payload", {})
            runtime = get_runtime(match_id)
            if runtime is None:
                await websocket.send_json(
                    {"type": "error", "payload": {"code": "MATCH_NOT_FOUND", "message": "Match not found"}}
                )
                continue

            if event_type == "presence.ping":
                await websocket.send_json({"type": "presence.pong", "payload": {"ok": True}})
                continue

            if event_type == "match.roll_request":
                if not is_player_turn(runtime, user_id):
                    await websocket.send_json(
                        {"type": "error", "payload": {"code": "NOT_YOUR_TURN", "message": "Cannot roll now"}}
                    )
                    continue
                rolled = roll_for_turn(match_id)
                await hub.broadcast_match(match_id, {"type": "match.roll_result", "payload": rolled})
                await hub.broadcast_match(match_id, {"type": "match.state", "payload": state_payload(match_id)})
                continue

            if event_type == "match.move_submit":
                if not is_player_turn(runtime, user_id):
                    await websocket.send_json(
                        {"type": "error", "payload": {"code": "NOT_YOUR_TURN", "message": "Cannot move now"}}
                    )
                    continue
                src = tuple(payload.get("from", []))
                dst = tuple(payload.get("to", []))
                if len(src) != 2 or len(dst) != 2:
                    await websocket.send_json(
                        {"type": "error", "payload": {"code": "BAD_PAYLOAD", "message": "from/to must be [x,y]"}}
                    )
                    continue
                ok, result = apply_move_for_turn(match_id, (int(src[0]), int(src[1])), (int(dst[0]), int(dst[1])), payload.get("promotion"))
                if not ok:
                    await websocket.send_json({"type": "error", "payload": result})
                    continue
                await hub.broadcast_match(match_id, {"type": "match.move_result", "payload": {"ok": True, **result}})
                await hub.broadcast_match(match_id, {"type": "match.state", "payload": state_payload(match_id)})
                state = runtime["state_obj"]
                if state.winner is not None or state.is_stalemate:
                    await hub.broadcast_match(
                        match_id,
                        {
                            "type": "match.end",
                            "payload": {
                                "result": "draw" if state.is_stalemate else f"{state.winner.value}_win",
                                "reason": "stalemate" if state.is_stalemate else "checkmate",
                            },
                        },
                    )
                continue

            await websocket.send_json(
                {"type": "error", "payload": {"code": "UNKNOWN_EVENT", "message": f"Unknown event: {event_type}"}}
            )
    except WebSocketDisconnect:
        hub.disconnect_match(match_id, websocket)
    finally:
        if websocket.application_state != WebSocketState.DISCONNECTED:
            hub.disconnect_match(match_id, websocket)
