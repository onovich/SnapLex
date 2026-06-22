# P1 to P2 Handoff

Date: 2026-06-22
Status: P1 pipeline complete

## P2 Goal

Build the clipboard translation MVP on top of the P1 pipeline. P2 should add UI and clipboard workflow behavior without duplicating translation, provider selection, fallback, cache, normalization, timeout, or error-mapping rules.

Use `docs/p2_clipboard_translation_goal_guide.md` as the executable P2 goal-mode guide.

## Entry Points For P2

- Use `create_default_translation_pipeline(...)` from `snaplex.services` for default wiring.
- Use `TranslationPipeline.translate_text(...)` for synchronous service tests.
- Use `TranslationPipeline.translate_text_async(...)` for UI-friendly calls.
- Use `AppConfig` fields:
  - `source_lang`
  - `target_lang`
  - `provider_name`
  - `provider_order`
- Use `FakeTranslationProvider` and `FakeTranslationScenario` for deterministic UI and integration tests.
- Use `FallbackExhaustedError`, `UnknownTranslationProviderError`, and provider-specific errors to map pipeline failures into UI error states.

## Expected P2 Flow

```text
Clipboard text -> normalize and translate through TranslationPipeline -> popup state
```

P2 UI code should not call provider instances directly. It should call the pipeline and render:

- Empty translated text for empty input.
- Successful translated text with provider name.
- Fallback exhaustion with a user-friendly provider failure message.
- Unknown provider with a settings/config error message.
- Timeout as a retryable provider error.

## Current Test Fixtures

- `tests/test_translation_pipeline.py`
- `tests/test_translation_cache.py`
- `tests/test_provider_registry.py`
- `tests/test_fake_provider.py`
- `tests/test_text.py`
- `tests/test_errors.py`

## P2 Guardrails

- Keep translation logic out of PySide6 widgets.
- Keep fake provider tests no-network.
- Do not add real provider HTTP calls in P2.
- Do not add screen capture or OCR behavior in P2.
- Do not persist history/settings in P2 unless the architect explicitly expands scope.
- Add UI smoke notes when the clipboard widget/popup appears.

## Suggested P2 First Round

Create the floating widget shell actions for clipboard translation, but wire them to a fake/injected pipeline first. Keep the real clipboard service and popup state tests separate from provider logic.
