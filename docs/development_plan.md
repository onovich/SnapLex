# SnapLex Development Plan

## Project Understanding

SnapLex is a keyboard-first desktop utility for fast translation of text visible on screen or already selected by the user. The product should feel non-intrusive: a small always-on-top widget, minimal clicks, reliable fallbacks, and a quick popup result instead of a heavy document-style interface.

The product has two core flows:

- Screen translation: user triggers capture, selects a screen region, OCR extracts text, translation runs, and a popup renders the result.
- Clipboard translation: user selects text, presses a hotkey, SnapLex copies or reads clipboard text, translates it, and displays the result.

The architecture from the current PDF docs separates the app into UI, capture, OCR, clipboard, translation, and storage layers. That separation should be kept from the start so OCR engines and translation providers can be swapped without rewriting UI code.

## MVP Goals

- Floating always-on-top widget with capture and clipboard translation actions.
- Region selection overlay and screenshot capture.
- OCR service with lazy model loading and clear failure states.
- Translation provider interface: `translate(text, source_lang, target_lang) -> translated_text`.
- At least one no-key local or self-hostable translation path for development.
- Popup result view with source text, translated text, copy action, and retry.
- Local config for hotkeys, provider settings, target language, and UI preferences.

## Architecture Direction

- `snaplex/app.py`: application bootstrap and dependency wiring.
- `snaplex/ui/`: PySide6 floating widget, overlay, popup, settings views.
- `snaplex/services/capture_service.py`: screen grab and region selection support.
- `snaplex/services/ocr_service.py`: image-to-text boundary, initially PaddleOCR-backed with a mockable interface.
- `snaplex/services/clipboard_service.py`: clipboard reads, copy hotkey flow, empty clipboard fallback.
- `snaplex/services/translation_service.py`: provider registry, timeout handling, cache lookup.
- `snaplex/providers/`: LibreTranslate, OpenAI, DeepL, and local/mock providers.
- `snaplex/storage/`: config and translation history persistence.
- `tests/`: service-level tests first, UI smoke tests after the desktop shell exists.

## Milestones

1. Repository foundation
   - Create Python project metadata, package layout, lint/test tooling, and sample config.
   - Add provider and OCR interfaces with fake implementations.
   - Add basic unit tests for normalization, provider dispatch, timeout behavior, and cache keys.

2. Clipboard translation MVP
   - Build the PySide6 floating widget and result popup.
   - Add global hotkey flow where practical on Windows.
   - Implement clipboard read, text normalization, translation, popup rendering, copy result, retry, and error messages.

3. Screen capture and OCR MVP
   - Build transparent region selection overlay.
   - Capture the selected region with `mss` or `pyautogui`.
   - Add OCR service with lazy loading and a fake/test OCR backend.
   - Connect OCR output into the same translation/result pipeline as clipboard translation.

4. Provider hardening
   - Add LibreTranslate provider for development.
   - Add API-key providers behind config/env variables.
   - Implement timeout handling, provider fallback order, and recent translation cache.

5. Persistence and history
   - Store user settings locally.
   - Add optional recent translation history with clear/delete controls.
   - Keep sensitive keys out of committed files and logs.

6. Packaging and release readiness
   - Add PyInstaller build configuration.
   - Smoke test launch, capture, clipboard, provider config, and popup behavior on Windows.
   - Document setup, development, packaging, and troubleshooting steps.

## Validation Plan

- Unit tests for service boundaries, provider selection, text normalization, cache behavior, and error mapping.
- Integration tests with fake OCR and fake translation providers for both runtime flows.
- Manual smoke checklist for Windows desktop behavior: always-on-top widget, region overlay, clipboard hotkey, popup focus behavior, and network timeout fallback.
- Packaging smoke test after PyInstaller is introduced.

## Key Risks

- OCR model size and startup time may hurt perceived speed; mitigate with lazy loading and progress states.
- Global hotkeys and clipboard access vary by OS and security settings; keep the first target explicit: Windows MVP.
- Translation APIs require credentials and network reliability; include a development provider and fallback behavior early.
- Region selection overlays can conflict with DPI scaling and multi-monitor setups; test these before polishing UI details.

