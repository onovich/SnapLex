# P4 to P5 Handoff

Date: 2026-06-22
Status: P4 provider hardening implementation complete; awaiting planner acceptance

Recommended next phase: P5 History, Persistence, and Settings UX

## P5 Goal

Persist local settings and optional recent translation history without storing
provider secrets in committed files or app-managed config.

## P4 Deliverables Available To P5

- `snaplex/storage/config.py`
  - `AppConfig`
  - `ProviderRuntimeConfig` values in `AppConfig.provider_configs`
  - `load_app_config_from_environment(...)`
- `snaplex/providers/`
  - `LibreTranslateProvider`
  - `OpenAITranslationProvider`
  - `DeepLTranslationProvider`
  - `UrllibHttpTransport`
  - `RetryingTranslationProvider`
- `snaplex/providers/registry.py`
  - `create_default_provider_registry(config, http_transport=..., environ=...)`
- `snaplex/services/translation_service.py`
  - `TranslationPipeline`
  - `create_default_translation_pipeline(config_store=..., http_transport=...)`
- `docs/p4_provider_configuration.md`
  - Environment variable and optional real-provider smoke notes.
- `.env.example`
  - Local provider configuration example without secrets.

## Accepted Runtime Boundaries

Clipboard:

```text
ClipboardService -> TranslationPipeline -> shared result view
```

Screen:

```text
RegionSelector -> CaptureService -> OcrService -> TranslationPipeline -> shared result view
```

P5 should preserve these flows. Settings and history should feed the service
configuration boundary, not bypass it.

## Recommended P5 Implementation Order

1. Add a file-backed config store with defaults, malformed-file fallback, and
   storage versioning/migration hooks.
2. Persist provider selection, provider order, language defaults, timeouts,
   retry counts, model options, and UI preferences.
3. Keep provider API keys out of persisted app config. Persist env var names
   only; continue reading actual secrets from the process environment.
4. Add history storage for recent translations with add/list/delete/clear
   operations.
5. Integrate settings and history UI lightly into the existing PySide6 shell.
6. Add privacy docs explaining local storage paths and history clearing.

## Guardrails

- Do not store actual OpenAI, DeepL, or LibreTranslate API key values.
- Do not commit `.env`, generated local config files, provider request logs, or
  translation history.
- Do not add packaging or PyInstaller work in P5.
- Do not add browser extension or AI summary scope in P5.
- Keep tests deterministic and no-network.
- Keep UI thin: settings UI should call storage/config services rather than
  reimplementing provider rules.

## P4 Known Limitations For P5

- P4 provider selection is environment-driven; P5 should make routine settings
  persistent.
- P4 has no recent translation history.
- P4 has no settings UI for provider order, target language, timeout, or retry.
- Optional real-provider smoke depends on local credentials and was not required
  for automated P4 validation.
