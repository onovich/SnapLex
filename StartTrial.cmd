@echo off
setlocal
cd /d "%~dp0"

if not defined SNAPLEX_APP_DATA_DIR set "SNAPLEX_APP_DATA_DIR=%CD%\snaplex-smoke-data\trial-source"
if not defined SNAPLEX_PROVIDER set "SNAPLEX_PROVIDER=fake"
if not defined SNAPLEX_PROVIDER_ORDER set "SNAPLEX_PROVIDER_ORDER=fake"

echo Starting SnapLex from source...
echo App data: %SNAPLEX_APP_DATA_DIR%
echo Provider: %SNAPLEX_PROVIDER%
echo.

python -m snaplex %*
