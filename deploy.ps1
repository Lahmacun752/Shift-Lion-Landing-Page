$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "1/2 Website bauen..." -ForegroundColor Cyan
python .\build.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "2/2 Firebase deployen..." -ForegroundColor Cyan
firebase.cmd deploy --only hosting
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Fertig: https://shiftlion.app" -ForegroundColor Green
