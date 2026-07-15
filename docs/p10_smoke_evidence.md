# P10 Smoke Evidence

Date: 2026-07-15
Phase: P10 Secure Credential And Account Strategy
Status: P8/P9/package/no-secret preservation smoke passed

This smoke pass validates that P10 credential work preserved the accepted P8
real/fake provider guardrails, P9 GUI smoke path, no-GUI bootstrap, package
dry-run, and no-secret/no-artifact repository boundaries.

## Commands

- `python -m snaplex --version`: PASS, `SnapLex 0.1.0`.
- `python -m snaplex --no-gui`: PASS, PySide6 bootstrap OK.
- `python scripts\package_windows.py --dry-run --variant base`: PASS.
- `cmd /c StartTrial.cmd --no-gui`: expected rejection PASS when no real
  provider credential or endpoint is configured.
- `cmd /c StartFakeTrial.cmd --no-gui`: PASS, deterministic fake smoke path.
- `cmd /c SmokeTrial.cmd`: PASS. Because `dist\SnapLex\SnapLex.exe` existed
  locally, this also ran packaged `--version`, packaged `--no-gui`, and
  packaged `--smoke-package`.
- `python scripts\p9_gui_smoke.py`: PASS, 7 offscreen screenshots written under
  ignored `snaplex-smoke-data\p9-screenshots`.
- `cmd /c "set SNAPLEX_OPENAI_API_KEY=dummy-key&& StartTrial.cmd --no-gui"`:
  PASS. Trial readiness selected OpenAI and did not fall back to fake. The
  placeholder key value was not printed.

## Guardrail Results

Missing real-provider setup still fails closed:

```text
Real translation provider is not configured.
```

Fake smoke remains visibly fake and deterministic:

```text
Provider: fake smoke mode; this is not real translation.
SnapLex bootstrap OK (PySide6 available).
```

Real-provider readiness with a local process environment variable reports only
source/status text:

```text
Real provider ready: OpenAI
- OpenAI: Ready to test - SNAPLEX_OPENAI_API_KEY is set in this process. The key value is not stored.
```

Package dry-run remains the deterministic base variant:

```text
SNAPLEX_PACKAGE_VARIANT=base
C:\Python314\python.exe -m PyInstaller --distpath D:\ToolProjects\SnapLex\dist --workpath D:\ToolProjects\SnapLex\build\pyinstaller --clean --noconfirm D:\ToolProjects\SnapLex\packaging\snaplex.spec
```

Packaged workflow smoke stayed on fake provider and local app data:

```text
SnapLex packaged workflow smoke PASS
- app data: D:\ToolProjects\SnapLex\snaplex-smoke-data\trial-smoke
- settings persistence: fake provider, history enabled
- clipboard translation: hello -> hello [en]
- screen fake capture/OCR translation: screen hello -> screen hello [en]
- history record/list/delete/clear: PASS
```

## Boundary Scan

- `git status --short --branch`: clean at `main...origin/main` before evidence
  docs were edited.
- `git ls-files -- build dist snaplex-smoke-data .env .pytest_cache`: no tracked
  files.
- Secret pattern scan for provider-key forms and the dummy smoke value returned
  only placeholder setup text in `RequireRealProvider.cmd`.

No real provider secrets, `.env` files, local config/history files, generated
package outputs, screenshot artifacts, OCR model caches, keyring exports, or
smoke data were tracked.

## Limitations

This was deterministic no-network validation. It did not call OpenAI, DeepL, or
LibreTranslate and did not require a real OS keyring. Manual Windows Credential
Locker smoke with a throwaway credential remains a recommended P11 task before
shipping keyring support in a distributable binary.
