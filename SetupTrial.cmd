@echo off
setlocal
cd /d "%~dp0"

echo Installing SnapLex trial dependencies...
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

python -m pip install -e ".[gui,package]"
if errorlevel 1 (
  echo.
  echo Setup failed. Check Python/pip output above.
  exit /b 1
)

echo.
echo Setup complete.
echo Next:
echo   BuildTrial.cmd
echo   StartTrial.cmd          ^(requires a real provider env var^)
echo   StartFakeTrial.cmd      ^(UI smoke only; not real translation^)
