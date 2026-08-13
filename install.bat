@echo off
color 0B
echo ==========================================================
echo     __  __              ___   _       ___ 
echo    ^|  \/  ^|  __ _   ___^| \ \ ^| ^|     ^|_ _^|
echo    ^| ^|\/^| ^| / _` ^| / __^| ^|\ \^| ^|      ^| ^| 
echo    ^| ^|  ^| ^|^| (_^| ^|^| (__^| ^| \ \ ^|___   ^| ^| 
echo    ^|_^|  ^|_^| \__,_^| \___^|_^|  \_\____^| ^|___^|
echo.
echo           S W A R M   D I R E C T O R     
echo             Crafted by Roedy Rustam       
echo ==========================================================
echo.
echo [SYSTEM INITIALIZATION SEQUENCE STARTED...]
timeout /t 1 /nobreak >nul
echo.
echo Bootstrapping Neural Uplink (Installing CLI)...

set REPO_URL=https://github.com/roedyrustam/multi_agent_cli.git
set INSTALL_DIR=%USERPROFILE%\multi-agent-cli

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in PATH.
    exit /b 1
)

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    exit /b 1
)

if exist "%INSTALL_DIR%" (
    echo Directory already exists: %INSTALL_DIR%.
    echo Pulling latest updates...
    cd /d "%INSTALL_DIR%"
    git pull
) else (
    echo Cloning repository to %INSTALL_DIR%...
    git clone %REPO_URL% "%INSTALL_DIR%"
    cd /d "%INSTALL_DIR%"
)

echo Setting up Python virtual environment...
python -m venv venv

echo Installing dependencies and CLI tool...
call venv\Scripts\pip.exe install -e .

echo.
echo Creating global wrapper script...
echo @echo off > macli.cmd
echo "%%~dp0venv\Scripts\macli.exe" %%* >> macli.cmd

echo Adding to User PATH...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$UserPath = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($UserPath -notmatch [regex]::Escape('%INSTALL_DIR%')) { [Environment]::SetEnvironmentVariable('PATH', '%INSTALL_DIR%;' + $UserPath, 'User'); Write-Host '✅ Added %INSTALL_DIR% to PATH.' -ForegroundColor Green } else { Write-Host '✅ Already in PATH.' -ForegroundColor Green }"

echo.
echo =========================================
echo  Installation Complete!
echo =========================================
echo To get started, simply open a NEW terminal and run:
echo   macli setup
echo.
