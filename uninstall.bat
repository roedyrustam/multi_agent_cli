@echo off
color 0C
echo ==========================================================
echo           S W A R M   D I R E C T O R     
echo               Uninstallation Utility      
echo ==========================================================
echo.

set INSTALL_DIR=%USERPROFILE%\multi-agent-cli

echo Cleaning up User PATH registry...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$InstallDir = '%INSTALL_DIR%'; $UserPath = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($UserPath) { $Paths = $UserPath -split ';'; $NewPaths = $Paths | Where-Object { $_ -ne $InstallDir -and $_ -ne '' }; $NewPathString = $NewPaths -join ';'; [Environment]::SetEnvironmentVariable('PATH', $NewPathString, 'User'); Write-Host '✅ Successfully removed from User PATH.' -ForegroundColor Green }"

echo Removing Virtual Environment...
if exist "%INSTALL_DIR%\venv" (
    rmdir /s /q "%INSTALL_DIR%\venv"
    echo ✅ Virtual Environment removed.
)

echo Removing Global Wrapper...
if exist "%INSTALL_DIR%\macli.cmd" (
    del /f /q "%INSTALL_DIR%\macli.cmd"
    echo ✅ Wrapper script removed.
)

echo.
echo ==========================================================
echo ✅ Uninstallation Complete!
echo To completely remove all files, you can now safely delete the folder:
echo   %INSTALL_DIR%
echo ==========================================================
echo.
