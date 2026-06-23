@echo off
setlocal
cd /d "%~dp0"

if not exist "dist\SnapLex\SnapLex.exe" (
  echo Packaged executable was not found:
  echo   %CD%\dist\SnapLex\SnapLex.exe
  echo.
  echo Run BuildTrial.cmd first.
  exit /b 1
)

if not defined SNAPLEX_APP_DATA_DIR set "SNAPLEX_APP_DATA_DIR=%CD%\snaplex-smoke-data\trial-packaged"
if not defined SNAPLEX_PROVIDER set "SNAPLEX_PROVIDER=fake"
if not defined SNAPLEX_PROVIDER_ORDER set "SNAPLEX_PROVIDER_ORDER=fake"

echo Starting packaged SnapLex...
echo App data: %SNAPLEX_APP_DATA_DIR%
echo Provider: %SNAPLEX_PROVIDER%
echo.

"dist\SnapLex\SnapLex.exe" %*
