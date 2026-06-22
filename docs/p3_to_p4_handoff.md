# P3 to P4 Handoff

Date: 2026-06-22
Status: P3 screen capture/OCR MVP ready for validation

## P4 Goal

Add real translation provider hardening and fallback behavior without changing
the accepted clipboard and screen translation UI flows.

P4 should add configurable real provider adapters behind the existing P1 provider
contracts, keep automated tests mocked/no-network, and ensure clipboard and
screen result presenters receive the same internal translation errors they
already know how to display.

## Entry Points For P4

- `snaplex/providers/base.py`
  - `TranslationProvider`
  - `TranslationRequest`
  - `TranslationResponse`
- `snaplex/providers/registry.py`
  - `ProviderRegistry`
  - `create_default_provider_registry(...)`
- `snaplex/providers/fake.py`
  - deterministic provider scenarios for tests
- `snaplex/services/translation_service.py`
  - `TranslationPipeline.translate_text(...)`
  - `TranslationPipeline.translate_text_async(...)`
- `snaplex/storage/config.py`
  - `AppConfig.provider_name`
  - `AppConfig.provider_order`
  - source/target language defaults
- `snaplex/ui/translation_result.py`
  - shared translation error-to-message behavior
- `snaplex/ui/clipboard_presenter.py`
  - clipboard result flow
- `snaplex/ui/screen_presenter.py`
  - screen result flow

## Current Accepted Runtime Flows

Clipboard:

```text
ClipboardService -> TranslationPipeline -> shared result view
```

Screen:

```text
RegionSelector -> CaptureService -> OcrService -> TranslationPipeline -> shared result view
```

P4 provider work should plug into `TranslationPipeline` and should not require
clipboard or screen widgets to know which provider is active.

## Recommended P4 Implementation Order

1. Extend provider config for real provider selection and credentials via local
   environment/config boundaries.
2. Add a LibreTranslate adapter first because it can be self-hosted or mocked
   simply.
3. Add mocked HTTP tests for provider success, timeout, HTTP error, malformed
   response, and unsupported language behavior.
4. Add OpenAI and DeepL adapters behind optional configuration.
5. Verify fallback order through `TranslationPipeline` with no UI changes.
6. Update docs and smoke notes for configuring providers.

## Guardrails

- Do not make automated tests call real provider endpoints.
- Do not commit API keys, local credentials, or generated secrets.
- Provider adapters must raise internal `TranslationError` subclasses.
- UI must keep calling `TranslationPipeline`; widgets must not call HTTP clients
  or provider instances directly.
- P4 should not add persistent settings/history UI. That belongs to P5.
- P4 should not package the app. That belongs to P6.
- Keep fake provider mode as the default deterministic validation path.

## P3 Deferred Items Relevant To P4

- Visible real-capture and real-OCR smoke remains useful context, but P4 should
  not block provider work on OCR model availability.
- The shared result presenter already maps provider timeout, provider failure,
  unsupported language, stale result, unknown provider, and fallback exhaustion.
- P4 should preserve those internal errors rather than inventing UI-specific
  provider messages.

## Suggested P4 First Round

Add the first real provider adapter behind the existing `TranslationProvider`
protocol with mocked HTTP tests and no UI changes. Keep the default provider
registry fake-first until configuration and credentials are explicitly wired.

