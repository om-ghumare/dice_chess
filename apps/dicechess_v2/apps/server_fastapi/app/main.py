from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Allow local engine import without published package install.
ROOT = Path(__file__).resolve().parents[3]
ENGINE_PATH = ROOT / "packages" / "dice_chess_engine"
if str(ENGINE_PATH) not in sys.path:
    sys.path.insert(0, str(ENGINE_PATH))

from app.api.auth import router as auth_router
from app.api.game import router as game_router
from app.api.profile import router as profile_router
from app.api.websocket import router as ws_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(game_router)
app.include_router(ws_router)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "service": settings.app_name, "version": settings.app_version}
