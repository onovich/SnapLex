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

## Implemented P4 Provider Hardening And Fallbacks

The repository now has accepted provider hardening:

- `snaplex/providers/http.py` defines an injectable HTTP transport boundary using
  the Python standard library.
- `snaplex/providers/config.py` defines runtime provider config for base URLs,
  API-key env var names, timeout, retry, and provider options.
- `snaplex/providers/libretranslate.py`, `openai.py`, and `deepl.py` implement
  real provider adapters behind the existing `TranslationProvider` contract.
- `snaplex/providers/retry.py` retries provider failures before the pipeline
  falls back to the next provider.
- `snaplex/providers/registry.py` registers fake, LibreTranslate, OpenAI, and
  DeepL providers while keeping fake as the selected default.
- `snaplex/storage/config.py` can build local runtime config from environment
  variables without storing API key values.
- `.env.example` and `docs/p4_provider_configuration.md` document local provider
  setup and optional real-provider smoke.
- Tests cover mocked HTTP success, missing credentials, timeout, retry, HTTP
  error, malformed response, unsupported language, fallback order, and fallback
  exhaustion.

The P4 final report is `docs/p4_final_validation_report.md`; the P5 handoff is
`docs/p4_to_p5_handoff.md`; the P5 execution guide is
`docs/p5_history_persistence_settings_goal_guide.md`.

## Implemented P5 History, Persistence, And Settings UX

The repository now has accepted local settings and optional translation history:

- `snaplex/storage/config.py` includes `JsonFileConfigStore`, config
  serialization, defaults, malformed-file fallback, and migration hooks.
- `snaplex/storage/paths.py` resolves `%APPDATA%\SnapLex`,
  `SNAPLEX_APP_DATA_DIR`, and a home-directory fallback.
- `snaplex/services/settings_service.py` provides a testable settings boundary.
- `snaplex/services/translation_service.py` refreshes provider registry from the
  current config store for future translations.
- `snaplex/storage/history.py` and `snaplex/services/history_service.py` provide
  text-only recent translation history with retention, delete, and clear.
- `snaplex/ui/settings_presenter.py` and `snaplex/ui/history_presenter.py`
  provide testable UI presentation boundaries.
- `snaplex/ui/app_shell.py` exposes compact settings and history dialogs.
- Clipboard and screen successful translations can record history when enabled.
- `docs/p5_privacy_and_storage.md` documents local data and privacy behavior.

The P5 final report is `docs/p5_final_validation_report.md`; the P6 handoff is
`docs/p5_to_p6_handoff.md`; the P6 execution guide is
`docs/p6_packaging_release_goal_guide.md`.

## Implemented P6 Packaging And Release Readiness

The repository now has accepted Windows packaging and release validation:

- `pyproject.toml` includes the optional `package` extra for PyInstaller.
- `scripts/package_windows.py` provides a repeatable Windows build wrapper.
- `packaging/snaplex.spec` is the tracked PyInstaller packaging entry.
- `.gitignore` keeps generated specs, `build/`, `dist/`, local smoke data,
  screenshots, OCR model caches, and packaged binaries out of git while allowing
  the chosen tracked spec.
- `snaplex/app.py` exposes `--smoke-package` and
  `snaplex/release_smoke.py` provides deterministic packaged workflow smoke.
- The base package smoke covers settings persistence, fake-provider clipboard
  translation, fake capture/OCR screen translation, and history
  record/list/delete/clear.
- `packaging/README.md`, `docs/p6_packaging_smoke_evidence.md`, and
  `docs/p6_release_checklist.md` document build, smoke, troubleshooting, local
  data, provider secret, and cleanup behavior.

The P6 final report is `docs/p6_final_validation_report.md`; the P7 handoff is
`docs/p6_to_p7_handoff.md`; the P7 execution guide is
`docs/p7_expansion_track_goal_guide.md`.

## P7 Expansion Track Completion

The repository now has accepted post-MVP expansion planning:

- `docs/p7_expansion_requirements.md` defines MVP freeze notes and expansion
  principles from the accepted P6 baseline.
- `docs/p7_multilingual_ux_plan.md` separates UI locale, translation language
  defaults, OCR hints, provider support messaging, and storage impact.
- `docs/p7_ai_summary_design.md` defines future `SummaryService` /
  `SummaryProvider` boundaries, privacy rules, settings needs, history
  interaction, and no-network test strategy.
- `docs/p7_browser_extension_bridge.md` defines future browser selection
  intents, trust boundaries, permission model, handoff options, privacy rules,
  and rejection criteria.
- `docs/p7_expansion_roadmap.md` separates accepted, deferred, and rejected
  post-MVP ideas.
- `docs/p7_final_validation_report.md` and `docs/p0_p7_final_report.md`
  provide the P7 and whole-track closure package for planner validation.

P7 introduced no runtime code or prototype. The accepted P6 package/release
baseline remains stable.

## Selected P8 Provider Setup And Real Translation UX

P8 is the selected first post-MVP implementation goal after trial feedback. It
supersedes the earlier low-risk localization recommendation because the current
trial blocker is user confidence in real translation:

- Provider setup must move into Settings instead of asking ordinary users to
  edit config files.
- Fake provider output must be visibly labeled as smoke/dev behavior.
- Real trial launch paths must not silently fall back to fake output.
- Provider readiness and connection checks should be testable without real
  network calls.
- The main shell, settings flow, and result view need an Apple HIG-inspired
  visual foundation before broader trial use.

The executable guide is
`docs/p8_provider_setup_real_translation_goal_guide.md`; the handoff is
`docs/p7_to_p8_handoff.md`.

## P8 Provider Setup And Real Translation UX Completion

The repository now has planner-accepted P8 provider setup UX:

- `snaplex/services/provider_setup.py` models provider setup and connection-test
  states without storing or displaying secret values.
- `SettingsService` and `SettingsPresenter` expose provider readiness and
  connection testing behind service/presenter boundaries.
- Settings UI renders provider choices, readiness, env var presence, provider
  fields, and a disabled future account-connect affordance.
- Real provider connection tests use mocked HTTP in automated tests.
- Fake provider output is labeled as fake smoke/dev mode in shared result
  state and UI.
- Trial docs and scripts keep real-provider launch paths separate from fake
  smoke paths.
- `docs/p8_final_validation_report.md` and `docs/p8_to_p9_handoff.md` provide
  the P8 closure package.

## P9 Apple-Inspired UI/UX Polish Completion

P9 planner-accepted work polishes the existing PySide6 desktop experience
without adding new product capabilities:

- Main shell and result-state hierarchy.
- Settings provider setup layout, focus order, and accessibility labels.
- History empty/list/long-entry states.
- Keyboard navigation and visible focus behavior.
- Long text and small-window behavior.
- Region selector status feedback and accessibility metadata.
- Screenshot-backed offscreen GUI smoke with uncommitted local artifacts.

The executable guide is `docs/p9_apple_inspired_ui_ux_goal_guide.md`. The P9
closure package is `docs/p9_final_validation_report.md` and
`docs/p9_to_p10_handoff.md`.

## P10 Secure Credential And Account Strategy Completion

P10 planner-accepted work addresses the remaining real-provider setup gap after
P8/P9: ordinary users should not need to edit environment variables forever,
but SnapLex also must not pretend that consumer account OAuth exists for
providers that expose API-key-based access.

P10 preserves environment-variable users, introduces credential service/store
boundaries, adds optional OS keyring support behind lazy dependencies and
fake-store tests, updates Settings and trial readiness to use credential
references instead of raw secrets, and documents future account/cloud/token
broker tradeoffs without implementing production OAuth, billing, or SnapLex
Cloud.

The closure package is `docs/p10_final_validation_report.md` and
`docs/p10_to_p11_handoff.md`.

## P11 Trial Release Hardening Completion

P11 planner-accepted work is release hardening, not feature expansion:

- visible Windows smoke for shell, Settings, History, focus, long text, fake
  warnings, and real/fake trial launch behavior;
- Windows Credential Locker/keyring smoke with a throwaway fake credential when
  the environment supports it;
- packaged credential behavior decision for base package versus a
  credential-capable variant or manual credentials extra;
- provider onboarding copy polish;
- key rotation and least-privilege notes;
- preservation of P10 credential boundaries, no-secret hygiene, deterministic
  fake smoke paths, and no-network automated tests.

P11 adds visible Windows GUI smoke, keyring blocker evidence, packaged
trial evidence, provider onboarding notes, key rotation guidance, a private
trial checklist, and a final boundary scan while preserving P10 credential
boundaries.

The closure package is `docs/p11_final_validation_report.md` and
`docs/p11_to_p12_handoff.md`.

## Selected P12 Private Trial Pilot And Feedback Triage

P12 is the selected next post-MVP implementation goal. It prepares the first
controlled private-trial pilot without adding runtime product scope:

- tester-facing release notes;
- feedback intake template and triage taxonomy;
- first private-trial pass/fail criteria;
- manual environment checks for assistive technology, DPI scaling,
  multi-monitor behavior, visible GUI, packaged fake smoke, and trial scripts;
- optional real-provider smoke policy that requires existing local credentials
  and intentional network approval;
- credential-capable package variant decision for a later phase;
- preservation of deterministic validation, no-secret boundaries, and P10/P11
  credential/release-hardening constraints.

The executable guide is
`docs/p12_private_trial_pilot_feedback_triage_goal_guide.md`; the TODO is
`docs/p12_todo.md`.

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
The P7 closure package is maintained in `docs/p7_final_validation_report.md`
and `docs/p0_p7_final_report.md`.

Summary:

- P0 Repository and Product Baseline: 4 conversation rounds.
- P1 Core Pipeline Foundation: 6 conversation rounds.
- P2 Clipboard Translation MVP: 8 conversation rounds.
- P3 Screen Capture and OCR MVP: 10 conversation rounds.
- P4 Provider Hardening and Fallbacks: 7 conversation rounds.
- P5 History, Persistence, and Settings UX: 6 conversation rounds.
- P6 Packaging and Release Readiness: 7 conversation rounds.
- P7 Expansion Track: 5 conversation rounds.
- P8 Provider Setup And Real Translation UX: 8 conversation rounds.
- P9 Apple-Inspired UI/UX Polish: 16 conversation rounds.
- P10 Secure Credential And Account Strategy: 16 conversation rounds.
- P11 Trial Release Hardening: 12 conversation rounds.
- P12 Private Trial Pilot And Feedback Triage: 12 conversation rounds.

Estimated total through the Windows MVP release candidate is 48 rounds.
Including the P7 post-MVP expansion track, the accepted plan was 53 rounds.
Including the selected P8 implementation goal, the post-MVP plan became 61
rounds. Including the accepted P9 implementation goal, the post-MVP plan became
77 rounds. Including accepted P10 credential/account strategy, the post-MVP
plan became 93 rounds. Including executor-complete P11 trial release hardening,
the post-MVP plan became 105 rounds. Including selected P12 private trial pilot
and feedback triage, the current post-MVP plan is 117 rounds.

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
