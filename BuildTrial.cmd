@echo off
setlocal
cd /d "%~dp0"

echo Building SnapLex base trial package...
python scripts\package_windows.py --variant base
if errorlevel 1 (
  echo.
  echo Build failed. If PyInstaller or PySide6 is missing, run SetupTrial.cmd first.
  exit /b 1
)

echo.
echo Build complete:
echo   %CD%\dist\SnapLex\SnapLex.exe
echo.
echo Next:
echo   StartPackagedTrial.cmd
echo   SmokeTrial.cmd
