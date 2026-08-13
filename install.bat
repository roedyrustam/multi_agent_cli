@echo off
echo =========================================
echo  Installing Multi-Agent CLI...
echo =========================================

set REPO_URL=https://github.com/YOUR_USERNAME/multi-agent-cli.git
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

echo Installing dependencies...
call venv\Scripts\pip.exe install -r requirements.txt

echo.
echo =========================================
echo  Installation Complete!
echo =========================================
echo To get started, run the following commands:
echo   cd %INSTALL_DIR%
echo   venv\Scripts\activate.bat
echo   python cli.py setup
echo.
