# P2 Windows Smoke Evidence

Date: 2026-06-22
Phase: P2 Clipboard Translation MVP
Environment: Windows PowerShell, Python 3.14.3

## Dependency State

- `python -m pip install -e ".[gui]"`: PASS
- `python -c "import PySide6; print(PySide6.__version__)"`: `6.11.1`

## Automated Validation

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`: PASS
- `python -m pytest`: 68 passed
- `python -m snaplex --version`: `SnapLex 0.1.0`
- `python -m snaplex --no-gui`: `SnapLex bootstrap OK (PySide6 available).`

## GUI Entry Smoke

Command:

```powershell
$env:QT_QPA_PLATFORM = 'offscreen'
$p = Start-Process -FilePath python -ArgumentList '-m','snaplex' -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 2
if ($p.HasExited) { exit $p.ExitCode } else { Stop-Process -Id $p.Id }
```

Result: PASS. The `python -m snaplex` GUI entry started and was stopped after
the smoke window.

## Clipboard Translation Flow Smoke

Smoke method: PySide6 offscreen launch using `launch_gui(...)` with
`InMemoryClipboardService("hello")` and the default fake-provider P1 pipeline.

Verified:

- SnapLex window initializes through the GUI shell.
- `Translate Clipboard` button triggers the clipboard translation flow.
- Source label shows `hello`.
- Result label shows `hello [en]`.
- `Copy Result` becomes enabled after success.
- Selecting `Copy Result` writes `hello [en]` back to the clipboard service.
- `Retry` becomes enabled after success.
- `Close Result` resets the shell to `Ready`.

Result: PASS.

## P2 Hotkey Note

Global hotkey support is intentionally not part of the P2 acceptance path. The
accepted P2 trigger is the visible `Translate Clipboard` action. See
`docs/p2_hotkey_decision.md`.

