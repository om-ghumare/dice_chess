# server_fastapi

FastAPI backend implementing:

- Auth endpoints (guest, google stub, refresh)
- Profile endpoints
- Room + matchmaking + match listing endpoints
- WebSocket channels (`/ws/lobby`, `/ws/match/{match_id}`)

## Run

```powershell
python -m pip install -r requirements.txt
python -m pip install -e ../../packages/dice_chess_engine
uvicorn app.main:app --reload
```
