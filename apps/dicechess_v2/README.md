# dicechess_v2

Clean rebuild of Dice Chess for Android (Play Store) and Windows with:

- Flutter client (`apps/client_flutter`)
- FastAPI backend (`apps/server_fastapi`)
- Deterministic rules engine (`packages/dice_chess_engine`)
- Specs and architecture docs (`docs/specs`)
- Local infra (`infra`)

## Workspace structure

```text
dicechess_v2/
  apps/
    client_flutter/
    server_fastapi/
  packages/
    dice_chess_engine/
  docs/specs/
  infra/
  scripts/
```

## Quick start

### Engine

```powershell
cd packages/dice_chess_engine
python -m pip install -e .[dev]
pytest
```

### Server

```powershell
cd apps/server_fastapi
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Client

```powershell
cd apps/client_flutter
flutter pub get
flutter run
```

## Notes

- Existing legacy pygame code is intentionally untouched.
- `docs/specs/rules-v1.md` is the v1 rules contract for engine parity.
