# Dice Chess

Dice Chess workspace containing the current rebuild plus the original Python
pygame experiments.

## Repository layout

```text
apps/
  dicechess_v2/       Flutter client, FastAPI backend, Python rules engine
  dice-chess-web/     Next.js web implementation
assets/
  images/             Original pygame piece and dice assets
  images2/            Alternate image set
legacy/
  prototypes/         Early single-file pygame versions
  refactored/         Refactored pygame implementation
  chessgame/          Modular pygame implementation
  experiments/        Small pygame test programs
archive/
  snapshots/          Local-only older copied project folders
```

## Quick start

### Legacy pygame

```powershell
python -m pip install -r requirements.txt
python legacy/prototypes/chess0_6.py
```

### Current rebuild

See [apps/dicechess_v2/README.md](apps/dicechess_v2/README.md).

### Web app

```powershell
cd apps/dice-chess-web
npm install
npm run dev
```

## Git notes

Generated folders such as `__pycache__`, `.next`, `node_modules`, Flutter
`build`, Python package metadata, and `archive/snapshots` are ignored. Keep new
source under `apps`, `legacy`, `assets`, or `docs` rather than adding loose
files at the repository root.
