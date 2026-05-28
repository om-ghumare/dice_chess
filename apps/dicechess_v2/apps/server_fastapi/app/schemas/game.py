from pydantic import BaseModel


class CreateRoomResponse(BaseModel):
    room_code: str


class JoinRoomResponse(BaseModel):
    room_code: str
    players: list[str]


class QueueRequest(BaseModel):
    queue: str = "casual"


class MatchResponse(BaseModel):
    match_id: str
    white_user_id: str
    black_user_id: str
    state: dict
    created_at: str
