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

Preview the exact PyInstaller command without building:

```powershell
python scripts\package_windows.py --dry-run
```

Generated output stays under `build\` and `dist\`. Do not commit those folders,
packaged executables, local smoke data, provider secrets, OCR model caches, or
screenshots.
