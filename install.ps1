Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "    __  __              ___   _       ___ " -ForegroundColor Cyan
Write-Host "   |  \/  |  __ _   ___| \ \ | |     |_ _|" -ForegroundColor Cyan
Write-Host "   | |\/| | / _`` | / __| |\ \| |      | | " -ForegroundColor Cyan
Write-Host "   | |  | || (_| || (__| | \ \ |___   | | " -ForegroundColor Cyan
Write-Host "   |_|  |_| \__,_| \___|_|  \_\____| |___|" -ForegroundColor Cyan
Write-Host " "
Write-Host "          S W A R M   D I R E C T O R     " -ForegroundColor Magenta
Write-Host "            Crafted by Roedy Rustam       " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[SYSTEM INITIALIZATION SEQUENCE STARTED...]" -ForegroundColor DarkGray
Start-Sleep -Seconds 1
Write-Host ""
Write-Host "🚀 Bootstrapping Neural Uplink (Installing CLI)..." -ForegroundColor Cyan

$RepoUrl = "https://github.com/roedyrustam/multi_agent_cli.git"
if (Test-Path (Join-Path $PWD "setup.py")) {
    $InstallDir = $PWD.Path
    Write-Host "📍 Detected local repository at $InstallDir" -ForegroundColor Yellow
} else {
    $InstallDir = "$env:USERPROFILE\multi-agent-cli"
}

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
    git fetch --all
    git reset --hard origin/main
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
    $env:PATH = "$InstallDir;" + $env:PATH
    Write-Host "✅ Added $InstallDir to PATH." -ForegroundColor Green
} else {
    $env:PATH = "$InstallDir;" + $env:PATH
    Write-Host "✅ Already in PATH." -ForegroundColor Green
}

Write-Host "✅ Installation Complete!" -ForegroundColor Cyan
Write-Host "To get started, simply open a NEW terminal and run:" -ForegroundColor White
Write-Host "  macli setup" -ForegroundColor Yellow
