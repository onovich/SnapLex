# P6 Release Checklist

Date: 2026-06-22
Phase: P6 Packaging and Release Readiness

Use this checklist before treating a local Windows package as an MVP release
candidate.

## Preflight

- Confirm `git status --short --branch` is clean except ignored generated files.
- Confirm no `.env`, provider API key values, local config/history files,
  screenshots, OCR model caches, packaged binaries, `build\`, or `dist\` are
  staged.
- Install release tooling:

```powershell
python -m pip install -e ".[dev,gui,package]"
```

## Source Validation

```powershell
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
git diff --check
python -m snaplex --version
python -m snaplex --no-gui
```

Expected result:

- Validation exits with code 0.
- Pytest reports the current suite passing.
- Version prints `SnapLex 0.1.0`.
- No-GUI bootstrap prints a PySide6 availability message.

## Package Build

```powershell
python scripts\package_windows.py --variant base
```

Expected artifact:

```text
dist\SnapLex\SnapLex.exe
```

Optional variants:

```powershell
python scripts\package_windows.py --variant capture
python scripts\package_windows.py --variant ocr
python scripts\package_windows.py --variant full
```

The `base` variant is the release-smoke default. Optional variants require the
matching local dependencies and may be larger or slower because of capture/OCR
libraries. Do not commit any generated artifact.

## Packaged Smoke

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexPackageSmoke"
.\dist\SnapLex\SnapLex.exe --version
.\dist\SnapLex\SnapLex.exe --no-gui
.\dist\SnapLex\SnapLex.exe --smoke-package
```

Expected result:

- Packaged version/no-GUI commands exit with code 0.
- Packaged workflow smoke reports settings persistence PASS.
- Packaged workflow smoke reports clipboard translation PASS.
- Packaged workflow smoke reports fake screen capture/OCR translation PASS.
- Packaged workflow smoke reports history record/list/delete/clear PASS.

## Manual GUI Smoke

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexPackageSmokeGui"
.\dist\SnapLex\SnapLex.exe
```

Checklist:

- Window titled `SnapLex` opens and can be closed cleanly.
- `Translate Clipboard` works with copied text and fake provider defaults.
- `Settings` can save provider/history preferences.
- `History` can show, copy, delete, and clear entries after history is enabled.
- `Translate Screen` can run the packaged default fake capture/OCR path.

## Known Limitations

- The default package uses fake capture/OCR for deterministic release smoke.
- Real `mss` and PaddleOCR smoke is optional and variant-dependent.
- The package does not bundle PaddleOCR model caches.
- Real provider smoke depends on local environment variables and may require
  network access; it is not part of automated P6 validation.
- Global hotkeys, browser extension, AI summary, cloud sync/accounts, and
  keychain integration are out of P6 scope.

## Cleanup

```powershell
Remove-Item -Recurse -Force build,dist
Remove-Item -Recurse -Force D:\Temp\SnapLexPackageSmoke,D:\Temp\SnapLexPackageSmokeGui
```

Verify cleanup with:

```powershell
git status --short --branch --ignored
```

Generated files may remain ignored locally, but none should be staged or
committed.
