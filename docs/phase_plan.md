# SnapLex Phase Development Plan

Date: 2026-06-22
Status: P20 planner-accepted; P21 ready for executor

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
| P8 | Provider Setup And Real Translation UX | Make real translation setup usable from Settings, separate fake smoke from real trial behavior, and establish the first Apple HIG-inspired UI foundation. | 8 rounds |
| P9 | Apple-Inspired UI/UX Polish | Make the PySide6 desktop shell trial-ready with visual hierarchy, accessibility, keyboard flow, long-text handling, and screenshot-backed GUI smoke. | 16 rounds |
| P10 | Secure Credential And Account Strategy | Add credential service boundaries, preserve env-var users, evaluate optional OS keyring storage, and document account/cloud strategy without production OAuth. | 16 rounds |
| P11 | Trial Release Hardening | Validate visible Windows behavior, manual keyring smoke, packaged credential behavior, onboarding copy, and release notes before broader private trial. | 12 rounds |
| P12 | Private Trial Pilot And Feedback Triage | Prepare tester-facing release notes, feedback intake, pass/fail criteria, manual environment checks, optional real-provider smoke policy, and triage rules. | 12 rounds |
| P13 | Private Trial Feedback Response And Credential Package Feasibility | Respond to the first private-trial feedback loop, close accepted S0/S1 blockers, capture manual environment results, and decide credential-capable package feasibility. | 12 rounds |
| P14 | Manual Environment And Source Keyring Validation | Run target-device manual checks, source keyring smoke, optional real-provider evidence, and decide whether to authorize a later credential-package spike. | 12 rounds |
| P15 | Isolated Credential-Capable Package Spike Design Gate | Prove, reject, or defer an explicit credential-capable package path while preserving the deterministic base package. | 12 rounds |
| P16 | Credential-Capable Package Production Hardening | Harden the explicit credential package path into a limited private tester candidate while preserving base package determinism. | 12 rounds |
| P17 | Limited Credential Package Pilot And Signing Decision | Run a controlled private tester lane and decide signing, installer, updater, artifact, support, and credential package variant policy. | 12 rounds |
| P18 | Signing And Distribution Readiness Gate | Decide signing identity, custody, verification, distribution, rollback, retention, and support policy before broader credential package distribution. | 12 rounds |
| P19 | Signing Rehearsal And Signed Archive Candidate Gate | Decide whether a safe isolated signing rehearsal can run and gate any signed archive candidate without public release. | 12 rounds |
| P20 | Approved Signing Path Acquisition And Rehearsal Setup Gate | Decide whether an approved safe signing path exists and set up or block isolated rehearsal work without public release. | 12 rounds |
| P21 | Signing Path Unblock Decision Or Pause Gate | Decide whether signing is unblocked for a later rehearsal or paused until human approval is supplied. | 8 rounds |

Total MVP estimate through P6: 48 rounds.
Total including P7 expansion planning: 53 rounds.
Total including selected P8 post-MVP implementation: 61 rounds.
Total including selected P9 post-MVP implementation: 77 rounds.
Total including selected P10 post-MVP implementation: 93 rounds.
Total including selected P11 post-MVP implementation: 105 rounds.
Total including selected P12 post-MVP implementation: 117 rounds.
Total including selected P13 post-MVP implementation: 129 rounds.
Total including selected P14 post-MVP implementation: 141 rounds.
Total including selected P15 post-MVP implementation: 153 rounds.
Total including selected P16 post-MVP implementation: 165 rounds.
Total including selected P17 post-MVP implementation: 177 rounds.
Total including accepted P18 post-MVP implementation: 189 rounds.
Total including accepted P19 post-MVP implementation: 201 rounds.
Total including accepted P20 post-MVP implementation: 213 rounds.
Total including selected P21 post-MVP implementation: 221 rounds.

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

Execution guide: `docs/p6_packaging_release_goal_guide.md`

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

Execution guide: `docs/p7_expansion_track_goal_guide.md`

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

Executor completion artifacts:

- `docs/p7_expansion_requirements.md`
- `docs/p7_multilingual_ux_plan.md`
- `docs/p7_ai_summary_design.md`
- `docs/p7_browser_extension_bridge.md`
- `docs/p7_expansion_roadmap.md`
- `docs/p7_final_validation_report.md`
- `docs/p0_p7_final_report.md`

P7 stayed documentation/design-first. No optional prototype was introduced.

## 10. Recommended Execution Order

Execute P0 through P3 first before broadening provider scope. This gives the project a working vertical slice: fake provider, clipboard path, capture path, OCR boundary, and popup rendering. After that, P4 through P6 turn the MVP into a usable release candidate.

Current accepted phase: P16 - Credential-Capable Package Production Hardening.

Current executor-complete phase: P17 - Limited Credential Package Pilot And
Signing Decision, ready for planner check.

P0-P7 status: complete.

Selected next step: planner recheck of P17 using
`docs/p17_final_validation_report.md` and `docs/p17_to_p18_handoff.md`.

For a dedicated implementation programmer taking P0-P7 as one continuous goal, use `docs/p0_p7_goal_mode_execution_guide.md`.
The direct execution guide for the first phase is `docs/p0_repository_baseline_goal_guide.md`.
The latest accepted phase report is `docs/p9_final_validation_report.md`.
The whole-track closure report is `docs/p0_p7_final_report.md`.

## 11. P8 - Provider Setup And Real Translation UX

Estimated rounds: 8

Execution guide: `docs/p8_provider_setup_real_translation_goal_guide.md`

Goal: make real translation setup usable for trial users without config-file
editing, make fake mode visibly separate from real translation, and improve the
first-run UI foundation.

Scope:

- Settings-based provider setup for fake, LibreTranslate, OpenAI, and DeepL.
- Provider readiness and connection testing behind service/presenter boundaries.
- Clear fake-versus-real trial behavior in commands, docs, and result UI.
- No raw API key values stored in JSON config, history, docs, tests, logs, or
  package resources.
- Apple HIG-inspired main shell, settings, and result-view polish.

Deliverables:

- Provider setup UX in Settings.
- Deterministic tests for provider setup and mocked provider readiness checks.
- Updated trial docs and smoke checklist.
- P8 final validation report and P8 to P9 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Package dry-run remains green.
- Real trial path rejects missing real providers clearly.
- Fake trial path remains deterministic smoke/dev mode.
- Boundary scan confirms no generated artifacts, local data, `.env`, or secrets
  are committed.

Round split:

- Round 1: rebaseline, provider setup state decisions, and audit.
- Round 2: settings presenter/service provider setup model.
- Round 3: provider readiness and connection testing.
- Round 4: Settings UI integration and no-config onboarding.
- Round 5: real trial commands, fake guardrails, and docs.
- Round 6: main shell and result visual foundation.
- Round 7: buffer hardening and package preservation.
- Round 8: final validation, report, and P9 handoff.

Executor completion artifacts:

- `docs/p8_provider_setup_decisions.md`
- `docs/p8_real_provider_trial_notes.md`
- `docs/p8_final_validation_report.md`
- `docs/p8_to_p9_handoff.md`

Planner acceptance:

- P8 accepted on 2026-07-15 at
  `d8d451a0c2efc140032737ec2afbbbdb2a4f704c`.

## 12. P9 - Apple-Inspired UI/UX Polish

Estimated rounds: 16

Execution guide: `docs/p9_apple_inspired_ui_ux_goal_guide.md`

Goal: make the existing PySide6 shell feel trial-ready without adding new
runtime product scope.

Scope:

- Visual audit and UI polish for main shell, result states, Settings, History,
  and region-selector touchpoints.
- Shared visual foundation for spacing, typography, semantic color, focus, and
  stable control dimensions.
- Keyboard navigation, focus order, accessible labels, and contrast checks.
- Long-text and small-window behavior for source, translation, OCR, provider,
  error, and history content.
- Screenshot-backed offscreen GUI smoke with screenshots kept in ignored local
  paths only.

Deliverables:

- Polished PySide6 shell, Settings, History, and result states.
- Screenshot-backed smoke helper/evidence.
- P9 final validation report and P9 to P10 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Package dry-run remains green.
- Fake/real trial command smoke remains green.
- GUI offscreen/screenshot smoke covers representative states.
- Boundary scan confirms no screenshots, generated artifacts, local data,
  `.env`, or secrets are committed.

Round split:

- Round 1: UI audit, visual targets, and baseline screenshots.
- Round 2: shared visual foundation.
- Round 3: main shell action hierarchy.
- Round 4: result state polish.
- Round 5: long text and small-window behavior.
- Round 6: Settings information architecture.
- Round 7: Settings keyboard and accessibility.
- Round 8: History dialog polish.
- Round 9: region selector and screen-flow UI polish.
- Round 10: iconography and command semantics.
- Round 11: screenshot-backed GUI smoke.
- Round 12: Windows visual QA and docs.
- Rounds 13-15: buffer hardening.
- Round 16: final validation, report, and P10 handoff.

Executor completion artifacts:

- `docs/p9_ui_audit.md`
- `docs/p9_visual_smoke_evidence.md`
- `docs/p9_hardening_notes.md`
- `docs/p9_final_validation_report.md`
- `docs/p9_to_p10_handoff.md`

Planner acceptance:

- P9 accepted on 2026-07-15 at
  `a2ebc99a47bc810fe3f6245f61a26a16fc6650b3`.

## 13. P10 - Secure Credential And Account Strategy

Estimated rounds: 16

Execution guide: `docs/p10_secure_credential_account_strategy_goal_guide.md`

Goal: add a safe credential/account strategy and first local secure credential
path without breaking existing environment-variable provider users or adding
production cloud/account OAuth scope.

Scope:

- Credential threat model and strategy decision document.
- Credential reference/status models and service/store boundaries.
- Environment-variable credential compatibility and migration-safe config.
- Optional lazy OS keyring path with fake-store tests, or a documented concrete
  blocker if the path cannot be implemented safely.
- Provider readiness and Test Connection routed through credential boundaries.
- Settings secure credential controls that never echo or serialize raw secrets.
- Trial launch readiness that recognizes accepted credential sources while
  preserving fake/real separation.
- Account/cloud/token-broker strategy docs without runtime production OAuth,
  billing, or SnapLex Cloud.

Deliverables:

- `docs/p10_credential_strategy_decisions.md`
- `docs/p10_secure_storage_notes.md`
- `docs/p10_account_strategy.md`
- `docs/p10_smoke_evidence.md`
- Credential service/store implementation and tests.
- Settings/provider setup integration and tests.
- P10 final validation report and P10 to P11 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Package dry-run remains green.
- Fake/real trial command smoke remains green.
- P9 GUI smoke remains green.
- Credential/store/provider setup tests prove secrets are not serialized,
  echoed, logged, or committed.
- Docs link/index and artifact/secret scans remain green.

Round split:

- Round 1: rebaseline, threat model, and source refresh.
- Round 2: credential domain model.
- Round 3: env credential resolver compatibility.
- Round 4: optional keyring adapter.
- Round 5: credential-aware provider setup.
- Round 6: provider connection integration.
- Round 7: Settings presenter and service integration.
- Round 8: Settings UI secure credential controls.
- Round 9: trial command and CLI readiness.
- Round 10: package and optional dependency boundaries.
- Round 11: account/cloud/token-broker strategy.
- Round 12: credential smoke and documentation.
- Rounds 13-15: buffer hardening.
- Round 16: final validation, report, and P11 handoff.

Executor completion artifacts:

- `docs/p10_credential_strategy_decisions.md`
- `docs/p10_secure_storage_notes.md`
- `docs/p10_account_strategy.md`
- `docs/p10_smoke_evidence.md`
- `docs/p10_final_validation_report.md`
- `docs/p10_to_p11_handoff.md`

Planner acceptance:

- P10 accepted on 2026-07-16 at
  `5a37564993c67dcf9c5bfe5da2ed06a44327874c`.
- Selected next phase: P11 Trial Release Hardening.

## 14. P11 - Trial Release Hardening

Estimated rounds: 12

Execution guide: `docs/p11_trial_release_hardening_goal_guide.md`

Goal: harden SnapLex for a private Windows trial release by validating visible
desktop behavior, manual credential/keyring behavior, packaged trial behavior,
provider onboarding clarity, and release notes while preserving P10 credential
boundaries.

Scope:

- Revalidate the accepted P10 baseline.
- Visible Windows smoke for shell, Settings, History, focus, long text, fake
  warnings, and real/fake trial launch behavior.
- Manual Windows Credential Locker/keyring smoke with a throwaway fake secret
  when the environment supports it.
- Packaged keyring/credential support decision.
- Packaged fake smoke and real-trial fail-closed checks.
- Provider onboarding copy polish.
- Key rotation and least-privilege notes.
- Release smoke checklist and private trial checklist consolidation.

Deliverables:

- `docs/p11_visible_windows_smoke_evidence.md`
- `docs/p11_keyring_smoke_evidence.md`
- `docs/p11_keyring_packaging_decision.md`
- `docs/p11_packaged_trial_evidence.md`
- `docs/p11_provider_onboarding_notes.md`
- `docs/p11_key_rotation_least_privilege.md`
- `docs/p11_private_trial_release_checklist.md`
- `docs/p11_boundary_scan_evidence.md`
- P11 final validation report and P11 to P12 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Package dry-run remains green.
- Fake/real trial command smoke remains green.
- P9 GUI smoke remains green.
- Visible Windows and manual keyring smoke pass or document exact blockers.
- Docs link/index and artifact/secret scans remain green.

Round split:

- Round 1: rebaseline and release-risk audit.
- Round 2: visible Windows GUI smoke.
- Round 3: manual keyring smoke.
- Round 4: packaged credential decision.
- Round 5: packaged trial hardening.
- Round 6: provider onboarding copy.
- Round 7: key rotation and least privilege.
- Round 8: release checklist consolidation.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P12 handoff.

Executor completion artifacts:

- `docs/p11_visible_windows_smoke_evidence.md`
- `docs/p11_keyring_smoke_evidence.md`
- `docs/p11_keyring_packaging_decision.md`
- `docs/p11_packaged_trial_evidence.md`
- `docs/p11_provider_onboarding_notes.md`
- `docs/p11_key_rotation_least_privilege.md`
- `docs/p11_private_trial_release_checklist.md`
- `docs/p11_boundary_scan_evidence.md`
- `docs/p11_final_validation_report.md`
- `docs/p11_to_p12_handoff.md`

Planner acceptance:

- P11 accepted on 2026-07-16 at
  `66d3cef11db492b6c6170c26b69e483528186767`.
- Selected next phase: P12 Private Trial Pilot And Feedback Triage.

## 15. P12 - Private Trial Pilot And Feedback Triage

Estimated rounds: 12

Execution guide: `docs/p12_private_trial_pilot_feedback_triage_goal_guide.md`

Goal: prepare the first controlled private-trial pilot with tester-facing
materials, feedback triage rules, pass/fail criteria, manual environment
checks, optional real-provider smoke policy, and credential package variant
decision notes.

Scope:

- Revalidate the accepted P11 baseline.
- Private-trial release notes for testers.
- Feedback intake template and triage taxonomy.
- First private-trial pass/fail criteria.
- Manual environment checks for assistive technology, DPI scaling,
  multi-monitor behavior, visible GUI, packaged fake smoke, and trial scripts.
- Optional real-provider smoke run/skip policy.
- Credential-capable package variant build/defer/reject decision.
- Private-trial checklist and onboarding doc updates.

Deliverables:

- `docs/p12_private_trial_release_notes.md`
- `docs/p12_feedback_intake_template.md`
- `docs/p12_trial_pass_fail_criteria.md`
- `docs/p12_manual_environment_checks.md`
- `docs/p12_real_provider_smoke_decision.md`
- `docs/p12_credential_package_variant_decision.md`
- `docs/p12_trial_triage_workflow.md`
- `docs/p12_boundary_scan_evidence.md`
- P12 final validation report and P12 to P13 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Package dry-run remains green.
- Fake/real trial command smoke remains green.
- P9 and P11 GUI smoke remain green.
- Docs link/index and artifact/secret scans remain green.

Round split:

- Round 1: rebaseline and pilot scope.
- Round 2: tester-facing release notes.
- Round 3: feedback intake template.
- Round 4: pass/fail criteria.
- Round 5: manual environment checks.
- Round 6: optional real-provider smoke decision.
- Round 7: credential package variant decision.
- Round 8: trial triage workflow.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P13 handoff.

Executor completion artifacts:

- `docs/p12_private_trial_release_notes.md`
- `docs/p12_feedback_intake_template.md`
- `docs/p12_trial_pass_fail_criteria.md`
- `docs/p12_manual_environment_checks.md`
- `docs/p12_real_provider_smoke_decision.md`
- `docs/p12_credential_package_variant_decision.md`
- `docs/p12_trial_triage_workflow.md`
- `docs/p12_boundary_scan_evidence.md`
- `docs/p12_final_validation_report.md`
- `docs/p12_to_p13_handoff.md`

Planner acceptance:

- P12 accepted on 2026-07-16 at
  `1b5c690b4c974c254b9d45d63a78ec4b11a4d583`.
- Selected next phase: P13 Private Trial Feedback Response And Credential
  Package Feasibility.

## 16. P13 - Private Trial Feedback Response And Credential Package Feasibility

Estimated rounds: 12

Execution guide:
`docs/p13_private_trial_feedback_response_credential_package_feasibility_goal_guide.md`

Goal: respond to the first private-trial feedback loop, close accepted S0/S1
pilot blockers when they are safe and deterministic, capture remaining manual
environment results or blockers, and decide whether a credential-capable
package variant is feasible for a later explicit phase.

Scope:

- Revalidate the accepted P12 baseline.
- Create a private-trial feedback response log.
- Triage supplied tester feedback, or explicitly record that no external
  feedback was supplied and process P12 known gaps as internal pilot blockers.
- Close accepted S0/S1 pilot blockers with deterministic validation, or record
  blockers.
- Capture assistive-technology, DPI, and multi-monitor manual results or
  blockers.
- Record optional real-provider smoke run/skip evidence.
- Record source keyring smoke pass/blocker evidence with only a throwaway fake
  value when optional credentials support is available.
- Decide credential-capable package feasibility for a later explicit phase.

Deliverables:

- `docs/p13_feedback_response_log.md`
- `docs/p13_s0_s1_blocker_resolution.md`
- `docs/p13_manual_environment_results.md`
- `docs/p13_real_provider_smoke_record.md`
- `docs/p13_keyring_source_smoke_record.md`
- `docs/p13_credential_package_feasibility.md`
- `docs/p13_boundary_scan_evidence.md`
- `docs/p13_final_validation_report.md`
- `docs/p13_to_p14_handoff.md`

Round 8 executor status:

- No external tester feedback was supplied; P13 processes P12 known gaps as
  internal pilot blockers instead of fabricating reports.
- No accepted S0/S1 code repair exists; closure evidence is recorded in
  `docs/p13_s0_s1_blocker_resolution.md`.
- Manual AT/DPI/multi-monitor results are recorded as blockers in
  `docs/p13_manual_environment_results.md`.
- Real-provider smoke is intentionally skipped without local credentials and
  explicit network approval; fail-closed evidence is recorded in
  `docs/p13_real_provider_smoke_record.md`.
- Source keyring smoke is blocked by missing optional `keyring`; feasibility
  remains deferred in `docs/p13_keyring_source_smoke_record.md` and
  `docs/p13_credential_package_feasibility.md`.

Final executor status:

- `docs/p13_boundary_scan_evidence.md` records artifact and secret scan PASS.
- `docs/p13_final_validation_report.md` records the final validation matrix.
- `docs/p13_to_p14_handoff.md` recommends P14 Manual Environment And Source
  Keyring Validation before any credential-capable package spike.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Package dry-run remains green.
- Fake/real trial command smoke remains green.
- P9 and P11 GUI smoke remain green.
- Docs link/index and artifact/secret scans remain green.

Round split:

- Round 1: rebaseline and feedback source inventory.
- Round 2: triage and S0/S1 decision.
- Round 3: first accepted blocker fix or closure.
- Round 4: manual AT/DPI/multi-monitor evidence.
- Round 5: optional real-provider smoke record.
- Round 6: source keyring smoke record.
- Round 7: credential package feasibility.
- Round 8: feedback response closure.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P14 handoff.

Planner acceptance:

- P13 accepted on 2026-07-16 at
  `9ec029c9d72354fac768a558ddb70881622475ca`.
- Selected next phase: P14 Manual Environment And Source Keyring Validation.

## 17. P14 - Manual Environment And Source Keyring Validation

Estimated rounds: 12

Execution guide: `docs/p14_manual_environment_source_keyring_validation_goal_guide.md`

Goal: collect target-device manual environment evidence, run source keyring
smoke when optional credential support is available, keep real-provider smoke
optional and human-approved, and decide whether to authorize a later isolated
credential-capable package spike.

Scope:

- Revalidate the accepted P13 baseline.
- Create a tester feedback intake log and record whether external tester
  feedback is available.
- Run or document blockers for assistive-technology checks.
- Run or document blockers for DPI scaling checks.
- Run or document blockers for multi-monitor checks.
- Install optional source credential support when feasible and record keyring
  dependency/backend status.
- Run source keyring save/read/delete smoke with only a throwaway fake value
  when feasible, or document the blocker.
- Record optional real-provider smoke run/skip evidence.
- Decide whether evidence justifies a later isolated credential-capable package
  spike.

Deliverables:

- `docs/p14_tester_feedback_intake_log.md`
- `docs/p14_manual_at_dpi_multimonitor_results.md`
- `docs/p14_source_keyring_smoke_evidence.md`
- `docs/p14_real_provider_smoke_record.md`
- `docs/p14_credential_package_spike_decision.md`
- `docs/p14_boundary_scan_evidence.md`
- P14 final validation report and P14 to P15 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Package dry-run remains green.
- Fake/real trial command smoke remains green.
- P9 and P11 GUI smoke remain green.
- Docs link/index and artifact/secret scans remain green.

Round split:

- Round 1: rebaseline and tester feedback inventory.
- Round 2: assistive-technology validation.
- Round 3: DPI scaling validation.
- Round 4: multi-monitor validation.
- Round 5: optional credential dependency setup.
- Round 6: source keyring smoke.
- Round 7: optional real-provider smoke record.
- Round 8: credential package spike decision.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P15 handoff.

Executor completion:

- P14 completed on 2026-07-16 and is ready for planner acceptance.
- External tester feedback was not supplied.
- AT/DPI/multi-monitor checks remain honest manual blockers.
- Source keyring save/read/delete passed with a throwaway fake value.
- Real-provider network smoke remained skipped without credentials and explicit
  approval; real trial paths fail closed.
- A later isolated credential-capable package spike is recommended, but no
  package credential implementation was added or promised.
- Closure package: `docs/p14_boundary_scan_evidence.md`,
  `docs/p14_final_validation_report.md`, and `docs/p14_to_p15_handoff.md`.

Planner acceptance:

- P14 accepted on 2026-07-16 at
  `1f7c3e388e01fb4514f8d08b8d3978feb14727e3`.
- Selected next phase: P15 Isolated Credential-Capable Package Spike Design
  Gate.

## 18. P15 - Isolated Credential-Capable Package Spike Design Gate

Estimated rounds: 12

Execution guide:
`docs/p15_isolated_credential_package_spike_design_gate_goal_guide.md`

Goal: run an isolated package spike for credential-capable packaging while
preserving the deterministic base package path.

Scope:

- Revalidate the accepted P14 baseline.
- Design the explicit credential-capable package spike boundary.
- Audit optional dependency and package variant behavior.
- Prove or reject packaged keyring import/backend discovery.
- Prove or reject packaged credential save/read/delete/cleanup with only a
  throwaway fake value.
- Prove or reject packaged restart readiness without displaying or printing the
  throwaway value.
- Preserve deterministic base package dry-run and fake package smoke.
- Document cleanup guidance for local throwaway/manual credentials and smoke
  data.
- Decide whether to promote, defer, or reject a later production
  credential-capable package hardening phase.

Deliverables:

- `docs/p15_packaging_spike_design.md`
- `docs/p15_packaged_keyring_import_evidence.md`
- `docs/p15_packaged_credential_smoke_evidence.md`
- `docs/p15_packaged_restart_readiness.md`
- `docs/p15_credential_cleanup_guidance.md`
- `docs/p15_package_spike_decision.md`
- `docs/p15_boundary_scan_evidence.md`
- P15 final validation report and P15 to P16 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Base package dry-run remains green.
- Credential-capable package spike build/dry-run has pass/fail/blocker
  evidence when feasible.
- Fake/real trial command smoke remains green.
- Packaged real trial remains fail-closed without real provider configuration.
- Docs link/index and artifact/secret scans remain green.

Round split:

- Round 1: rebaseline and package spike boundary.
- Round 2: packaging optional dependency audit.
- Round 3: packaged keyring import evidence.
- Round 4: packaged credential save/read/delete smoke.
- Round 5: packaged restart readiness.
- Round 6: base package preservation.
- Round 7: cleanup guidance.
- Round 8: spike decision.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P16 handoff.

Executor completion:

- P15 completed on 2026-07-16 and was accepted by planner review on
  2026-07-17.
- Explicit `credentials` package variant added and validated.
- Packaged keyring import/backend discovery passed.
- Packaged credential save/read/delete/cleanup passed with runtime-generated
  throwaway values.
- Packaged restart readiness passed across two packaged processes.
- Base package remained deterministic and rejects credential smoke because
  keyring is unavailable in that runtime.
- Decision: promote to later production hardening phase, not a production
  release promise.
- Closure package: `docs/p15_boundary_scan_evidence.md`,
  `docs/p15_final_validation_report.md`, and `docs/p15_to_p16_handoff.md`.

Planner acceptance:

- P15 accepted at `8e920c7c70155095cee92df86867535c98993220`.
- Selected next phase: P16 Credential-Capable Package Production Hardening.

## 19. P16 - Credential-Capable Package Production Hardening

Estimated rounds: 12

Execution guide:
`docs/p16_credential_capable_package_production_hardening_goal_guide.md`

Goal: harden the explicit credential-capable package path for a production
decision while preserving the deterministic base package.

Scope:

- Revalidate the accepted P15 baseline.
- Preserve deterministic base package behavior and prove keyring remains
  excluded from base.
- Harden the explicit `credentials` package variant.
- Harden `--smoke-credentials` modes, output, exit codes, restart readiness,
  and no-secret guarantees.
- Produce tester-facing setup, failure, and cleanup documentation.
- Document or harden missing, unavailable, locked, unsupported, and cleanup
  failure states for keyring backends.
- Define signed/unsigned build gates, artifact handling, manual smoke evidence,
  and support boundaries.
- Decide whether the credential-capable package path is ready for limited
  private tester distribution, needs another hardening phase, or remains
  deferred.

Deliverables:

- `docs/p16_base_package_preservation_evidence.md`
- `docs/p16_credentials_variant_hardening.md`
- `docs/p16_credential_smoke_hardening.md`
- `docs/p16_tester_setup_cleanup_guide.md`
- `docs/p16_keyring_failure_modes.md`
- `docs/p16_release_gate_artifact_policy.md`
- `docs/p16_production_hardening_decision.md`
- `docs/p16_boundary_scan_evidence.md`
- P16 final validation report and P16 to P17 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Base and credentials package dry-runs pass.
- Base package remains deterministic and rejects credential smoke.
- Credentials package smoke covers import, cycle, save/check-delete restart
  readiness, and cleanup when feasible.
- Fake/real trial command smoke remains green and real trial paths fail closed.
- P9 and P11 GUI smoke remain green.
- Docs link/index and artifact/secret scans remain green.

Round split:

- Round 1: rebaseline and hardening acceptance.
- Round 2: base package preservation gate.
- Round 3: credentials variant build/dependency gate.
- Round 4: credential smoke command hardening.
- Round 5: tester setup and cleanup docs.
- Round 6: keyring failure modes and support policy.
- Round 7: release gate and artifact policy.
- Round 8: production hardening decision.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P17 handoff.

Executor completion:

- P16 completed on 2026-07-17 and was accepted by planner review on
  2026-07-17.
- Base package remains deterministic and keyring-free.
- Explicit `credentials` variant remains the only credential-capable package
  path.
- Credential smoke uses phase-neutral reference
  `snaplex/package-credential-smoke`.
- Packaged credential import/cycle/save/check-delete passed.
- Keyring backend/store failures are wrapped without raw value leakage.
- Tester setup/cleanup, keyring failure modes, release gate/artifact policy,
  and production hardening decision are documented.
- Decision: approve limited private tester credential package candidate under
  P16 gates; public release and signed installer remain out of scope.
- Closure package: `docs/p16_boundary_scan_evidence.md`,
  `docs/p16_final_validation_report.md`, and `docs/p16_to_p17_handoff.md`.

Planner acceptance:

- P16 accepted at `d50cd949178adf78a0d54b3dd1ed8159d42770f3`.
- Selected next phase: P17 Limited Credential Package Pilot And Signing
  Decision.

## 20. P17 - Limited Credential Package Pilot And Signing Decision

Estimated rounds: 12

Execution guide:
`docs/p17_limited_credential_package_pilot_signing_decision_goal_guide.md`

Goal: run a controlled private tester lane for the explicit unsigned
`credentials` package candidate and decide signing, installer, updater,
artifact transfer, retention, support escalation, and variant policy.

Scope:

- Revalidate the accepted P16 baseline.
- Define controlled private tester lane and pre-share package gates.
- Build or rehearse explicit credentials package candidate gates from a clean
  source commit.
- Preserve deterministic base package validation.
- Collect no-secret tester feedback or record honest blockers/absence.
- Record optional real-provider smoke only with explicit human network
  approval and existing local credentials.
- Decide whether credentials stay as a separate package variant.
- Decide signing, installer, updater, artifact transfer, retention, and support
  escalation requirements.

Deliverables:

- `docs/p17_pilot_lane_plan.md`
- `docs/p17_package_candidate_gate_evidence.md`
- `docs/p17_tester_feedback_intake.md`
- `docs/p17_real_provider_smoke_record.md`
- `docs/p17_artifact_transfer_retention_support.md`
- `docs/p17_signing_installer_updater_decision.md`
- `docs/p17_credential_package_lane_decision.md`
- `docs/p17_boundary_scan_evidence.md`
- P17 final validation report and P17 to P18 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Base and credentials package dry-runs pass.
- Base package remains deterministic and rejects credential smoke.
- Credentials package smoke covers import, cycle, save/check-delete restart
  readiness, and cleanup when feasible.
- Fake/real trial command smoke remains green and real trial paths fail closed.
- P9 and P11 GUI smoke remain green.
- Docs link/index and artifact/secret scans remain green.

Round split:

- Round 1: rebaseline and pilot lane.
- Round 2: package candidate pre-share gate.
- Round 3: tester instructions and feedback intake.
- Round 4: tester feedback or blocker record.
- Round 5: optional real-provider smoke decision.
- Round 6: artifact transfer, retention, and support policy.
- Round 7: signing, installer, and updater decision.
- Round 8: credential package lane decision.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P18 handoff.

Executor completion:

- P17 completed on 2026-07-17 and was accepted by planner review on
  2026-07-17.
- Controlled credential package pilot lane, pre-share gate evidence,
  no-secret tester intake, real-provider smoke skip record, artifact
  transfer/retention/support policy, signing/installer/updater decision, and
  credential package lane decision are documented.
- Credentials package build/import/cycle/save/check-delete passed.
- Final base package restore passed, and base credential smoke still rejects
  keyring as unavailable.
- External tester feedback and real-provider network smoke were not supplied.
- Decision: keep credentials as a separate explicit unsigned private-trial
  variant; defer signing, installer, updater, and broader distribution.
- Closure package: `docs/p17_boundary_scan_evidence.md`,
  `docs/p17_final_validation_report.md`, and `docs/p17_to_p18_handoff.md`.

Recommended next phase: P18 Signing And Distribution Readiness Gate.

Planner acceptance:

- P17 accepted at `6c7061ad21cbd7b384806a3466f7c31adf8399db`.
- Selected next phase: P18 Signing And Distribution Readiness Gate.

## 21. P18 - Signing And Distribution Readiness Gate

Estimated rounds: 12

Execution guide:
`docs/p18_signing_distribution_readiness_gate_goal_guide.md`

Goal: decide signing and distribution readiness before broader credential
package distribution.

Scope:

- Revalidate the accepted P17 baseline.
- Define signing identity and certificate custody requirements.
- Define signing command, verification evidence, and revocation expectations.
- Decide archive versus installer readiness.
- Define rollback/update expectations without implementing updater runtime.
- Define signed artifact naming, transfer, retention, and support escalation.
- Optionally run a safe local signing rehearsal only when no real private keys
  or signed artifacts enter git.
- Preserve deterministic base package validation.
- Preserve explicit credentials package validation.

Deliverables:

- `docs/p18_signing_identity_certificate_custody.md`
- `docs/p18_signing_verification_policy.md`
- `docs/p18_signing_rehearsal_record.md`
- `docs/p18_archive_installer_readiness_decision.md`
- `docs/p18_rollback_update_policy.md`
- `docs/p18_artifact_retention_revocation_support.md`
- `docs/p18_distribution_readiness_decision.md`
- `docs/p18_boundary_scan_evidence.md`
- `docs/p18_package_validation_evidence.md`
- P18 final validation report and P18 to P19 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Base and credentials package dry-runs pass.
- Base package remains deterministic and rejects credential smoke.
- Credentials package smoke covers import, cycle, save/check-delete restart
  readiness, and cleanup when feasible.
- Fake/real trial command smoke remains green and real trial paths fail closed.
- P9 and P11 GUI smoke remain green.
- Docs link/index and artifact/secret/private-key scans remain green.

Round split:

- Round 1: rebaseline and signing readiness questions.
- Round 2: signing identity and certificate custody policy.
- Round 3: signing command and verification evidence policy.
- Round 4: optional signing rehearsal decision and record.
- Round 5: archive-versus-installer readiness decision.
- Round 6: rollback/update expectations.
- Round 7: artifact retention, revocation, and support escalation.
- Round 8: distribution readiness decision.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P19 handoff.

Executor completion:

- P18 completed at `9055bd7c565b3965b22bb267aebdd5ae7f8b1aa6`.
- P18 preserved base and credentials package separation.
- P18 recorded signing rehearsal as SKIPPED because no approved safe
  throwaway/test signing path was supplied.
- P18 did not create a public release, signed artifact, installer, updater, or
  production certificate path.
- P18 closure is recorded in `docs/p18_final_validation_report.md` and
  `docs/p18_to_p19_handoff.md`.

Planner acceptance:

- P18 accepted at `9055bd7c565b3965b22bb267aebdd5ae7f8b1aa6`.
- Selected next phase: P19 Signing Rehearsal And Signed Archive Candidate Gate.

## 22. P19 - Signing Rehearsal And Signed Archive Candidate Gate

Estimated rounds: 12

Execution guide:
`docs/p19_signing_rehearsal_signed_archive_candidate_gate_goal_guide.md`

Goal: decide whether a safe isolated signing rehearsal can run, and gate any
signed archive candidate without becoming a public release.

Scope:

- Revalidate the accepted P18 baseline.
- Decide whether an approved safe throwaway/test signing path exists.
- Run any approved signing rehearsal only in ignored local artifact paths.
- Record SKIPPED or BLOCKED honestly when no safe signing path is available.
- Preserve deterministic base package validation.
- Preserve explicit credentials package validation.
- Define signature verification, trust, timestamp, cleanup, stop-condition,
  rollback, support, and revocation expectations.
- Preserve no-secret and no-artifact repository hygiene.

Deliverables:

- `docs/p19_signing_path_decision.md`
- `docs/p19_base_package_control_evidence.md`
- `docs/p19_credentials_package_candidate_evidence.md`
- `docs/p19_signing_rehearsal_evidence.md`
- `docs/p19_signature_verification_policy.md`
- `docs/p19_signed_archive_stop_conditions.md`
- `docs/p19_signed_archive_candidate_decision.md`
- `docs/p19_boundary_scan_evidence.md`
- P19 final validation report and P19 to P20 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Base and credentials package dry-runs pass.
- Base package remains deterministic and rejects credential smoke.
- Credentials package smoke covers import, cycle, save/check-delete restart
  readiness, and cleanup when feasible.
- Fake/real trial command smoke remains green and real trial paths fail closed.
- P9 and P11 GUI smoke remain green.
- Any signing rehearsal uses only approved throwaway/test material in ignored
  local artifact paths.
- Docs link/index and artifact/secret/private-key/certificate/signing-material
  scans remain green.

Round split:

- Round 1: rebaseline P18 and signing approval inputs.
- Round 2: signing path decision.
- Round 3: base package control lane.
- Round 4: credentials package candidate lane.
- Round 5: signing rehearsal run or SKIPPED/BLOCKED record.
- Round 6: signature verification, trust, timestamp, and evidence policy.
- Round 7: signed archive stop conditions, cleanup, and rollback implications.
- Round 8: signed archive candidate decision.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P20 handoff.

Executor completion:

- P19 completed at `11001b64a4b5e093c7ee57615e7e5dbbb288749f`.
- P19 preserved base and credentials package separation.
- P19 recorded signing rehearsal as SKIPPED because no approved safe
  throwaway/test signing path was supplied.
- P19 did not run signing commands, create signed artifacts, introduce a
  production certificate path, or approve public release.
- P19 closure is recorded in `docs/p19_final_validation_report.md` and
  `docs/p19_to_p20_handoff.md`.

Planner acceptance:

- P19 accepted at `11001b64a4b5e093c7ee57615e7e5dbbb288749f`.
- Selected next phase: P20 Approved Signing Path Acquisition And Rehearsal
  Setup Gate.

## 23. P20 - Approved Signing Path Acquisition And Rehearsal Setup Gate

Estimated rounds: 12

Execution guide:
`docs/p20_approved_signing_path_acquisition_rehearsal_setup_gate_goal_guide.md`

Goal: decide whether a safe signing path has explicit approval, then either
prepare an isolated local rehearsal or keep signing blocked.

Scope:

- Revalidate the accepted P19 baseline.
- Decide whether safe signing-path approval exists.
- Define required approval inputs, ignored local artifact directories, cleanup,
  evidence retention, command discovery, verification, timestamp, trust, and
  revocation rules.
- Run signing only if approval and safety inputs are explicit.
- Preserve deterministic base package validation.
- Preserve explicit credentials package validation.
- Preserve no-secret and no-artifact repository hygiene.

Deliverables:

- `docs/p20_signing_path_approval_record.md`
- `docs/p20_rehearsal_artifact_directory_policy.md`
- `docs/p20_signing_command_discovery.md`
- `docs/p20_isolated_rehearsal_evidence.md`
- `docs/p20_signature_verification_evidence_policy.md`
- `docs/p20_base_package_control_evidence.md`
- `docs/p20_credentials_package_control_evidence.md`
- `docs/p20_boundary_scan_evidence.md`
- P20 final validation report and P20 to P21 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Base and credentials package dry-runs pass.
- Base package remains deterministic and rejects credential smoke.
- Credentials package smoke covers import, cycle, save/check-delete restart
  readiness, and cleanup when feasible.
- Fake/real trial command smoke remains green and real trial paths fail closed.
- P9 and P11 GUI smoke remain green.
- Any signing rehearsal uses only explicit approval, ignored local artifact
  paths, and non-secret evidence.
- Docs link/index and artifact/secret/private-key/certificate/signing-material
  scans remain green.

Round split:

- Round 1: rebaseline P19 and package lanes.
- Round 2: signing-path approval decision.
- Round 3: artifact directory, cleanup, and evidence retention policy.
- Round 4: command discovery and rehearsal command shape.
- Round 5: approved rehearsal run or BLOCKED/SKIPPED record.
- Round 6: verification, trust, timestamp, and revocation evidence handling.
- Round 7: base package control lane.
- Round 8: credentials package control lane.
- Rounds 9-11: buffer hardening.
- Round 12: final validation, report, and P21 handoff.

Executor completion:

- P20 completed at `0821a109c683e763997ca116c74ffbe2fddfbde9`.
- P20 preserved base and credentials package separation.
- P20 recorded signing path approval as BLOCKED/SKIPPED because no explicit
  safe throwaway/test signing path approval was supplied.
- P20 did not run signing commands, create/import/purchase/invent/use
  certificates, call timestamp services, create signed artifacts, or approve
  public release.
- P20 closure is recorded in `docs/p20_final_validation_report.md` and
  `docs/p20_to_p21_handoff.md`.

Planner acceptance:

- P20 accepted at `0821a109c683e763997ca116c74ffbe2fddfbde9`.
- Selected next phase: P21 Signing Path Unblock Decision Or Pause Gate.

## 24. P21 - Signing Path Unblock Decision Or Pause Gate

Estimated rounds: 8

Execution guide:
`docs/p21_signing_path_unblock_decision_pause_gate_goal_guide.md`

Goal: decide whether signing is unblocked for a later rehearsal or paused until
human approval and tooling inputs are supplied.

Scope:

- Revalidate the accepted P20 baseline.
- Decide whether safe signing-path approval exists.
- Record APPROVED for later rehearsal or PAUSED with exact unblock inputs.
- Recommend the next phase based on the decision.
- Preserve deterministic base package validation.
- Preserve explicit credentials package validation.
- Preserve no-secret and no-artifact repository hygiene.

Deliverables:

- `docs/p21_signing_path_decision.md`
- `docs/p21_signing_unblock_requirements.md`
- `docs/p21_next_phase_recommendation.md`
- `docs/p21_base_package_control_evidence.md`
- `docs/p21_credentials_package_control_evidence.md`
- `docs/p21_boundary_scan_evidence.md`
- P21 final validation report and P21 to P22 handoff.

Validation:

- Full project validation wrapper passes.
- Version/no-GUI bootstrap passes.
- Real-provider readiness rejects missing real setup clearly.
- Base and credentials package dry-runs pass.
- Base package remains deterministic and rejects credential smoke.
- Credentials package smoke covers import, cycle, save/check-delete restart
  readiness, and cleanup when feasible.
- Fake/real trial command smoke remains green and real trial paths fail closed.
- No signing command runs.
- Docs link/index and artifact/secret/private-key/certificate/signing-material
  scans remain green.

Round split:

- Round 1: rebaseline P20 and package lanes.
- Round 2: signing-path approval decision.
- Round 3: pause/unblock requirements and next-phase recommendation.
- Round 4: base package control lane.
- Round 5: credentials package control lane.
- Round 6: boundary and signing-material scans.
- Round 7: buffer for docs, links, or decision clarity.
- Round 8: final validation, report, and P22 handoff.
