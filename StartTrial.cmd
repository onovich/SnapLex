@echo off
setlocal
cd /d "%~dp0"

if not defined SNAPLEX_APP_DATA_DIR set "SNAPLEX_APP_DATA_DIR=%CD%\snaplex-smoke-data\trial-real-source"
call "%~dp0RequireRealProvider.cmd"
if errorlevel 1 exit /b 1

echo Starting SnapLex from source with real translation...
echo App data: %SNAPLEX_APP_DATA_DIR%
echo Provider: %SNAPLEX_PROVIDER%
echo Target language: %SNAPLEX_TARGET_LANG%
echo.

python -m snaplex %*
