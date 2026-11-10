Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Launching ReconMail OSINT Dashboard..." -ForegroundColor Green
Write-Host "  Target Port: 5050 | UI: http://localhost:5050" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location -Path $PSScriptRoot

Start-Process "http://localhost:5050"
py app.py
