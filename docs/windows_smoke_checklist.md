# Windows Smoke Checklist

Use this checklist after automated validation passes.

Latest P2 smoke evidence is recorded in `docs/p2_windows_smoke_evidence.md`.

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

## P2 Clipboard Translation Smoke

With the GUI shell running:

1. Copy `hello` into the Windows clipboard.
2. Select `Translate Clipboard`.
3. Confirm the status changes away from `Ready` and then shows a result.
4. Confirm the source text shows `hello`.
5. Confirm the translated text is visible.
6. Select `Copy Result`.
7. Paste into a scratch editor and confirm the copied text matches the visible result.
8. Select `Retry` and confirm the result refreshes through the same source text.
9. Select `Close Result` and confirm the shell returns to `Ready`.

Expected result:

- The app uses the clipboard service and P1 translation pipeline.
- The fake provider path works without network access.
- Empty clipboard, provider failure, timeout, unknown provider, and fallback
  exhaustion are represented as user-friendly result states when exercised with
  fake/injected test paths.

## P2 Hotkey Scope

Global Windows hotkey support is deferred in P2. See
`docs/p2_hotkey_decision.md`.

Expected result:

- P2 smoke uses the manual `Translate Clipboard` button.
- No global hotkey is required for P2 acceptance.

## No-GUI Dependency Fallback

In an environment without PySide6, run:

```powershell
python -m snaplex
```

Expected result:

- The command prints the PySide6 install hint.
- The command exits with code 0.

## Not Expected In P2

- Real screen-region capture.
- Real OCR extraction.
- Global clipboard hotkey handling.
- Network translation providers.
- Windows packaging.
