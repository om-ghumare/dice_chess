Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Starting DiceChess v2 local stack..."
Push-Location "$PSScriptRoot\..\infra"
docker compose up --build
Pop-Location
