Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Bootstrapping engine..."
Push-Location "$PSScriptRoot\..\packages\dice_chess_engine"
python -m pip install -e .[dev]
pytest
Pop-Location

Write-Host "Bootstrapping server..."
Push-Location "$PSScriptRoot\..\apps\server_fastapi"
python -m pip install -r requirements.txt
python -m pip install -e ../../packages/dice_chess_engine
pytest
Pop-Location
