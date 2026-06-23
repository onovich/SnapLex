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

if not defined SNAPLEX_APP_DATA_DIR set "SNAPLEX_APP_DATA_DIR=%CD%\snaplex-smoke-data\trial-real-packaged"
call "%~dp0RequireRealProvider.cmd"
if errorlevel 1 exit /b 1

echo Starting packaged SnapLex with real translation...
echo App data: %SNAPLEX_APP_DATA_DIR%
echo Provider: %SNAPLEX_PROVIDER%
echo Target language: %SNAPLEX_TARGET_LANG%
echo.

"dist\SnapLex\SnapLex.exe" %*
