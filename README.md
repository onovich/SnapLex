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

## Planned Stack

- Python + PySide6 for the desktop shell and floating UI.
- `mss` or `pyautogui` for screen capture.
- PaddleOCR first, with a Tesseract-compatible service boundary.
- Pluggable translation providers for LibreTranslate, OpenAI, DeepL, or local fallback providers.
- PyInstaller for Windows packaging.

## Current Status

SnapLex is in P0 repository baseline work. The repository now has a Python package
skeleton, project metadata, and a bootstrap command that can be checked before GUI
dependencies are installed.

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

Round 1 validation uses import and bootstrap checks:

```powershell
python -m compileall snaplex
python -m snaplex --version
python -m snaplex --no-gui
```

Unit tests and stricter lint/typecheck commands are planned for later P0 rounds,
after service contracts and fake implementations exist.

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
