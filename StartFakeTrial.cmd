@echo off
setlocal
cd /d "%~dp0"

if not defined SNAPLEX_APP_DATA_DIR set "SNAPLEX_APP_DATA_DIR=%CD%\snaplex-smoke-data\trial-fake-source"
set "SNAPLEX_PROVIDER=fake"
set "SNAPLEX_PROVIDER_ORDER=fake"
if not defined SNAPLEX_TARGET_LANG set "SNAPLEX_TARGET_LANG=zh"

echo Starting SnapLex from source in fake smoke mode...
echo App data: %SNAPLEX_APP_DATA_DIR%
echo Provider: fake smoke mode; this is not real translation.
echo Target language: %SNAPLEX_TARGET_LANG%
echo.

python -m snaplex %*
