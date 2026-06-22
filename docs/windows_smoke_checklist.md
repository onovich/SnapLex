# Windows Smoke Checklist

Use this checklist after automated validation passes.

Latest P2 smoke evidence is recorded in `docs/p2_windows_smoke_evidence.md`.
Latest P3 smoke evidence is recorded in `docs/p3_windows_smoke_evidence.md`.
P4 provider smoke planning is recorded in `docs/p4_provider_hardening_goal_guide.md`.
P5 settings/history behavior is recorded in `docs/p5_final_validation_report.md`
and `docs/p5_privacy_and_storage.md`.
P6 packaging smoke planning is recorded in `docs/p6_packaging_release_goal_guide.md`.

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

## P3 Screen Translation Smoke

Install optional GUI and capture dependencies when exercising the visible real
capture path:

```powershell
python -m pip install -e ".[gui]"
python -m pip install -e ".[capture]"
python -m snaplex
```

Single-monitor visible path:

1. Select `Translate Screen`.
2. Drag a non-empty screen region in the overlay.
3. Release the mouse to confirm the region.
4. Confirm the result view shows OCR source text and translated text.
5. Select `Copy Result` and verify the clipboard receives the translated text.
6. Select `Retry` and confirm the same selected region is reused.
7. Select `Close Result` and confirm the shell returns to `Ready`.

Cancel path:

1. Select `Translate Screen`.
2. Press `Esc` in the overlay.

Expected result:

- Status shows `Screen selection cancelled`.
- No capture, OCR, or translation result is copied.

Failure paths to smoke with fake/injected services:

- Empty OCR result shows `No screen text found`.
- OCR failure shows a user-friendly error.
- Capture failure shows a user-friendly error.
- Translation provider failure shows a user-friendly error.

Current limitation:

- P3 records single-monitor as the first accepted real-capture smoke path.
- DPI scaling and multi-monitor coordinate conversion need visible Windows smoke
  before packaging.

## No-GUI Dependency Fallback

In an environment without PySide6, run:

```powershell
python -m snaplex
```

Expected result:

- The command prints the PySide6 install hint.
- The command exits with code 0.

## P4 Provider Configuration Smoke

After P4 is implemented, provider smoke should use local environment variables
or ignored local configuration only. Automated P4 tests must still use mocked
HTTP and must not call external services.

Expected result:

- Fake provider remains the default no-credential path.
- Missing LibreTranslate/OpenAI/DeepL credentials produce controlled provider
  errors or provider omission, not app bootstrap crashes.
- A real-provider smoke is recorded only when local credentials or endpoints are
  already available.

## P5 Settings And History Smoke

Use a local test data directory when exercising settings/history manually:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexSmoke"
python -m snaplex
```

Settings path:

1. Select `Settings`.
2. Change source/target language or provider order.
3. Toggle `History` and set `History Max`.
4. Save, close the app, relaunch, and reopen `Settings`.

History path:

1. Enable history in `Settings`.
2. Translate clipboard text.
3. Select `History`.
4. Confirm the recent translation is listed.
5. Select the entry and use `Copy`.
6. Paste into a scratch editor and confirm the copied text matches the result.
7. Delete the entry.
8. Translate another item, reopen `History`, and use `Clear`.

Expected result:

- Changing provider/language/history settings persists across app restart.
- Recent translation history can be listed, copied, deleted, and cleared when
  history is enabled.
- Disabling history prevents future successful translations from being stored.
- No actual provider API key values are persisted.

## P6 Packaging Smoke

After P6 is implemented, run the documented packaging command and smoke the
generated artifact with fake provider defaults and a test app data directory.

Expected result:

- The package builds or records a narrow, reproducible blocker.
- Generated `build/`, `dist/`, binaries, screenshots, OCR model caches, and
  local config/history files remain uncommitted.
- Packaged launch, clipboard translation, settings persistence, history clear,
  and available screen/capture paths are smoked or explicitly documented.

## Deferred To Later Phases

- Global clipboard hotkey handling.
- Browser extension and AI summary expansion.
