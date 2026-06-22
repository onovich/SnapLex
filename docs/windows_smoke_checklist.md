# Windows Smoke Checklist

Use this checklist after automated validation passes.

## Automated Precheck

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
```

Expected result:

- Validation exits with code 0.
- Pytest reports the current unit test suite passing.

## Bootstrap Smoke

```powershell
python -m snaplex --version
python -m snaplex --no-gui
snaplex --no-gui
```

Expected result:

- Version command prints `SnapLex 0.1.0`.
- No-GUI commands print a bootstrap OK message and exit with code 0.

## GUI Shell Smoke

Install the optional GUI dependency:

```powershell
python -m pip install -e ".[gui]"
python -m snaplex
```

Expected result:

- A small window titled `SnapLex` opens.
- The window displays `SnapLex` and `Ready`.
- The window is configured as always on top.
- Closing the window exits the process cleanly.

## No-GUI Dependency Fallback

In an environment without PySide6, run:

```powershell
python -m snaplex
```

Expected result:

- The command prints the PySide6 install hint.
- The command exits with code 0.

## Not Expected In P0

- Real screen-region capture.
- Real OCR extraction.
- Clipboard hotkey handling.
- Network translation providers.
- Translation popup UX.
- Windows packaging.
