Write-Host "🚀 Installing Multi-Agent CLI..." -ForegroundColor Cyan

$RepoUrl = "https://github.com/roedyrustam/multi_agent_cli.git"
$InstallDir = "$env:USERPROFILE\multi-agent-cli"

if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Git is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

if (Test-Path $InstallDir) {
    Write-Host "📂 Directory already exists: $InstallDir. Pulling latest updates..." -ForegroundColor Yellow
    Set-Location $InstallDir
    git pull
} else {
    Write-Host "📥 Cloning repository to $InstallDir..." -ForegroundColor Green
    git clone $RepoUrl $InstallDir
    Set-Location $InstallDir
}

Write-Host "🐍 Setting up Python virtual environment..." -ForegroundColor Green
python -m venv venv

Write-Host "📦 Installing dependencies..." -ForegroundColor Green
.\venv\Scripts\pip.exe install -r requirements.txt

Write-Host "✅ Installation Complete!" -ForegroundColor Cyan
Write-Host "To get started, run the following commands:" -ForegroundColor White
Write-Host "  cd $InstallDir" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  python cli.py setup" -ForegroundColor Yellow
