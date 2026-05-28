Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Step($msg) {
  Write-Host ""
  Write-Host "==> $msg" -ForegroundColor Cyan
}

$root = Split-Path -Parent $PSScriptRoot
$engineDir = Join-Path $root "packages\dice_chess_engine"
$serverDir = Join-Path $root "apps\server_fastapi"
$clientDir = Join-Path $root "apps\client_flutter"

Step "Engine: install + tests"
Push-Location $engineDir
python -m pip install -e .[dev]
python -m pytest -q
Pop-Location

Step "Server: install + tests"
Push-Location $serverDir
python -m pip install -r requirements.txt
python -m pip install -e ..\..\packages\dice_chess_engine
python -m pytest -q
Pop-Location

Step "Client: pub get + widget tests"
Push-Location $clientDir
if (Get-Command flutter -ErrorAction SilentlyContinue) {
  flutter pub get
  flutter test
} else {
  Write-Warning "Flutter CLI not found in PATH. Skipping client checks."
}
Pop-Location

Step "All checks passed"
