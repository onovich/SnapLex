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
P8 provider setup and real translation UX planning is recorded in
`docs/p8_provider_setup_real_translation_goal_guide.md`,
`docs/p7_to_p8_handoff.md`, `docs/p8_final_validation_report.md`, and
`docs/p8_real_provider_trial_notes.md`.
P9 UI/UX polish planning and executor evidence are recorded in
`docs/p9_apple_inspired_ui_ux_goal_guide.md`,
`docs/p9_visual_smoke_evidence.md`, and
`docs/p9_final_validation_report.md`.
P10 secure credential/account strategy planning is recorded in
`docs/p10_secure_credential_account_strategy_goal_guide.md`,
`docs/p10_credential_strategy_decisions.md`,
`docs/p10_secure_storage_notes.md`, `docs/p10_account_strategy.md`,
`docs/p10_smoke_evidence.md`, `docs/p10_final_validation_report.md`,
`docs/p10_to_p11_handoff.md`, and `docs/p10_todo.md`.
P11 trial release hardening planning is recorded in
`docs/p11_trial_release_hardening_goal_guide.md` and `docs/p11_todo.md`.

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

## P8 Provider Setup And Real Trial Smoke

After P8 is implemented, smoke the user-facing provider setup path before
broader trial distribution:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexP8Smoke"
python -m snaplex
```

Expected result:

- Settings exposes provider setup for fake, LibreTranslate, OpenAI, and DeepL.
- Provider readiness shows whether required environment variables or endpoints
  are configured without displaying raw secrets.
- `Test Connection` reports success/failure through user-friendly states and
  does not expose credential values.
- Fake provider mode is clearly labeled as fake smoke/dev behavior.
- The main result view shows provider identity, language pair, source text,
  translated text, loading, empty, and error states with readable hierarchy.
- Results produced by the fake provider show a visible warning that fake output
  is deterministic placeholder text, not real translation.

Real trial command behavior:

```powershell
.\StartTrial.cmd --no-gui
.\StartFakeTrial.cmd --no-gui
```

Expected result:

- `StartTrial.cmd` rejects missing real provider configuration with a clear
  message.
- `StartFakeTrial.cmd` remains the deterministic fake smoke path.
- Real trial scripts must not set provider order to `fake` when no real provider
  is configured.
- Automated validation does not require real provider credentials or network.

P8 final validation additionally requires:

```powershell
cmd /c SmokeTrial.cmd
cmd /c StartPackagedFakeTrial.cmd --no-gui
```

Expected result:

- SmokeTrial passes source bootstrap, package dry-run, and packaged fake
  workflow smoke when a packaged executable exists.
- Packaged fake trial no-GUI remains deterministic and labels fake smoke mode.

## P9 Apple-Inspired UI/UX Polish Smoke

After P9 is implemented, smoke the user-facing desktop quality before broader
trial distribution:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexP9Smoke"
python -m snaplex
```

Expected result:

- Main shell has clear primary actions, secondary actions, result states, and
  status hierarchy.
- Settings provider setup is scannable and keyboard-accessible.
- History empty/list/long-entry states remain readable and operable.
- Fake provider output remains visibly labeled as fake smoke/dev mode.
- Long source text, long translation text, provider labels, errors, and history
  entries do not overflow or overlap at common small window sizes.
- Focus order is predictable in shell, Settings, and History.

P9 final validation additionally requires:

```powershell
python scripts\p9_gui_smoke.py
```

- PySide6 offscreen GUI smoke for shell, Settings, History, and result states.
- Screenshot-backed smoke with local artifacts kept under ignored paths.
- Keyboard/focus smoke.
- Long-text and small-window smoke.
- Artifact scan proving screenshots and smoke outputs are not committed.

Expected result:

- The P9 GUI smoke helper reports PASS.
- Screenshots are written under `snaplex-smoke-data\p9-screenshots`.
- `snaplex-smoke-data`, screenshots, local app data, build outputs, `.env`, and
  provider secrets remain untracked.
- If the offscreen environment has no fonts, screenshot text may render as
  square glyphs; visible Windows smoke should still be run before broader trial
  distribution.

## P10 Secure Credential And Account Strategy Smoke

After P10 is implemented, smoke credential setup without using real provider
secrets unless the user explicitly approves a real-provider trial:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexP10Smoke"
python -m snaplex
```

Expected result:

- Settings shows credential source and readiness without displaying secret
  values.
- Environment-variable provider setup still works for existing P8/P9 users.
- Local secure credential save/delete, if implemented, uses password-style
  transient input and clears the field after save or test.
- Unsupported or unavailable keyring backends produce a clear user-facing state
  without crashing app launch, no-GUI bootstrap, or package dry-run.
- `Test Connection` resolves credentials through service boundaries and never
  echoes raw values in status text, logs, screenshots, config, or history.
- `StartTrial.cmd --no-gui` still rejects missing real provider configuration
  clearly when no accepted credential source is present.
- `python -m snaplex --check-real-provider` reports real-provider readiness
  through the credential service without performing a network call or printing
  a secret value.
- `StartFakeTrial.cmd --no-gui` remains deterministic fake smoke/dev mode.

Optional manual Windows Credential Locker smoke:

1. Use only a throwaway fake secret value.
2. Save the credential through Settings.
3. Close and relaunch SnapLex with the same `SNAPLEX_APP_DATA_DIR`.
4. Confirm readiness reports the credential reference, not the secret value.
5. Delete the credential and confirm readiness returns to missing or
   unconfigured state.

P10 final validation should additionally prove generated keyring exports, local
config/history, `.env`, screenshots, logs, package outputs, and provider secrets
remain untracked and uncommitted.

## P11 Trial Release Hardening Smoke

P11 is the release-hardening pass before broader private trial distribution.
Run visible desktop smoke when the environment supports it:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexP11VisibleSmoke"
python -m snaplex
```

Expected result:

- Shell, Settings, History, result states, long text, fake warnings, and focus
  outlines are readable with normal Windows desktop fonts.
- Real trial paths fail closed when no real provider or accepted credential
  source is configured.
- Fake trial paths remain deterministic and visibly fake.
- Credential source/readiness controls do not echo raw secret values.
- Screenshots or notes from visible smoke remain local ignored artifacts.

Manual keyring smoke should use only a throwaway fake secret:

1. Install optional credential support when needed:
   `python -m pip install -e ".[gui,credentials]"`.
2. Select keyring/local secure credential source in Settings.
3. Save the throwaway value.
4. Confirm readiness reports a non-secret keyring reference.
5. Relaunch SnapLex with the same local app data directory.
6. Confirm readiness persists without displaying the value.
7. Delete the credential and confirm readiness returns to missing.

Packaging hardening should decide whether keyring support is included in the
base package, an explicit credential-capable variant, or a manual-install path
for the private trial. Base package fake smoke must remain deterministic.

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
