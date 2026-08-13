Write-Host "==========================================================" -ForegroundColor Red
Write-Host "           S W A R M   D I R E C T O R     " -ForegroundColor Magenta
Write-Host "               Uninstallation Utility      " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Red
Write-Host ""

$InstallDir = $PSScriptRoot
if ([string]::IsNullOrEmpty($InstallDir)) {
    $InstallDir = $PWD.Path
}
Write-Host "📍 Detected installation at: $InstallDir" -ForegroundColor Yellow
Write-Host "🧹 Cleaning up User PATH registry..." -ForegroundColor Cyan

$UserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($UserPath) {
    $Paths = $UserPath -split ';'
    $NewPaths = $Paths | Where-Object { $_ -ne $InstallDir -and $_ -ne "" }
    $NewPathString = $NewPaths -join ';'
    [Environment]::SetEnvironmentVariable("PATH", $NewPathString, "User")
    Write-Host "✅ Successfully removed $InstallDir from User PATH." -ForegroundColor Green
}

Write-Host "🗑️  Removing Virtual Environment..." -ForegroundColor Cyan
if (Test-Path "$InstallDir\venv") {
    Remove-Item -Recurse -Force "$InstallDir\venv"
    Write-Host "✅ Virtual Environment removed." -ForegroundColor Green
}

Write-Host "🗑️  Removing Global Wrapper..." -ForegroundColor Cyan
if (Test-Path "$InstallDir\macli.cmd") {
    Remove-Item -Force "$InstallDir\macli.cmd"
    Write-Host "✅ Wrapper script removed." -ForegroundColor Green
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "✅ Uninstallation Complete!" -ForegroundColor Green
Write-Host "To completely remove all files, you can now safely delete the folder:" -ForegroundColor White
Write-Host "  $InstallDir" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
