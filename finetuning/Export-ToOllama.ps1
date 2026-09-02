# Export-ToOllama.ps1 - Import trained GGUF or LoRA adapter into local Ollama
param (
    [Parameter(Mandatory=$false)]
    [string]$GGUFPath = "model_q4_k_m-unsloth.Q4_K_M.gguf",
    
    [Parameter(Mandatory=$false)]
    [string]$ModelName = "my-custom-finetune:latest"
)

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Exporting Fine-Tuned Model to Ollama: $ModelName" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

if (-not (Test-Path $GGUFPath)) {
    Write-Host "Warning: GGUF file '$GGUFPath' not found in current directory." -ForegroundColor Yellow
    Write-Host "If you downloaded the GGUF from Colab/Unsloth, pass the path via: .\Export-ToOllama.ps1 -GGUFPath 'path\to\model.gguf'" -ForegroundColor Yellow
    exit 1
}

$modelfileContent = @"
FROM $GGUFPath

SYSTEM """
You are a custom fine-tuned assistant trained on proprietary codebase knowledge and coding guidelines.
Always write clean, typed, concise code.
"""

PARAMETER temperature 0.2
PARAMETER num_ctx 8192
"@

$modelfilePath = "Modelfile.$ModelName"
$modelfileContent | Set-Content $modelfilePath

Write-Host "Building Ollama model from $modelfilePath..." -ForegroundColor Green
ollama create $ModelName -f $modelfilePath

Write-Host "`nModel '$ModelName' successfully installed in Ollama!" -ForegroundColor Green
Write-Host "Test your model with: ollama run $ModelName" -ForegroundColor Cyan
