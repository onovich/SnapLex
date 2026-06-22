# SnapLex Development Plan

## Project Understanding

SnapLex is a keyboard-first desktop utility for fast translation of text visible on screen or already selected by the user. The product should feel non-intrusive: a small always-on-top widget, minimal clicks, reliable fallbacks, and a quick popup result instead of a heavy document-style interface.

The product has two core flows:

- Screen translation: user triggers capture, selects a screen region, OCR extracts text, translation runs, and a popup renders the result.
- Clipboard translation: user selects text, presses a hotkey, SnapLex copies or reads clipboard text, translates it, and displays the result.

The architecture from the current PDF docs separates the app into UI, capture, OCR, clipboard, translation, and storage layers. That separation should be kept from the start so OCR engines and translation providers can be swapped without rewriting UI code.

## Implemented P0 Baseline

The repository now has a runnable Python package baseline:

- `pyproject.toml` defines package metadata, optional GUI/capture/OCR/dev extras, and the `snaplex` console entry point.
- `snaplex/app.py` provides the CLI/bootstrap boundary.
- `snaplex/ui/app_shell.py` lazy-loads PySide6 and falls back cleanly when GUI dependencies are absent.
- `snaplex/services/` defines capture, OCR, clipboard, text normalization, and translation service boundaries.
- `snaplex/providers/` defines translation provider contracts and a deterministic fake provider.
- `snaplex/storage/` defines config storage contracts and an in-memory config store.
- `tests/` covers normalization, fake provider behavior, fake OCR/capture behavior, and config defaults.
- `.codex/project-ops-workflow.json` and `.codex/project-git-workflow.json` run repeatable validation before commits.

The P0 handoff is `docs/p0_to_p1_handoff.md`; the next implementation checklist is `docs/p1_todo.md`.

## Implemented P1 Baseline

The repository now has the core non-UI translation pipeline:

- `snaplex/errors.py` defines stable pipeline/provider error types.
- `snaplex/providers/registry.py` maps config provider names to runtime provider instances.
- `snaplex/providers/fake.py` supports deterministic success, failure, timeout, unsupported-language, and stale-result scenarios.
- `snaplex/services/translation_service.py` exposes `TranslationPipeline.translate_text(...)` and `translate_text_async(...)`.
- `snaplex/services/translation_cache.py` provides in-memory cache keying and storage.
- `snaplex/storage/config.py` defines translation defaults and provider fallback order.
- Tests cover normalization, errors, registry lookup, fake scenarios, cache hits/misses, fallback, timeout, and async behavior.

The P1 final report is `docs/p1_final_validation_report.md`; the P2 handoff is `docs/p1_to_p2_handoff.md`.

## Implemented P2 Clipboard MVP

The repository now has the first user-facing clipboard translation vertical slice:

- `snaplex/ui/clipboard_presenter.py` owns loading, success, empty clipboard, error,
  retry, copy, and close presentation states.
- `snaplex/ui/app_shell.py` provides a small always-on-top PySide6 shell with the
  `Translate Clipboard`, `Copy Result`, `Retry`, and `Close Result` actions.
- `snaplex/services/clipboard_service.py` provides `InMemoryClipboardService` for
  deterministic tests and `QtClipboardService` for the desktop clipboard.
- Clipboard text flows through `TranslationPipeline.translate_text_async(...)`.
- UI error states cover empty clipboard, unknown provider, timeout, provider
  failure, fallback exhaustion, unsupported language, stale result, clipboard read
  failure, and unexpected pipeline failure.
- P2 smoke evidence is recorded in `docs/p2_windows_smoke_evidence.md`.

The P2 final report is `docs/p2_final_validation_report.md`; the P3 handoff is
`docs/p2_to_p3_handoff.md`; the P3 execution guide is
`docs/p3_screen_capture_ocr_goal_guide.md`.

## Implemented P3 Screen Capture And OCR MVP

The repository now has an accepted screen translation vertical slice:

- `snaplex/ui/region_selector.py` provides a minimal Qt region selection overlay
  and a pure selection presenter for tests.
- `snaplex/services/capture_service.py` provides capture geometry, deterministic
  fake capture, and lazy optional `MssCaptureService`.
- `snaplex/services/ocr_service.py` provides deterministic fake OCR scenarios and
  lazy optional `PaddleOcrService`.
- `snaplex/services/screen_translation_service.py` orchestrates capture -> OCR ->
  `TranslationPipeline`.
- `snaplex/ui/screen_presenter.py` maps success, cancel, invalid region, capture
  failure, OCR unavailable/failure, empty OCR result, translation failure, retry,
  copy, and close states into the shared result view.
- Optional `mss` and `paddleocr` dependencies are not imported during app shell
  import or no-GUI bootstrap.

The P3 final report is `docs/p3_final_validation_report.md`; the P4 handoff is
`docs/p3_to_p4_handoff.md`; the P4 execution guide is
`docs/p4_provider_hardening_goal_guide.md`.

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
   - Build the PySide6 floating widget and result view.
   - Keep global hotkey support deferred until it can be implemented and smoked safely.
   - Implement clipboard read, text normalization through the P1 pipeline,
     translation, result rendering, copy result, retry, and error messages.

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

## Detailed Phase Plan

The concrete phase-by-phase execution plan is maintained in `docs/phase_plan.md`.
The full P0-P7 delegated execution guide is maintained in `docs/p0_p7_goal_mode_execution_guide.md`.
The first executable phase guide is maintained in `docs/p0_repository_baseline_goal_guide.md`.
The next executable phase guide is maintained in `docs/p4_provider_hardening_goal_guide.md`.

Summary:

- P0 Repository and Product Baseline: 4 conversation rounds.
- P1 Core Pipeline Foundation: 6 conversation rounds.
- P2 Clipboard Translation MVP: 8 conversation rounds.
- P3 Screen Capture and OCR MVP: 10 conversation rounds.
- P4 Provider Hardening and Fallbacks: 7 conversation rounds.
- P5 History, Persistence, and Settings UX: 6 conversation rounds.
- P6 Packaging and Release Readiness: 7 conversation rounds.
- P7 Expansion Track: 5 conversation rounds.

Estimated total through the Windows MVP release candidate is 48 rounds. Including the post-MVP expansion track, the plan is 53 rounds.

## Validation Plan

- Unit tests for service boundaries, provider selection, text normalization, cache behavior, and error mapping.
- Integration tests with fake OCR and fake translation providers for both runtime flows.
- Manual smoke checklist for Windows desktop behavior: always-on-top widget, clipboard
  action, region overlay, future hotkey behavior, popup focus behavior, and network
  timeout fallback.
- Packaging smoke test after PyInstaller is introduced.

## Key Risks

- OCR model size and startup time may hurt perceived speed; mitigate with lazy loading and progress states.
- Global hotkeys and clipboard access vary by OS and security settings; keep the
  first target explicit: Windows MVP. P2 defers global hotkeys and accepts the
  manual clipboard action.
- Translation APIs require credentials and network reliability; include a development provider and fallback behavior early.
- Region selection overlays can conflict with DPI scaling and multi-monitor setups; test these before polishing UI details.
