# SnapLex Windows Packaging

P6 uses PyInstaller for the Windows MVP package. Install the packaging toolchain
without enabling heavyweight optional OCR dependencies:

```powershell
python -m pip install -e ".[gui,package]"
```

Build a console-mode package for repeatable launch smoke:

```powershell
python scripts\package_windows.py
```

The default command uses the tracked spec at `packaging\snaplex.spec`. Use
`--no-spec` only when diagnosing PyInstaller option changes locally.

The tracked spec supports dependency variants:

- `base`: GUI package with fake/offline capture and OCR services for smoke.
- `capture`: additionally includes optional `mss` modules when installed.
- `ocr`: additionally includes optional `paddleocr` modules when installed.
- `full`: includes both optional capture and OCR module families when installed.

Use variants explicitly:

```powershell
python scripts\package_windows.py --variant capture
python scripts\package_windows.py --variant full
```

Preview the exact PyInstaller command without building:

```powershell
python scripts\package_windows.py --dry-run
```

The `base` variant is the deterministic release-smoke path. It does not package
PaddleOCR model caches and does not require real provider credentials. Generated
output stays under `build\` and `dist\`. Do not commit those folders, packaged
executables, local smoke data, provider secrets, OCR model caches, or screenshots.

## Smoke

Run packaged smoke with an explicit local app data directory:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexPackageSmoke"
.\dist\SnapLex\SnapLex.exe --version
.\dist\SnapLex\SnapLex.exe --no-gui
.\dist\SnapLex\SnapLex.exe --smoke-package
```

`--smoke-package` runs inside the packaged executable and checks settings
persistence, fake-provider clipboard translation, fake capture/OCR screen
translation, history record/list/delete/clear, and local data path containment.

## Troubleshooting

- `No module named PyInstaller`: run `python -m pip install -e ".[package]"`.
- PySide6 import or Qt plugin failures: rebuild after installing
  `python -m pip install -e ".[gui,package]"`.
- Missing `mss` or PaddleOCR in optional variants: install `.[capture]`,
  `.[ocr]`, or both before using `--variant capture`, `--variant ocr`, or
  `--variant full`.
- Provider credential errors: use fake provider smoke first. Real provider
  smoke depends on local environment variables and must not put key values into
  config files, docs, logs, or package resources.
- History/config smoke writes to `SNAPLEX_APP_DATA_DIR`. Set it to a temporary
  directory before running package smoke.

## Cleanup

```powershell
Remove-Item -Recurse -Force build,dist
Remove-Item -Recurse -Force D:\Temp\SnapLexPackageSmoke
```

Only delete directories you explicitly created for local smoke.
