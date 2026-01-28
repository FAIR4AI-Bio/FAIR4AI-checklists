# PowerShell script to run FAIR4AI agent

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "FAIR4AI Evaluation Agent" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher" -ForegroundColor Yellow
    pause
    exit 1
}

# Check if API key is set
if (-not $env:OPENAI_API_KEY -and -not $env:ANTHROPIC_API_KEY) {
    Write-Host ""
    Write-Host "ERROR: No API key found!" -ForegroundColor Red
    Write-Host "Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Example:" -ForegroundColor Cyan
    Write-Host '  $env:OPENAI_API_KEY="your-key-here"' -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

# Check for metadata files in parent directory
$metadataFiles = Get-ChildItem -Path "..\metadata_downloads\*.json" -ErrorAction SilentlyContinue

if ($metadataFiles.Count -eq 0) {
    Write-Host ""
    Write-Host "ERROR: No metadata files found in ..\metadata_downloads\" -ForegroundColor Red
    Write-Host "Please add JSON metadata files to evaluate" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "Found $($metadataFiles.Count) metadata file(s):" -ForegroundColor Green
foreach ($file in $metadataFiles) {
    Write-Host "  - $($file.Name)" -ForegroundColor White
}

# Run the agent
Write-Host ""
Write-Host "Running evaluation..." -ForegroundColor Cyan
Write-Host ""

$metadataArgs = $metadataFiles | ForEach-Object { $_.FullName }

python fair4ai_agent.py --metadata @metadataArgs --output evaluation_results

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "Evaluation Complete!" -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "Check evaluation_results.json and evaluation_results.csv" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Red
    Write-Host "Evaluation Failed!" -ForegroundColor Red
    Write-Host "======================================================================" -ForegroundColor Red
}

Write-Host ""
pause
