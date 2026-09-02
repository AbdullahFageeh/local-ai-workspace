# Start-AIWorkspace.ps1 - Launch Ollama service and Open-WebUI

Write-Host "Checking Ollama status..." -ForegroundColor Cyan

# 1. Start Ollama service if not already running
$ollamaProc = Get-Process -Name "ollama app", "ollama" -ErrorAction SilentlyContinue
if (-not $ollamaProc) {
    Write-Host "Starting Ollama service..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
} else {
    Write-Host "Ollama service is already active." -ForegroundColor Green
}

# 2. Open default browser to Open-WebUI
Write-Host "Opening browser to http://localhost:8080..." -ForegroundColor Cyan
Start-Process "http://localhost:8080"

# 3. Start Open-WebUI server (foreground process)
Write-Host "Starting Open-WebUI server (press Ctrl+C to stop)..." -ForegroundColor Green
open-webui serve
