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
