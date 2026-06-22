# P2 to P3 Handoff

Date: 2026-06-22
Status: P2 clipboard MVP ready for validation

## P3 Goal

Build the screen capture and OCR MVP on top of the accepted P1 translation
pipeline and the P2 result-flow patterns.

P3 should let a user trigger screen translation, select or provide a screen
region, extract text through an OCR service boundary, translate the extracted
text through `TranslationPipeline`, and render the result in the existing desktop
shell/result view pattern.

## Entry Points For P3

- `snaplex/services/capture_service.py`
  - `CaptureService`
  - `FakeCaptureService`
  - `ScreenRegion`
- `snaplex/services/ocr_service.py`
  - `OcrService`
  - `FakeOcrService`
  - `OcrResult`
- `snaplex/services/translation_service.py`
  - `TranslationPipeline.translate_text(...)`
  - `TranslationPipeline.translate_text_async(...)`
  - `create_default_translation_pipeline(...)`
- `snaplex/ui/app_shell.py`
  - Add the screen translation action and any minimal shell wiring here.
- `snaplex/ui/clipboard_presenter.py`
  - Reuse the state-machine pattern for loading, success, retry, copy, close,
    and user-friendly error states.
  - If OCR needs a non-clipboard-specific presenter, extract shared result-state
    behavior instead of duplicating it.

## Expected P3 Flow

```text
User trigger -> region selection/capture -> OCR text -> TranslationPipeline -> result view
```

The OCR flow should reuse the P1 pipeline for translation behavior and should not
call translation providers directly.

## Current P2 Result Behavior To Preserve

- Loading state while async work runs.
- Success state with source text, translated text, provider name, copy, retry,
  and close.
- Empty-input state for no text.
- Error states for expected service/provider failures.
- Retry reuses the last source text where possible.
- Copy writes only successful translated text.
- Widgets do not own provider selection, fallback, cache, or normalization logic.

## Recommended P3 Implementation Order

1. Add a screen translation action to the shell with an injected presenter/service
   path and no real capture yet.
2. Add deterministic capture/OCR tests with fake region and fake OCR output.
3. Add a minimal region selection or capture adapter only after the fake path is
   covered.
4. Wire OCR text into `TranslationPipeline.translate_text_async(...)`.
5. Reuse or extract result-state UI for OCR translation results.
6. Add Windows smoke notes for capture, cancel, OCR success, OCR empty result, and
   OCR failure.

## P3 Guardrails

- Keep screen capture behind `CaptureService`.
- Keep OCR behind `OcrService`.
- Keep translation behind `TranslationPipeline`.
- Do not add real network translation providers in P3.
- Do not add persistent history/settings in P3.
- Do not add PyInstaller packaging in P3.
- Keep tests deterministic; use fake image/capture/OCR fixtures.
- If DPI or multi-monitor behavior is unstable, document the limitation and keep
  the single-monitor smoke path reliable first.

## P2 Deferred Items Relevant To P3

- Global hotkeys remain deferred. P3 may add a manual screen translation action
  without solving global hotkeys.
- P2 GUI smoke used Qt offscreen automation. P3 should add visible Windows smoke
  notes for region selection when the overlay exists.

## Suggested P3 First Round

Add the screen translation action shell and a presenter/service skeleton that can
accept injected fake OCR text, call the P1 pipeline, and render through the same
result-state surface as P2. Do not start with real capture or OCR dependencies.

