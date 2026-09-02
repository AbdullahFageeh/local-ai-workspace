# Start-LlamaFactory.ps1 - Launch LLaMA-Factory Web UI for Visual Fine-Tuning
# GitHub: https://github.com/hiyouga/LLaMA-Factory

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Launching LLaMA-Factory Web UI (Visual Fine-Tuning Board)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$llamaFactoryDir = "$HOME\LLaMA-Factory"

if (-not (Test-Path $llamaFactoryDir)) {
    Write-Host "Cloning LLaMA-Factory repository..." -ForegroundColor Yellow
    git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git $llamaFactoryDir
    Write-Host "Installing LLaMA-Factory dependencies..." -ForegroundColor Yellow
    pip install -e "$llamaFactoryDir[torch,metrics]"
}

Write-Host "Copying your local dataset to LLaMA-Factory data folder..." -ForegroundColor Cyan
Copy-Item ".\dataset_alpaca.json" "$llamaFactoryDir\data\custom_dataset.json" -Force

Write-Host "Starting LLaMA-Factory Web Dashboard at http://localhost:7860..." -ForegroundColor Green
Start-Process "http://localhost:7860"

# Launch Web UI with Gradio
python "$llamaFactoryDir\src\webui.py"
