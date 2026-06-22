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
- `docs/p1_todo.md`
- `docs/p2_todo.md`
- `docs/windows_smoke_checklist.md`
- `docs/p0_final_validation_report.md`

## Planned Stack

- Python + PySide6 for the desktop shell and floating UI.
- `mss` or `pyautogui` for screen capture.
- PaddleOCR first, with a Tesseract-compatible service boundary.
- Pluggable translation providers for LibreTranslate, OpenAI, DeepL, or local fallback providers.
- PyInstaller for Windows packaging.

## Current Status

SnapLex has an accepted P0 repository baseline and an accepted P1 non-UI
translation pipeline foundation. The current pipeline works without UI, network,
OCR models, or API credentials. The next executable guide is
`docs/p2_clipboard_translation_goal_guide.md`.

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

## Run

Bootstrap check without starting the desktop shell:

```powershell
python -m snaplex --no-gui
```

Launch the desktop shell after installing the GUI extra:

```powershell
python -m snaplex
```

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

## P0 Boundaries

P0 intentionally does not include real OCR, screen capture, global hotkeys, network
translation providers, persistent history, or Windows packaging. Those are staged
for later phases in `docs/phase_plan.md`.
