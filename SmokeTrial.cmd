@echo off
setlocal
cd /d "%~dp0"

echo Running SnapLex trial smoke checks...
echo.

python -m snaplex --version
if errorlevel 1 exit /b 1

python -m snaplex --no-gui
if errorlevel 1 exit /b 1

python scripts\package_windows.py --dry-run --variant base
if errorlevel 1 exit /b 1

if exist "dist\SnapLex\SnapLex.exe" (
  set "SNAPLEX_APP_DATA_DIR=%CD%\snaplex-smoke-data\trial-smoke"
  echo.
  echo Running packaged executable smoke...
  "dist\SnapLex\SnapLex.exe" --version
  if errorlevel 1 exit /b 1
  "dist\SnapLex\SnapLex.exe" --no-gui
  if errorlevel 1 exit /b 1
  "dist\SnapLex\SnapLex.exe" --smoke-package
  if errorlevel 1 exit /b 1
) else (
  echo.
  echo Packaged executable not found. Run BuildTrial.cmd to create it.
)

echo.
echo Trial smoke checks passed.
