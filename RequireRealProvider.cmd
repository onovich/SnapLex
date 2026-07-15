@echo off
rem Configure a real translation provider for trial launch scripts.
rem This file is meant to be called from another .cmd script.

if defined SNAPLEX_PROVIDER (
  if /I not "%SNAPLEX_PROVIDER%"=="fake" (
    if not defined SNAPLEX_PROVIDER_ORDER set "SNAPLEX_PROVIDER_ORDER=%SNAPLEX_PROVIDER%"
    goto :target
  )
)

if defined SNAPLEX_OPENAI_API_KEY (
  set "SNAPLEX_PROVIDER=openai"
  set "SNAPLEX_PROVIDER_ORDER=openai"
  goto :target
)

if defined OPENAI_API_KEY (
  set "SNAPLEX_PROVIDER=openai"
  set "SNAPLEX_PROVIDER_ORDER=openai"
  set "SNAPLEX_OPENAI_API_KEY_ENV=OPENAI_API_KEY"
  goto :target
)

if /I "%SNAPLEX_OPENAI_CREDENTIAL_SOURCE%"=="keyring" (
  set "SNAPLEX_PROVIDER=openai"
  set "SNAPLEX_PROVIDER_ORDER=openai"
  goto :target
)

if defined SNAPLEX_DEEPL_API_KEY (
  set "SNAPLEX_PROVIDER=deepl"
  set "SNAPLEX_PROVIDER_ORDER=deepl"
  goto :target
)

if defined DEEPL_API_KEY (
  set "SNAPLEX_PROVIDER=deepl"
  set "SNAPLEX_PROVIDER_ORDER=deepl"
  set "SNAPLEX_DEEPL_API_KEY_ENV=DEEPL_API_KEY"
  goto :target
)

if /I "%SNAPLEX_DEEPL_CREDENTIAL_SOURCE%"=="keyring" (
  set "SNAPLEX_PROVIDER=deepl"
  set "SNAPLEX_PROVIDER_ORDER=deepl"
  goto :target
)

if defined SNAPLEX_LIBRETRANSLATE_BASE_URL (
  set "SNAPLEX_PROVIDER=libretranslate"
  set "SNAPLEX_PROVIDER_ORDER=libretranslate"
  goto :target
)

if /I "%SNAPLEX_LIBRETRANSLATE_CREDENTIAL_SOURCE%"=="keyring" (
  set "SNAPLEX_PROVIDER=libretranslate"
  set "SNAPLEX_PROVIDER_ORDER=libretranslate"
  goto :target
)

python -m snaplex --check-real-provider
if not errorlevel 1 goto :target

echo Real translation provider is not configured.
echo.
echo Configure one of these before launching real translation.
echo PowerShell examples:
echo   $env:SNAPLEX_OPENAI_API_KEY='your_trial_key'
echo   $env:SNAPLEX_DEEPL_API_KEY='your_trial_key'
echo   $env:SNAPLEX_LIBRETRANSLATE_BASE_URL='http://localhost:5000'
echo   $env:SNAPLEX_OPENAI_CREDENTIAL_SOURCE='keyring'
echo.
echo cmd.exe examples:
echo   set SNAPLEX_OPENAI_API_KEY=your_trial_key
echo   set SNAPLEX_DEEPL_API_KEY=your_trial_key
echo   set SNAPLEX_LIBRETRANSLATE_BASE_URL=http://localhost:5000
echo   set SNAPLEX_OPENAI_CREDENTIAL_SOURCE=keyring
echo.
echo For packaging/smoke UI without real translation, use:
echo   StartPackagedFakeTrial.cmd
echo   StartFakeTrial.cmd
exit /b 1

:target
if not defined SNAPLEX_SOURCE_LANG set "SNAPLEX_SOURCE_LANG=auto"
if not defined SNAPLEX_TARGET_LANG set "SNAPLEX_TARGET_LANG=zh"
python -m snaplex --check-real-provider
if errorlevel 1 exit /b 1
exit /b 0
