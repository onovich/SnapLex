# SnapLex Phase Development Plan

Date: 2026-06-22
Status: executable planning document

## 0. Round Estimate Rules

This plan estimates work in Codex conversation rounds. One round means one focused implementation session with code/docs changes, local validation, a short report, and, when requested, commit and push.

Round estimates assume one primary developer agent, Windows as the MVP target, and no existing application code beyond the current docs. A phase can finish earlier if validation is clean; use the buffer rounds for bug fixes, dependency friction, packaging issues, and UI smoke fixes.

## 1. Phase Summary

| Phase | Name | Goal | Estimated rounds |
| --- | --- | --- | --- |
| P0 | Repository and Product Baseline | Turn the document-only repo into a runnable Python project skeleton with clear contracts. | 4 rounds |
| P1 | Core Pipeline Foundation | Build text normalization, provider abstraction, fake providers, cache, and config boundaries. | 6 rounds |
| P2 | Clipboard Translation MVP | Deliver a usable clipboard-to-popup desktop flow. | 8 rounds |
| P3 | Screen Capture and OCR MVP | Deliver region capture, OCR extraction, and shared translate/render flow. | 10 rounds |
| P4 | Provider Hardening and Fallbacks | Add real provider integrations, timeout handling, fallback order, and safe provider configuration. | 7 rounds |
| P5 | History, Persistence, and Settings UX | Add local settings and optional recent translation history. | 6 rounds |
| P6 | Packaging and Release Readiness | Produce and smoke-test a Windows distributable. | 7 rounds |
| P7 | Expansion Track | Prepare optional AI summary, multilingual polish, and browser-extension bridge planning. | 5 rounds |

Total MVP estimate through P6: 48 rounds.
Total including P7 expansion planning: 53 rounds.

The whole-goal execution guide for delegated implementation is `docs/p0_p7_goal_mode_execution_guide.md`.

## 2. P0 - Repository and Product Baseline

Estimated rounds: 4

Goal: create a clean Python project foundation that future phases can extend without reworking structure.

Scope:

- Add `pyproject.toml`, package layout, dependency groups, test tooling, lint/format tooling, and entry-point command.
- Create `snaplex/` modules for app bootstrap, services, providers, storage, and UI placeholders.
- Add a sample config file and environment variable documentation.
- Convert current PDF-derived understanding into developer-facing docs and a first smoke checklist.

Deliverables:

- Runnable command such as `python -m snaplex` or a console script.
- Placeholder PySide6 app shell that can start without OCR/provider credentials.
- Service interfaces and fake implementations for tests.
- Initial unit test suite.

Validation:

- Dependency install succeeds in a fresh virtual environment.
- Unit tests pass.
- Lint or format check passes.
- App bootstrap command exits or opens a minimal shell without import errors.

Round split:

- Round 1: project metadata, package layout, dev commands.
- Round 2: service/provider/storage interface skeletons.
- Round 3: fake implementations and tests.
- Round 4: docs, smoke checklist, cleanup, validation.

## 3. P1 - Core Pipeline Foundation

Estimated rounds: 6

Execution guide: `docs/p1_core_pipeline_goal_guide.md`

Goal: implement the non-UI translation pipeline that both clipboard and OCR flows will reuse.

Scope:

- Text normalization and language parameter handling.
- `TranslationProvider` protocol and provider registry.
- Fake/local development provider for deterministic testing.
- Translation cache keying and basic in-memory cache.
- Error model for empty input, provider failure, timeout, unsupported language, and stale result.
- Async-friendly pipeline boundary so UI calls do not block.

Deliverables:

- `translate_text(...)` application service.
- Provider registry with fake provider and stub real-provider adapters.
- Config-driven source/target language defaults.
- Unit tests for success, empty input, provider errors, timeouts, fallback, and cache hits.

Validation:

- Unit tests pass without network.
- Pipeline can be exercised from a small CLI/dev script.
- No API keys or local secrets are required for tests.

Round split:

- Round 1: normalize input and define provider/error contracts.
- Round 2: provider registry and fake provider.
- Round 3: translation pipeline orchestration.
- Round 4: cache and fallback behavior.
- Round 5: async boundary and timeout tests.
- Round 6: docs, cleanup, validation.

## 4. P2 - Clipboard Translation MVP

Estimated rounds: 8

Execution guide: `docs/p2_clipboard_translation_goal_guide.md`

Goal: make SnapLex useful for selected-text translation through clipboard and a desktop popup.

Scope:

- PySide6 floating always-on-top widget.
- Clipboard read service and empty clipboard fallback.
- Manual trigger button first, then Windows hotkey where practical.
- Result popup with source text, translated text, copy result, retry, and error state.
- Non-blocking UI wiring to P1 pipeline.
- Basic UI smoke path for launch, translate, retry, and copy.

Deliverables:

- User can start the app, trigger clipboard translation, and see a popup result.
- Fake provider mode works without network.
- Clipboard errors and empty text produce clear UI states.
- Minimal settings for target language and provider selection if needed for the flow.

Validation:

- Unit tests for clipboard service using mocks.
- Integration test for clipboard pipeline with fake provider.
- Manual smoke on Windows: launch widget, copy text, translate, copy result, retry.

Round split:

- Round 1: floating widget shell.
- Round 2: result popup component.
- Round 3: clipboard service and mocks.
- Round 4: connect clipboard to translation pipeline.
- Round 5: UI error, loading, retry, and copy states.
- Round 6: hotkey investigation and implementation where stable.
- Round 7: UI polish and smoke fixes.
- Round 8: docs, validation, release note for MVP behavior.

## 5. P3 - Screen Capture and OCR MVP

Estimated rounds: 10

Execution guide: `docs/p3_screen_capture_ocr_goal_guide.md`

Goal: support screen-region translation using capture, OCR, translation, and the same popup result UI.

Scope:

- Transparent region-selection overlay.
- Screenshot capture via `mss` or `pyautogui`.
- OCR service interface with fake OCR backend for tests.
- PaddleOCR adapter behind lazy loading.
- Shared pipeline: capture -> OCR -> normalize -> translate -> popup.
- OCR failure retry and empty OCR result handling.
- Multi-monitor and DPI-scaling smoke notes for Windows.

Deliverables:

- User can click capture, select a region, OCR text, translate it, and view result.
- OCR backend can be swapped or disabled for development.
- Lazy loading keeps app launch responsive.
- Failure states are visible and recoverable.

Validation:

- Unit tests for capture geometry and OCR service contracts where feasible.
- Integration test using a fixture image and fake OCR.
- Manual smoke: single monitor, scaled display, cancel selection, small region, OCR failure, successful translation.

Round split:

- Round 1: capture service contract and geometry model.
- Round 2: screenshot backend prototype.
- Round 3: region overlay UI.
- Round 4: overlay-to-capture integration.
- Round 5: OCR service interface and fake backend.
- Round 6: PaddleOCR adapter with lazy loading.
- Round 7: capture/OCR/translation pipeline integration.
- Round 8: failure states, retry, cancel behavior.
- Round 9: Windows DPI and multi-monitor smoke fixes.
- Round 10: docs, validation, cleanup.

## 6. P4 - Provider Hardening and Fallbacks

Estimated rounds: 7

Execution guide: `docs/p4_provider_hardening_goal_guide.md`

Goal: make real translation providers usable while keeping development and failure behavior predictable.

Scope:

- LibreTranslate provider for local or self-hosted development.
- OpenAI and DeepL provider adapters behind optional configuration.
- Timeout, retry, and fallback order.
- Provider health/error reporting.
- Sensitive config handling through environment variables or local ignored config.
- Provider-level tests with mocked HTTP.

Deliverables:

- Users can choose provider and configure credentials locally.
- Network timeout can fall back to another provider when configured.
- Tests do not call external services.
- Provider errors map cleanly into UI states.

Validation:

- Mocked HTTP tests for each provider adapter.
- Integration tests for fallback order.
- Manual smoke with fake provider and one configured real provider when credentials exist.

Round split:

- Round 1: provider config model.
- Round 2: LibreTranslate adapter.
- Round 3: OpenAI adapter.
- Round 4: DeepL adapter.
- Round 5: fallback order, retry, timeout behavior.
- Round 6: provider configuration docs and optional real-provider smoke.
- Round 7: validation and hardening.

## 7. P5 - History, Persistence, and Settings UX

Estimated rounds: 6

Execution guide: `docs/p5_history_persistence_settings_goal_guide.md`

Goal: persist user preferences and optional recent translations without making the app feel heavy.

Scope:

- Local config storage for hotkeys, target language, provider, and UI preferences.
- Optional recent translation history.
- History list with copy, delete, and clear controls.
- Storage migration/versioning boundary.
- Privacy-first defaults and clear docs for local data.

Deliverables:

- Settings persist across app restarts.
- Recent translations can be reviewed and cleared.
- Storage layer is testable without PySide6.
- Sensitive values are not committed or logged.

Validation:

- Unit tests for config read/write, defaults, malformed config, and migration.
- Unit tests for history add/list/delete/clear.
- Manual smoke: change setting, restart app, verify setting; add history, clear history.

Round split:

- Round 1: config storage model.
- Round 2: settings service and tests.
- Round 3: history storage and tests.
- Round 4: settings UI integration.
- Round 5: history UI integration.
- Round 6: privacy docs, validation, cleanup.

## 8. P6 - Packaging and Release Readiness

Estimated rounds: 7

Goal: package the Windows MVP and make release validation repeatable.

Scope:

- PyInstaller configuration.
- Asset/model handling strategy for OCR.
- Windows launch smoke and packaging smoke.
- Troubleshooting docs for dependencies, provider config, hotkeys, and OCR model loading.
- Release checklist and versioning convention.

Deliverables:

- Reproducible packaging command.
- Windows executable artifact or distributable folder.
- Smoke-tested release candidate checklist.
- README setup and packaging instructions.

Validation:

- Clean environment install/build succeeds.
- Packaged app launches.
- Clipboard translation smoke passes in packaged app.
- Screen capture smoke passes in packaged app if OCR dependencies are included or documented.

Round split:

- Round 1: package entry points and app metadata.
- Round 2: PyInstaller spec.
- Round 3: dependency and asset inclusion.
- Round 4: packaged launch smoke.
- Round 5: clipboard and capture smoke on packaged app.
- Round 6: docs and troubleshooting.
- Round 7: final release checklist and cleanup.

## 9. P7 - Expansion Track

Estimated rounds: 5

Goal: prepare post-MVP expansion without destabilizing the MVP.

Scope:

- Multilingual UX improvements.
- AI summarization as an optional provider-style capability.
- Browser extension integration design.
- Exportable history or notes if needed.
- Roadmap update based on MVP feedback.

Deliverables:

- Design notes and technical boundaries for each expansion.
- One narrow prototype only if it does not touch MVP stability.
- Updated roadmap with accepted, deferred, and rejected ideas.

Validation:

- Docs review for scope boundaries.
- Prototype tests if code is introduced.
- No MVP regression or provider contract breakage.

Round split:

- Round 1: feedback and requirements synthesis.
- Round 2: multilingual and AI summary design.
- Round 3: browser extension bridge design.
- Round 4: optional narrow prototype.
- Round 5: roadmap update and validation.

## 10. Recommended Execution Order

Execute P0 through P3 first before broadening provider scope. This gives the project a working vertical slice: fake provider, clipboard path, capture path, OCR boundary, and popup rendering. After that, P4 through P6 turn the MVP into a usable release candidate.

Current accepted phase: P4 - Provider Hardening and Fallbacks.

Recommended next phase: P5 - History, Persistence, and Settings UX.

For a dedicated implementation programmer taking P0-P7 as one continuous goal, use `docs/p0_p7_goal_mode_execution_guide.md`.
The direct execution guide for the first phase is `docs/p0_repository_baseline_goal_guide.md`.
The latest completed phase report is `docs/p4_final_validation_report.md`.
The next handoff is `docs/p4_to_p5_handoff.md`.
The direct execution guide for the next phase is `docs/p5_history_persistence_settings_goal_guide.md`.
