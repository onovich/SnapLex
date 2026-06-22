# Windows Smoke Checklist

Use this checklist after automated validation passes.

Latest P2 smoke evidence is recorded in `docs/p2_windows_smoke_evidence.md`.
Latest P3 smoke evidence is recorded in `docs/p3_windows_smoke_evidence.md`.
P4 provider smoke planning is recorded in `docs/p4_provider_hardening_goal_guide.md`.
P5 settings/history behavior is recorded in `docs/p5_final_validation_report.md`
and `docs/p5_privacy_and_storage.md`.
P6 packaging smoke evidence is recorded in `docs/p6_packaging_smoke_evidence.md`.
P7 expansion planning is recorded in `docs/p7_expansion_track_goal_guide.md`,
`docs/p7_final_validation_report.md`, and `docs/p0_p7_final_report.md`.

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

Install packaging dependencies:

```powershell
python -m pip install -e ".[gui,package]"
```

Build the deterministic base package:

```powershell
python scripts\package_windows.py --variant base
```

Run packaged bootstrap and workflow smoke with a local test app data directory:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexPackageSmoke"
.\dist\SnapLex\SnapLex.exe --version
.\dist\SnapLex\SnapLex.exe --no-gui
.\dist\SnapLex\SnapLex.exe --smoke-package
```

Optional capture/OCR variants are explicit:

```powershell
python scripts\package_windows.py --variant capture
python scripts\package_windows.py --variant ocr
python scripts\package_windows.py --variant full
```

Expected result:

- The package builds under `dist\SnapLex`.
- Packaged version/no-GUI smoke exits with code 0.
- Packaged workflow smoke reports fake-provider settings, clipboard
  translation, fake screen capture/OCR translation, and history clear PASS.
- Generated `build/`, `dist/`, binaries, screenshots, OCR model caches, and
  local config/history files remain uncommitted.
- Real `mss` and PaddleOCR smoke is manual and variant-dependent. The default
  base package intentionally avoids bundling OCR model caches or requiring
  provider credentials, network, model downloads, or screen permissions.

## Deferred To Later Phases

- Global clipboard hotkey handling.
- Production browser extension implementation.
- Real AI summary service integration.

## P7 Expansion Planning Validation

P7 is design-first from the accepted P6 release baseline. If no runtime code is
introduced, validation remains documentation, link, boundary, and no-regression
focused:

```powershell
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
git diff --check
python -m snaplex --version
python -m snaplex --no-gui
python scripts\package_windows.py --dry-run --variant base
```

Expected result:

- Existing MVP validation remains green.
- P7 docs clearly separate multilingual UX, AI summary, and browser extension
  bridge work from the released MVP runtime.
- P7 docs link/index checks cover requirements, multilingual UX, AI summary,
  browser bridge, roadmap, P7 final validation, and P0-P7 final report.
- No generated packages, screenshots, local data, provider secrets, or new
  network-dependent validation are committed.
