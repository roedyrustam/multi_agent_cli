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

Write-Host "Installing dependencies and CLI tool..." -ForegroundColor Cyan
& ".\venv\Scripts\pip.exe" install -e .

Write-Host "🌍 Creating global wrapper script..." -ForegroundColor Cyan
$WrapperPath = Join-Path $InstallDir "macli.cmd"
Set-Content -Path $WrapperPath -Value "@echo off`r`n`"%~dp0venv\Scripts\macli.exe`" %*"

Write-Host "🔗 Adding to User PATH..." -ForegroundColor Cyan
$UserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($UserPath -notmatch [regex]::Escape($InstallDir)) {
    $NewPath = "$InstallDir;$UserPath"
    [Environment]::SetEnvironmentVariable("PATH", $NewPath, "User")
    Write-Host "✅ Added $InstallDir to PATH." -ForegroundColor Green
} else {
    Write-Host "✅ Already in PATH." -ForegroundColor Green
}

Write-Host "✅ Installation Complete!" -ForegroundColor Cyan
Write-Host "To get started, simply open a NEW terminal and run:" -ForegroundColor White
Write-Host "  macli setup" -ForegroundColor Yellow
