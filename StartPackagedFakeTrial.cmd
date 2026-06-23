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

if not defined SNAPLEX_APP_DATA_DIR set "SNAPLEX_APP_DATA_DIR=%CD%\snaplex-smoke-data\trial-fake-packaged"
set "SNAPLEX_PROVIDER=fake"
set "SNAPLEX_PROVIDER_ORDER=fake"
if not defined SNAPLEX_TARGET_LANG set "SNAPLEX_TARGET_LANG=zh"

echo Starting packaged SnapLex in fake smoke mode...
echo App data: %SNAPLEX_APP_DATA_DIR%
echo Provider: fake smoke mode; this is not real translation.
echo Target language: %SNAPLEX_TARGET_LANG%
echo.

"dist\SnapLex\SnapLex.exe" %*
