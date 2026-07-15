# P11 Packaged Trial Evidence

Date: 2026-07-16
Phase: P11 Trial Release Hardening
Status: PASS for deterministic packaged fake smoke and real-trial fail-closed

P11 preserves the P6/P10 package baseline: the packaged `base` path is
deterministic, fake-provider based, and does not require keyring, real provider
credentials, real network calls, screen permissions, model downloads, or
provider secrets.

## Trial Smoke Wrapper

Command:

```cmd
SmokeTrial.cmd
```

Result: PASS.

Evidence:

```text
SnapLex 0.1.0
SnapLex bootstrap OK (PySide6 available).
SNAPLEX_PACKAGE_VARIANT=base
C:\Python314\python.exe -m PyInstaller --distpath D:\ToolProjects\SnapLex\dist --workpath D:\ToolProjects\SnapLex\build\pyinstaller --clean --noconfirm D:\ToolProjects\SnapLex\packaging\snaplex.spec
SnapLex packaged workflow smoke PASS
- app data: D:\ToolProjects\SnapLex\snaplex-smoke-data\trial-smoke
- settings persistence: fake provider, history enabled
- clipboard translation: hello -> hello [en]
- screen fake capture/OCR translation: screen hello -> screen hello [en]
- history record/list/delete/clear: PASS
Trial smoke checks passed.
```

## Packaged Fake Trial

Command:

```cmd
StartPackagedFakeTrial.cmd --no-gui
```

Result: PASS.

Evidence:

```text
Starting packaged SnapLex in fake smoke mode...
Provider: fake smoke mode; this is not real translation.
SnapLex bootstrap OK (PySide6 available).
```

## Packaged Real Trial Fail-Closed

Command:

```cmd
StartPackagedTrial.cmd --no-gui
```

Result: expected rejection PASS when no real provider credential or accepted
endpoint exists.

Evidence:

```text
Real translation provider is not configured.
Configure one of these before launching real translation.
```

The real packaged trial path did not silently fall back to fake provider mode.

## Direct Packaged Executable Smoke

Commands:

```cmd
dist\SnapLex\SnapLex.exe --version
dist\SnapLex\SnapLex.exe --no-gui
set SNAPLEX_APP_DATA_DIR=%CD%\snaplex-smoke-data\p11-packaged&& dist\SnapLex\SnapLex.exe --smoke-package
```

Results:

- `--version`: PASS, `SnapLex 0.1.0`.
- `--no-gui`: PASS, PySide6 bootstrap OK.
- `--smoke-package`: PASS with fake-provider clipboard, fake screen
  capture/OCR, settings persistence, and history clear checks.

## Artifact Boundary

The package executable and smoke app data were pre-existing or generated local
artifacts under ignored paths. P11 does not commit `build\`, `dist\`,
`snaplex-smoke-data\`, package binaries, screenshots, local config/history,
logs, `.env`, keyring exports, OCR caches, or provider secrets.
