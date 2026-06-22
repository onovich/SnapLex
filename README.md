# SnapLex

SnapLex is a desktop floating utility for instant screen text capture and translation.
The MVP is planned as a Python + PySide6 application with two primary workflows:

- Screen translation: capture a selected region, run OCR, translate the extracted text, then show the result in a popup.
- Text translation: use a hotkey and clipboard pipeline to translate selected text quickly.

The current project source of truth lives in:

- `docs/SnapLex_Product_Design.pdf`
- `docs/SnapLex_Technical_Architecture.pdf`
- `docs/development_plan.md`
- `docs/phase_plan.md`
- `docs/p0_p7_goal_mode_execution_guide.md`
- `docs/p0_repository_baseline_goal_guide.md`
- `docs/p1_core_pipeline_goal_guide.md`
- `docs/p2_clipboard_translation_goal_guide.md`
- `docs/p0_to_p1_handoff.md`
- `docs/p1_to_p2_handoff.md`
- `docs/p2_final_validation_report.md`
- `docs/p2_to_p3_handoff.md`
- `docs/p3_screen_capture_ocr_goal_guide.md`
- `docs/p3_final_validation_report.md`
- `docs/p3_to_p4_handoff.md`
- `docs/p4_provider_hardening_goal_guide.md`
- `docs/p4_provider_configuration.md`
- `docs/p4_final_validation_report.md`
- `docs/p4_to_p5_handoff.md`
- `docs/p5_history_persistence_settings_goal_guide.md`
- `docs/p5_privacy_and_storage.md`
- `docs/p5_final_validation_report.md`
- `docs/p5_to_p6_handoff.md`
- `docs/p6_packaging_release_goal_guide.md`
- `docs/p6_final_validation_report.md`
- `docs/p6_to_p7_handoff.md`
- `docs/p6_packaging_smoke_evidence.md`
- `docs/p6_release_checklist.md`
- `docs/p7_expansion_track_goal_guide.md`
- `docs/p3_windows_smoke_evidence.md`
- `docs/p3_capture_notes.md`
- `docs/p3_ocr_notes.md`
- `docs/p3_lazy_loading_notes.md`
- `docs/p2_hotkey_decision.md`
- `docs/p2_windows_smoke_evidence.md`
- `docs/p1_todo.md`
- `docs/p2_todo.md`
- `docs/p3_todo.md`
- `docs/windows_smoke_checklist.md`
- `docs/p0_final_validation_report.md`
- `docs/p4_todo.md`
- `docs/p5_todo.md`
- `docs/p6_todo.md`
- `docs/p7_todo.md`

## Planned Stack

- Python + PySide6 for the desktop shell and floating UI.
- `mss` or `pyautogui` for screen capture.
- PaddleOCR first, with a Tesseract-compatible service boundary.
- Pluggable translation providers for LibreTranslate, OpenAI, DeepL, or local fallback providers.
- PyInstaller for Windows packaging.

## Current Status

SnapLex has accepted P0 through P6 and P7 is ready for expansion-track execution. The app now has manual clipboard and screen
translation actions, capture/OCR service boundaries, optional lazy real
capture/OCR adapters, real provider adapters for LibreTranslate/OpenAI/DeepL,
mocked HTTP tests, fake offline defaults, persisted settings, optional recent
translation history, shared result states, a PyInstaller spec, and packaged
release smoke commands.

The current implementation phase is P7 expansion track. Start from
`docs/p7_expansion_track_goal_guide.md`, `docs/p7_todo.md`,
`docs/p6_final_validation_report.md`, and `docs/p6_to_p7_handoff.md`.

## Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Install the optional desktop dependency when you want to launch the PySide6 shell:

```powershell
python -m pip install -e ".[gui]"
```

Install optional real capture/OCR dependencies only when you want to exercise
those backends:

```powershell
python -m pip install -e ".[capture]"
python -m pip install -e ".[ocr]"
```

Install the optional packaging toolchain when building a local Windows package:

```powershell
python -m pip install -e ".[gui,package]"
```

## Run

Bootstrap check without starting the desktop shell:

```powershell
python -m snaplex --no-gui
```

Launch the desktop shell after installing the GUI extra:

```powershell
python -m snaplex
```

Clipboard MVP flow:

1. Copy text into the Windows clipboard.
2. Run `python -m snaplex`.
3. Select `Translate Clipboard`.
4. Review the source, translated text, provider, or error state.
5. Use `Copy Result`, `Retry`, or `Close Result`.

Screen MVP flow:

1. Run `python -m snaplex`.
2. Select `Translate Screen`.
3. Drag a non-empty screen region in the overlay, or press `Esc` to cancel.
4. Review the OCR source, translated text, provider, or error state.
5. Use `Copy Result`, `Retry`, or `Close Result`.

The same entry point is exposed as a console script after editable install:

```powershell
snaplex --no-gui
```

## Development Checks

Quick bootstrap checks:

```powershell
python -m compileall snaplex
python -m snaplex --version
python -m snaplex --no-gui
```

Full local validation now runs through the project ops wrapper:

```powershell
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
```

The configured validation sequence is:

- `python -m ruff check .`
- `python -m ruff format --check .`
- `python -m mypy snaplex`
- `python -m compileall snaplex`
- `python -m pytest`

## Packaging

Build the deterministic Windows smoke package:

```powershell
python scripts\package_windows.py --variant base
```

Preview the PyInstaller command without building:

```powershell
python scripts\package_windows.py --dry-run --variant base
```

Smoke the packaged executable with fake provider defaults and a local test data
directory:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexPackageSmoke"
.\dist\SnapLex\SnapLex.exe --version
.\dist\SnapLex\SnapLex.exe --no-gui
.\dist\SnapLex\SnapLex.exe --smoke-package
```

The default `base` package includes the GUI runtime and deterministic fake
capture/OCR smoke path. Optional variants can include `mss` and/or PaddleOCR
modules when those dependencies are installed:

```powershell
python scripts\package_windows.py --variant capture
python scripts\package_windows.py --variant ocr
python scripts\package_windows.py --variant full
```

Generated `build\`, `dist\`, local smoke data, OCR model caches, screenshots,
`.env`, provider secrets, and packaged binaries must remain uncommitted. See
`packaging\README.md`, `docs\p6_packaging_smoke_evidence.md`, and
`docs\p6_release_checklist.md`.

## Package Layout

```text
snaplex/
  app.py                 # application bootstrap
  ui/                    # PySide6 shell and future widgets
  services/              # capture, OCR, clipboard, and translation boundaries
  providers/             # translation provider contracts and adapters
  storage/               # configuration and future persistence boundaries
```

Current local fakes:

- `FakeTranslationProvider`
- `FakeOcrService`
- `FakeCaptureService`
- `InMemoryClipboardService`
- `InMemoryConfigStore`
- `InMemoryTranslationCache`

## Core Translation Pipeline

P1 provides a reusable service boundary for later clipboard and OCR flows:

```python
from snaplex.services import create_default_translation_pipeline

pipeline = create_default_translation_pipeline()
result = pipeline.translate_text("hello", target_lang="es")
```

For UI callers, use the async-friendly boundary:

```python
result = await pipeline.translate_text_async("hello", target_lang="es")
```

Pipeline behavior includes normalization, config-driven provider selection,
fallback order, in-memory cache lookup/write, and expected error mapping.

## Clipboard Translation MVP

P2 adds the first user-facing vertical slice:

- `snaplex/ui/clipboard_presenter.py` owns clipboard translation presentation state.
- `snaplex/ui/app_shell.py` exposes the always-on-top PySide6 shell and result view.
- `snaplex/services/clipboard_service.py` contains the in-memory and Qt clipboard adapters.
- UI calls `TranslationPipeline.translate_text_async(...)`; it does not call providers directly.
- Tests cover clipboard service behavior, presenter states, pipeline integration, retry, copy,
  empty clipboard, timeout, provider failure, fallback exhaustion, unknown provider,
  unsupported language, stale result, and unexpected failure states.

Global Windows hotkey support is deferred for a later phase. P2 accepts the
manual `Translate Clipboard` button as the stable trigger path.

## Screen Capture And OCR MVP

P3 adds the first screen-translation vertical slice:

- `snaplex/ui/region_selector.py` provides a minimal Qt region selector plus
  testable selection presenter.
- `snaplex/services/capture_service.py` contains fake capture and lazy optional
  `MssCaptureService`.
- `snaplex/services/ocr_service.py` contains fake OCR scenarios and lazy optional
  `PaddleOcrService`.
- `snaplex/services/screen_translation_service.py` orchestrates
  capture -> OCR -> `TranslationPipeline`.
- `snaplex/ui/screen_presenter.py` maps screen translation results and failures
  into the shared result view.
- Tests cover fake capture/OCR integration, cancel, invalid region, capture
  failure, OCR unavailable/failure, empty OCR result, translation failure, retry,
  copy, close, and optional dependency lazy-loading.

## Provider Configuration

P4 adds real provider adapters for LibreTranslate, OpenAI, and DeepL behind the
existing `TranslationPipeline`. Fake provider mode remains the default. To select
a real provider locally, set environment variables before launching the GUI:

```powershell
$env:SNAPLEX_PROVIDER = "libretranslate"
$env:SNAPLEX_PROVIDER_ORDER = "libretranslate,fake"
python -m snaplex
```

Use `.env.example` and `docs/p4_provider_configuration.md` for provider-specific
base URLs, API-key env var names, timeout, retry, OpenAI model, and DeepL model
type settings. Do not commit real API keys or local `.env` files.

## Settings And History

P5 adds local JSON settings and optional recent translation history. By default,
SnapLex uses `%APPDATA%\SnapLex` on Windows, or a home-directory fallback. For
tests and local smoke, override the data path:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexSmoke"
python -m snaplex
```

The app stores provider selection/order, language defaults, provider endpoints,
API-key environment variable names, timeout/retry settings, model options,
history preferences, and UI preferences. It does not store actual provider API
key values.

History is disabled by default. When enabled in `Settings`, successful clipboard
and screen translations store source text, translated text, provider/language
metadata, flow, timestamp, and entry id. The `History` dialog can copy, delete,
and clear entries. See `docs/p5_privacy_and_storage.md`.

## Current Boundaries

The current implementation intentionally does not include global hotkeys,
browser extension, AI summary, cloud sync, accounts, or keychain integration.
Real capture/OCR adapters and real translation providers are present but
optional; fake mode remains the deterministic default for automated tests and
packaged release smoke. Later phases are staged in `docs/phase_plan.md`.
