from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import current_user_id
from app.core.store import MATCHES, ROOMS, room_code
from app.schemas.game import CreateRoomResponse, JoinRoomResponse, MatchResponse, QueueRequest
from app.services.matchmaking_service import dequeue_user, enqueue_user
from app.services.match_service import create_match

router = APIRouter(tags=["game"])


@router.post("/rooms", response_model=CreateRoomResponse)
def create_room(user_id: str = Depends(current_user_id)) -> CreateRoomResponse:
    code = room_code()
    ROOMS[code] = [user_id]
    return CreateRoomResponse(room_code=code)


@router.post("/rooms/{code}/join", response_model=JoinRoomResponse)
def join_room(code: str, user_id: str = Depends(current_user_id)) -> JoinRoomResponse:
    if code not in ROOMS:
        raise HTTPException(status_code=404, detail="Room not found")
    if user_id not in ROOMS[code]:
        ROOMS[code].append(user_id)
    return JoinRoomResponse(room_code=code, players=ROOMS[code])


@router.post("/matchmaking/enqueue")
def matchmaking_enqueue(payload: QueueRequest, user_id: str = Depends(current_user_id)) -> dict:
    _ = payload.queue  # queue name reserved for future.
    return enqueue_user(user_id)


@router.post("/matchmaking/dequeue")
def matchmaking_dequeue(user_id: str = Depends(current_user_id)) -> dict:
    dequeue_user(user_id)
    return {"ok": True}


@router.post("/matches/local", response_model=MatchResponse)
def create_local_match(user_id: str = Depends(current_user_id)) -> MatchResponse:
    match = create_match(user_id, user_id)
    return MatchResponse(
        match_id=match.match_id,
        white_user_id=match.white_user_id,
        black_user_id=match.black_user_id,
        state=match.state,
        created_at=match.created_at,
    )


@router.get("/matches", response_model=list[MatchResponse])
def list_matches(user_id: str = Depends(current_user_id)) -> list[MatchResponse]:
    records = [
        m
        for m in MATCHES.values()
        if m.white_user_id == user_id or m.black_user_id == user_id
    ]
    return [
        MatchResponse(
            match_id=m.match_id,
            white_user_id=m.white_user_id,
            black_user_id=m.black_user_id,
            state=m.state,
            created_at=m.created_at,
        )
        for m in records
    ]


@router.get("/matches/{match_id}", response_model=MatchResponse)
def get_match(match_id: str, user_id: str = Depends(current_user_id)) -> MatchResponse:
    match = MATCHES.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if user_id not in (match.white_user_id, match.black_user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
    return MatchResponse(
        match_id=match.match_id,
        white_user_id=match.white_user_id,
        black_user_id=match.black_user_id,
        state=match.state,
        created_at=match.created_at,
    )
