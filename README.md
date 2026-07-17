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
- `docs/p1_core_pipeline_goal_guide.md`
- `docs/p2_clipboard_translation_goal_guide.md`
- `docs/p0_to_p1_handoff.md`
- `docs/p1_to_p2_handoff.md`
- `docs/p2_final_validation_report.md`
- `docs/p2_to_p3_handoff.md`
- `docs/p3_screen_capture_ocr_goal_guide.md`
- `docs/p3_final_validation_report.md`
- `docs/p3_to_p4_handoff.md`
- `docs/p4_provider_hardening_goal_guide.md`
- `docs/p4_provider_configuration.md`
- `docs/p4_final_validation_report.md`
- `docs/p4_to_p5_handoff.md`
- `docs/p5_history_persistence_settings_goal_guide.md`
- `docs/p5_privacy_and_storage.md`
- `docs/p5_final_validation_report.md`
- `docs/p5_to_p6_handoff.md`
- `docs/p6_packaging_release_goal_guide.md`
- `docs/p6_final_validation_report.md`
- `docs/p6_to_p7_handoff.md`
- `docs/p6_packaging_smoke_evidence.md`
- `docs/p6_release_checklist.md`
- `docs/p7_expansion_track_goal_guide.md`
- `docs/p7_expansion_requirements.md`
- `docs/p7_multilingual_ux_plan.md`
- `docs/p7_ai_summary_design.md`
- `docs/p7_browser_extension_bridge.md`
- `docs/p7_expansion_roadmap.md`
- `docs/p7_final_validation_report.md`
- `docs/p0_p7_final_report.md`
- `docs/p7_to_p8_handoff.md`
- `docs/p8_provider_setup_real_translation_goal_guide.md`
- `docs/p8_todo.md`
- `docs/p8_provider_setup_decisions.md`
- `docs/p8_real_provider_trial_notes.md`
- `docs/p8_final_validation_report.md`
- `docs/p8_to_p9_handoff.md`
- `docs/p9_apple_inspired_ui_ux_goal_guide.md`
- `docs/p9_todo.md`
- `docs/p9_ui_audit.md`
- `docs/p9_visual_smoke_evidence.md`
- `docs/p9_hardening_notes.md`
- `docs/p9_final_validation_report.md`
- `docs/p9_to_p10_handoff.md`
- `docs/p10_secure_credential_account_strategy_goal_guide.md`
- `docs/p10_todo.md`
- `docs/p10_credential_strategy_decisions.md`
- `docs/p10_secure_storage_notes.md`
- `docs/p10_account_strategy.md`
- `docs/p10_smoke_evidence.md`
- `docs/p10_final_validation_report.md`
- `docs/p10_to_p11_handoff.md`
- `docs/p11_trial_release_hardening_goal_guide.md`
- `docs/p11_todo.md`
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
- `docs/p12_private_trial_pilot_feedback_triage_goal_guide.md`
- `docs/p12_todo.md`
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
- `docs/p13_private_trial_feedback_response_credential_package_feasibility_goal_guide.md`
- `docs/p13_todo.md`
- `docs/p13_feedback_response_log.md`
- `docs/p13_s0_s1_blocker_resolution.md`
- `docs/p13_manual_environment_results.md`
- `docs/p13_real_provider_smoke_record.md`
- `docs/p13_keyring_source_smoke_record.md`
- `docs/p13_credential_package_feasibility.md`
- `docs/p13_boundary_scan_evidence.md`
- `docs/p13_final_validation_report.md`
- `docs/p13_to_p14_handoff.md`
- `docs/p14_manual_environment_source_keyring_validation_goal_guide.md`
- `docs/p14_todo.md`
- `docs/p14_tester_feedback_intake_log.md`
- `docs/p14_manual_at_dpi_multimonitor_results.md`
- `docs/p14_source_keyring_smoke_evidence.md`
- `docs/p14_real_provider_smoke_record.md`
- `docs/p14_credential_package_spike_decision.md`
- `docs/p14_boundary_scan_evidence.md`
- `docs/p14_final_validation_report.md`
- `docs/p14_to_p15_handoff.md`
- `docs/p15_isolated_credential_package_spike_design_gate_goal_guide.md`
- `docs/p15_todo.md`
- `docs/p15_packaging_spike_design.md`
- `docs/p15_packaged_keyring_import_evidence.md`
- `docs/p15_packaged_credential_smoke_evidence.md`
- `docs/p15_packaged_restart_readiness.md`
- `docs/p15_credential_cleanup_guidance.md`
- `docs/p15_package_spike_decision.md`
- `docs/p15_boundary_scan_evidence.md`
- `docs/p15_final_validation_report.md`
- `docs/p15_to_p16_handoff.md`
- `docs/p16_credential_capable_package_production_hardening_goal_guide.md`
- `docs/p16_todo.md`
- `docs/p16_base_package_preservation_evidence.md`
- `docs/p16_credentials_variant_hardening.md`
- `docs/p16_credential_smoke_hardening.md`
- `docs/p16_tester_setup_cleanup_guide.md`
- `docs/p16_keyring_failure_modes.md`
- `docs/p16_release_gate_artifact_policy.md`
- `docs/p16_production_hardening_decision.md`
- `docs/p16_boundary_scan_evidence.md`
- `docs/p16_final_validation_report.md`
- `docs/p16_to_p17_handoff.md`
- `docs/p17_limited_credential_package_pilot_signing_decision_goal_guide.md`
- `docs/p17_todo.md`
- `docs/p17_pilot_lane_plan.md`
- `docs/p17_package_candidate_gate_evidence.md`
- `docs/p17_tester_feedback_intake.md`
- `docs/p17_real_provider_smoke_record.md`
- `docs/p17_artifact_transfer_retention_support.md`
- `docs/p17_signing_installer_updater_decision.md`
- `docs/p17_credential_package_lane_decision.md`
- `docs/p17_boundary_scan_evidence.md`
- `docs/p17_final_validation_report.md`
- `docs/p17_to_p18_handoff.md`
- `docs/p3_windows_smoke_evidence.md`
- `docs/p3_capture_notes.md`
- `docs/p3_ocr_notes.md`
- `docs/p3_lazy_loading_notes.md`
- `docs/p2_hotkey_decision.md`
- `docs/p2_windows_smoke_evidence.md`
- `docs/p1_todo.md`
- `docs/p2_todo.md`
- `docs/p3_todo.md`
- `docs/windows_smoke_checklist.md`
- `docs/p0_final_validation_report.md`
- `docs/p4_todo.md`
- `docs/p5_todo.md`
- `docs/p6_todo.md`
- `docs/p7_todo.md`

## Planned Stack

- Python + PySide6 for the desktop shell and floating UI.
- `mss` or `pyautogui` for screen capture.
- PaddleOCR first, with a Tesseract-compatible service boundary.
- Pluggable translation providers for LibreTranslate, OpenAI, DeepL, or local fallback providers.
- PyInstaller for Windows packaging.

## Current Status

SnapLex has accepted P0 through P22. P23 Private Trial Feedback Intake And
Support Loop Gate is in executor validation with feedback intake, no-feedback
disposition, support decisions, package-lane, artifact-retention, and boundary
evidence recorded. The
P0-P7 track is complete with a Windows MVP release baseline and a post-MVP
expansion roadmap. The app now has manual clipboard and screen translation
actions, capture/OCR service boundaries, optional lazy real capture/OCR
adapters, real provider adapters for LibreTranslate/OpenAI/DeepL, mocked HTTP
tests, fake offline defaults, persisted settings, optional recent translation
history, shared result states, a PyInstaller spec, packaged release smoke
commands, post-MVP expansion plans, provider setup UX, Apple-inspired UI
polish, accepted P10 credential/account work, accepted P11 trial release
hardening, accepted P12 private-trial pilot materials, accepted P13 feedback
response evidence, and accepted P14 source keyring validation evidence. P15
adds explicit credential-capable package spike evidence while keeping the base
package deterministic. P16 hardens that explicit package path into a limited
private tester candidate while preserving the deterministic base package. P17
evaluates the controlled credential package pilot lane. P18 through P21 record
signing/distribution gates and keep signing PAUSED because no approved safe
signing path was supplied. P22 refreshes unsigned/private-trial tester
instructions, support intake, feedback triage, artifact retention, package-lane
evidence, and boundary scans without adding runtime features. P23 records that
no external tester feedback was supplied, keeps support intake privacy-safe,
revalidates base and credentials package lanes, and keeps signing paused.

Use `docs/p7_final_validation_report.md`, `docs/p0_p7_final_report.md`, and
`docs/p7_expansion_roadmap.md` for the P7 closure package. P8 Provider Setup
And Real Translation UX is planner-accepted; use
`docs/p8_final_validation_report.md` and `docs/p8_to_p9_handoff.md` for the P8
closure package. P9 Apple-Inspired UI/UX Polish is planner-accepted; use
`docs/p9_final_validation_report.md` and `docs/p9_to_p10_handoff.md` for the
P9 closure package. P10 Secure Credential And Account Strategy is
planner-accepted; use `docs/p10_final_validation_report.md` and
`docs/p10_to_p11_handoff.md`. P11 Trial Release Hardening is planner-accepted;
use `docs/p11_final_validation_report.md` and `docs/p11_to_p12_handoff.md`.
P12 Private Trial Pilot And Feedback Triage is planner-accepted; use
`docs/p12_final_validation_report.md` and `docs/p12_to_p13_handoff.md`. P13 is
planner-accepted; use
`docs/p13_private_trial_feedback_response_credential_package_feasibility_goal_guide.md`
and `docs/p13_todo.md`. P13 feedback response artifacts are recorded in
`docs/p13_feedback_response_log.md`,
`docs/p13_s0_s1_blocker_resolution.md`,
`docs/p13_manual_environment_results.md`,
`docs/p13_real_provider_smoke_record.md`,
`docs/p13_keyring_source_smoke_record.md`, and
`docs/p13_credential_package_feasibility.md`. P13 closure evidence is
`docs/p13_boundary_scan_evidence.md`, `docs/p13_final_validation_report.md`,
and `docs/p13_to_p14_handoff.md`. P14 executor evidence is recorded in
`docs/p14_tester_feedback_intake_log.md`,
`docs/p14_manual_at_dpi_multimonitor_results.md`,
`docs/p14_source_keyring_smoke_evidence.md`,
`docs/p14_real_provider_smoke_record.md`,
`docs/p14_credential_package_spike_decision.md`,
`docs/p14_boundary_scan_evidence.md`,
`docs/p14_final_validation_report.md`, and `docs/p14_to_p15_handoff.md`. P15
executor evidence is recorded in `docs/p15_packaging_spike_design.md`,
`docs/p15_packaged_keyring_import_evidence.md`,
`docs/p15_packaged_credential_smoke_evidence.md`,
`docs/p15_packaged_restart_readiness.md`,
`docs/p15_credential_cleanup_guidance.md`,
`docs/p15_package_spike_decision.md`,
`docs/p15_boundary_scan_evidence.md`,
`docs/p15_final_validation_report.md`, and `docs/p15_to_p16_handoff.md`.

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

Install optional real capture/OCR dependencies only when you want to exercise
those backends:

```powershell
python -m pip install -e ".[capture]"
python -m pip install -e ".[ocr]"
```

Install the optional packaging toolchain when building a local Windows package:

```powershell
python -m pip install -e ".[gui,package]"
```

Install the optional local secure credential dependency only when you want to
save provider keys in the OS keyring:

```powershell
python -m pip install -e ".[gui,credentials]"
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

Clipboard MVP flow:

1. Copy text into the Windows clipboard.
2. Run `python -m snaplex`.
3. Select `Translate Clipboard`.
4. Review the source, translated text, provider, or error state.
5. Use `Copy Result`, `Retry`, or `Close Result`.

Screen MVP flow:

1. Run `python -m snaplex`.
2. Select `Translate Screen`.
3. Drag a non-empty screen region in the overlay, or press `Esc` to cancel.
4. Review the OCR source, translated text, provider, or error state.
5. Use `Copy Result`, `Retry`, or `Close Result`.

The same entry point is exposed as a console script after editable install:

```powershell
snaplex --no-gui
```

## Development Checks

Quick bootstrap checks:

```powershell
python -m compileall snaplex
python -m snaplex --version
python -m snaplex --no-gui
```

Full local validation now runs through the project ops wrapper:

```powershell
C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd
```

The configured validation sequence is:

- `python -m ruff check .`
- `python -m ruff format --check .`
- `python -m mypy snaplex`
- `python -m compileall snaplex`
- `python -m pytest`

## Packaging

Build the deterministic Windows smoke package:

```powershell
python scripts\package_windows.py --variant base
```

Preview the PyInstaller command without building:

```powershell
python scripts\package_windows.py --dry-run --variant base
```

Smoke the packaged executable with fake provider defaults and a local test data
directory:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexPackageSmoke"
.\dist\SnapLex\SnapLex.exe --version
.\dist\SnapLex\SnapLex.exe --no-gui
.\dist\SnapLex\SnapLex.exe --smoke-package
```

The default `base` package includes the GUI runtime and deterministic fake
capture/OCR smoke path. Optional variants can include `mss` and/or PaddleOCR
modules when those dependencies are installed:

```powershell
python scripts\package_windows.py --variant capture
python scripts\package_windows.py --variant ocr
python scripts\package_windows.py --variant full
```

Generated `build\`, `dist\`, local smoke data, OCR model caches, screenshots,
`.env`, provider secrets, and packaged binaries must remain uncommitted. See
`packaging\README.md`, `docs\p6_packaging_smoke_evidence.md`, and
`docs\p6_release_checklist.md`.

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
- `InMemoryTranslationCache`

## Core Translation Pipeline

P1 provides a reusable service boundary for later clipboard and OCR flows:

```python
from snaplex.services import create_default_translation_pipeline

pipeline = create_default_translation_pipeline()
result = pipeline.translate_text("hello", target_lang="es")
```

For UI callers, use the async-friendly boundary:

```python
result = await pipeline.translate_text_async("hello", target_lang="es")
```

Pipeline behavior includes normalization, config-driven provider selection,
fallback order, in-memory cache lookup/write, and expected error mapping.

## Clipboard Translation MVP

P2 adds the first user-facing vertical slice:

- `snaplex/ui/clipboard_presenter.py` owns clipboard translation presentation state.
- `snaplex/ui/app_shell.py` exposes the always-on-top PySide6 shell and result view.
- `snaplex/services/clipboard_service.py` contains the in-memory and Qt clipboard adapters.
- UI calls `TranslationPipeline.translate_text_async(...)`; it does not call providers directly.
- Tests cover clipboard service behavior, presenter states, pipeline integration, retry, copy,
  empty clipboard, timeout, provider failure, fallback exhaustion, unknown provider,
  unsupported language, stale result, and unexpected failure states.

Global Windows hotkey support is deferred for a later phase. P2 accepts the
manual `Translate Clipboard` button as the stable trigger path.

## Screen Capture And OCR MVP

P3 adds the first screen-translation vertical slice:

- `snaplex/ui/region_selector.py` provides a minimal Qt region selector plus
  testable selection presenter.
- `snaplex/services/capture_service.py` contains fake capture and lazy optional
  `MssCaptureService`.
- `snaplex/services/ocr_service.py` contains fake OCR scenarios and lazy optional
  `PaddleOcrService`.
- `snaplex/services/screen_translation_service.py` orchestrates
  capture -> OCR -> `TranslationPipeline`.
- `snaplex/ui/screen_presenter.py` maps screen translation results and failures
  into the shared result view.
- Tests cover fake capture/OCR integration, cancel, invalid region, capture
  failure, OCR unavailable/failure, empty OCR result, translation failure, retry,
  copy, close, and optional dependency lazy-loading.

## Provider Configuration

P4 adds real provider adapters for LibreTranslate, OpenAI, and DeepL behind the
existing `TranslationPipeline`. Fake provider mode remains the default. To select
a real provider locally, set environment variables before launching the GUI:

```powershell
$env:SNAPLEX_PROVIDER = "libretranslate"
$env:SNAPLEX_PROVIDER_ORDER = "libretranslate,fake"
python -m snaplex
```

Use `.env.example` and `docs/p4_provider_configuration.md` for provider-specific
base URLs, API-key env var names, timeout, retry, OpenAI model, and DeepL model
type settings. Do not commit real API keys or local `.env` files.

P8 adds Settings-based provider setup and `Test Connection` behavior. Settings
shows provider readiness and whether configured env vars are present, but it
does not display or store key values. Real trial commands require a real
provider; fake trial commands remain smoke/dev only.

## Settings And History

P5 adds local JSON settings and optional recent translation history. By default,
SnapLex uses `%APPDATA%\SnapLex` on Windows, or a home-directory fallback. For
tests and local smoke, override the data path:

```powershell
$env:SNAPLEX_APP_DATA_DIR = "D:\Temp\SnapLexSmoke"
python -m snaplex
```

The app stores provider selection/order, language defaults, provider endpoints,
API-key environment variable names, timeout/retry settings, model options,
history preferences, and UI preferences. It does not store actual provider API
key values.

History is disabled by default. When enabled in `Settings`, successful clipboard
and screen translations store source text, translated text, provider/language
metadata, flow, timestamp, and entry id. The `History` dialog can copy, delete,
and clear entries. See `docs/p5_privacy_and_storage.md`.

## P7 Expansion Track

P7 is documentation/design-first and does not add runtime product features. It
keeps the accepted P6 package baseline stable while defining post-MVP paths for:

- multilingual UX and localization boundaries,
- optional AI summary as a future `SummaryService` / `SummaryProvider`
  capability,
- browser selection bridge design with explicit trust and privacy boundaries,
- roadmap triage for accepted, deferred, and rejected ideas.

P7 originally recommended localization foundation as the lowest-risk first
post-MVP goal. Trial feedback changed the priority: the selected next goal is
P8 Provider Setup And Real Translation UX, focused on Settings-based provider
setup, fake-versus-real translation clarity, real trial guardrails, and an Apple
HIG-inspired UI foundation. See
`docs/p8_provider_setup_real_translation_goal_guide.md`.

## P8 Provider Setup And Real Translation UX

P8 executor work adds the first real-provider trial UX:

- Settings exposes provider choices, readiness, endpoint/env-var fields, and
  connection testing for fake, LibreTranslate, OpenAI, and DeepL.
- Connection tests run through service/presenter/provider boundaries and are
  covered by mocked HTTP tests.
- Fake provider output is labeled as fake smoke mode, not real translation.
- Real trial launch paths reject missing real provider configuration.
- The main shell and result view have a clearer, restrained UI foundation.

See `docs/p8_final_validation_report.md`, `docs/p8_real_provider_trial_notes.md`,
and `docs/p8_to_p9_handoff.md`.

## P9 Apple-Inspired UI/UX Polish

P9 executor work refines the PySide6 desktop experience for trial use:

- shared visual tokens for spacing, typography, semantic colors, focus, and
  stable controls;
- clearer main-shell action hierarchy, result states, provider identity, and
  fake-mode warnings;
- scrollable/selectable long text regions for OCR/source and translation text;
- tabbed Settings information architecture with explicit labels, tooltips, and
  keyboard flow;
- polished History empty/list/long-entry states;
- region selector status feedback and accessibility metadata;
- screenshot-backed offscreen GUI smoke in `scripts/p9_gui_smoke.py`.

See `docs/p9_final_validation_report.md`, `docs/p9_visual_smoke_evidence.md`,
and `docs/p9_to_p10_handoff.md`.

## P10 Secure Credential And Account Strategy

P10 executor work preserves existing environment-variable provider setup while
adding a credential service boundary and first local secure credential path.
The implementation keeps
provider secrets behind `CredentialService`, stores only env-var names or
keyring identifiers in config, adds optional lazy OS keyring support, updates
Settings credential save/delete/readiness controls, and hardens real/fake trial
readiness. Production account OAuth, SnapLex Cloud, token broker, and billing
remain out of runtime scope for P10.

See `docs/p10_secure_credential_account_strategy_goal_guide.md`,
`docs/p10_credential_strategy_decisions.md`,
`docs/p10_secure_storage_notes.md`, `docs/p10_account_strategy.md`,
`docs/p10_smoke_evidence.md`, `docs/p10_final_validation_report.md`,
`docs/p10_to_p11_handoff.md`, and `docs/p10_todo.md`.

## P11 Trial Release Hardening

P11 planner-accepted work hardens SnapLex for private Windows trial release by
validating visible desktop behavior, manual Windows Credential Locker/keyring
behavior, packaged trial behavior, provider onboarding copy, key
rotation/least-privilege notes, and the private-trial release checklist.

P11 must preserve P10 credential boundaries, deterministic fake smoke paths,
no-network automated tests, and no-secret repository hygiene. It is
release-hardening, not feature expansion.

See `docs/p11_trial_release_hardening_goal_guide.md`,
`docs/p11_visible_windows_smoke_evidence.md`,
`docs/p11_keyring_smoke_evidence.md`,
`docs/p11_keyring_packaging_decision.md`,
`docs/p11_packaged_trial_evidence.md`,
`docs/p11_provider_onboarding_notes.md`,
`docs/p11_key_rotation_least_privilege.md`,
`docs/p11_private_trial_release_checklist.md`,
`docs/p11_boundary_scan_evidence.md`,
`docs/p11_final_validation_report.md`,
`docs/p11_to_p12_handoff.md`, and `docs/p11_todo.md`.

## P12 Private Trial Pilot And Feedback Triage

P12 planner-accepted work prepares the first controlled private-trial pilot by producing
tester-facing release notes, feedback intake templates, pass/fail criteria,
manual environment-check instructions, optional real-provider smoke policy,
credential package variant decision notes, a triage workflow, and boundary
evidence.

P12 must preserve P11/P10 boundaries: deterministic fake smoke, no-network
automated tests, no-secret repository hygiene, credential service boundaries,
and fail-closed real trial paths. It is private-trial operations and feedback
triage, not feature expansion.

See `docs/p12_private_trial_pilot_feedback_triage_goal_guide.md` and
`docs/p12_todo.md`. Pilot operations are captured in
`docs/p12_private_trial_release_notes.md`,
`docs/p12_feedback_intake_template.md`,
`docs/p12_trial_pass_fail_criteria.md`,
`docs/p12_manual_environment_checks.md`,
`docs/p12_real_provider_smoke_decision.md`,
`docs/p12_credential_package_variant_decision.md`, and
`docs/p12_trial_triage_workflow.md`. Boundary evidence is recorded in
`docs/p12_boundary_scan_evidence.md`. The closure package is
`docs/p12_final_validation_report.md` and `docs/p12_to_p13_handoff.md`.

## P13 Private Trial Feedback Response And Credential Package Feasibility

P13 planner-accepted work ran the first private-trial feedback response loop, closed
accepted S0/S1 pilot blockers inside existing boundaries, captured
assistive-technology/DPI/multi-monitor manual results or blockers, recorded
optional real-provider and keyring smoke evidence only when allowed, and decided
that credential-capable package implementation should be deferred to a later
explicit phase.

P13 must preserve P10/P11/P12 boundaries: deterministic fake smoke, no-network
automated tests, no-secret repository hygiene, credential service boundaries,
fail-closed real trial paths, and no broad feature expansion.

See
`docs/p13_private_trial_feedback_response_credential_package_feasibility_goal_guide.md`
and `docs/p13_todo.md`. The Round 8 feedback closure package is
`docs/p13_feedback_response_log.md`,
`docs/p13_s0_s1_blocker_resolution.md`,
`docs/p13_manual_environment_results.md`,
`docs/p13_real_provider_smoke_record.md`,
`docs/p13_keyring_source_smoke_record.md`, and
`docs/p13_credential_package_feasibility.md`. The final P13 executor package is
`docs/p13_boundary_scan_evidence.md`, `docs/p13_final_validation_report.md`,
and `docs/p13_to_p14_handoff.md`.

## P14 Manual Environment And Source Keyring Validation

P14 planner-accepted work collected privacy-safe tester feedback status, recorded
assistive-technology/DPI/multi-monitor blockers honestly, installed optional
source credential support, ran source keyring save/read/delete smoke with a
throwaway fake value, kept real-provider network smoke skipped without
credentials and explicit approval, and decided that a later isolated
credential-capable package spike is justified.

P14 must not implement the credential-capable package variant. It must preserve
P10-P13 boundaries: deterministic fake smoke, no-network automated tests,
no-secret repository hygiene, credential service boundaries, fail-closed real
trial paths, and no broad feature expansion.

See `docs/p14_manual_environment_source_keyring_validation_goal_guide.md`,
`docs/p14_todo.md`, `docs/p14_final_validation_report.md`, and
`docs/p14_to_p15_handoff.md`.

## P15 Isolated Credential-Capable Package Spike Design Gate

P15 executor work ran a narrow package spike for credential-capable packaging
while preserving the deterministic base package path. It added an explicit
`credentials` variant, proved packaged keyring import/backend discovery,
packaged credential save/read/delete, packaged restart readiness, cleanup
guidance, and no-secret/no-network hygiene.

P15 does not ship a production credential-capable package. It promotes the
evidence to a later production hardening phase while keeping real trial paths
fail-closed when no real provider is configured.

See `docs/p15_isolated_credential_package_spike_design_gate_goal_guide.md`,
`docs/p15_todo.md`, `docs/p15_final_validation_report.md`, and
`docs/p15_to_p16_handoff.md`.

## P16 Credential-Capable Package Production Hardening

P16 hardens the explicit credential-capable package path for a production
decision while preserving the deterministic base package. It focuses on the
`credentials` variant, package smoke behavior, tester-facing setup and cleanup
docs, keyring failure modes, release gates, and no-secret/no-network hygiene.
P16 executor work approves a limited private tester credential package
candidate under explicit gates, not a public release.

See `docs/p16_credential_capable_package_production_hardening_goal_guide.md`
and `docs/p16_todo.md`. Current P16 hardening evidence is recorded in
`docs/p16_base_package_preservation_evidence.md`,
`docs/p16_credentials_variant_hardening.md`,
`docs/p16_credential_smoke_hardening.md`,
`docs/p16_tester_setup_cleanup_guide.md`,
`docs/p16_keyring_failure_modes.md`,
`docs/p16_release_gate_artifact_policy.md`,
`docs/p16_production_hardening_decision.md`, and
`docs/p16_boundary_scan_evidence.md`. The P16 closure package is
`docs/p16_final_validation_report.md` and `docs/p16_to_p17_handoff.md`.

## P17 Limited Credential Package Pilot And Signing Decision

P17 prepares and evaluates a controlled private tester lane for the explicit
unsigned `credentials` package candidate. It focuses on pre-share gates,
no-secret feedback, optional human-approved real-provider smoke, artifact
transfer/retention/support policy, and signing/installer/updater decisions.

See `docs/p17_limited_credential_package_pilot_signing_decision_goal_guide.md`
and `docs/p17_todo.md`. Current P17 executor evidence is recorded in
`docs/p17_pilot_lane_plan.md`,
`docs/p17_package_candidate_gate_evidence.md`,
`docs/p17_tester_feedback_intake.md`,
`docs/p17_real_provider_smoke_record.md`,
`docs/p17_artifact_transfer_retention_support.md`,
`docs/p17_signing_installer_updater_decision.md`,
`docs/p17_credential_package_lane_decision.md`, and
`docs/p17_boundary_scan_evidence.md`. The P17 closure package is
`docs/p17_final_validation_report.md` and `docs/p17_to_p18_handoff.md`.

## P18 Signing And Distribution Readiness Gate

P18 decides whether SnapLex is ready to move from an unsigned private-trial
credential package lane toward signed distribution. It covers signing identity,
certificate custody, signing verification, archive-versus-installer policy,
rollback/update expectations, artifact retention/revocation, and support
escalation.

See `docs/p18_signing_distribution_readiness_gate_goal_guide.md`. P18 executor
evidence is recorded in
`docs/p18_signing_identity_certificate_custody.md`,
`docs/p18_signing_verification_policy.md`,
`docs/p18_signing_rehearsal_record.md`,
`docs/p18_archive_installer_readiness_decision.md`,
`docs/p18_rollback_update_policy.md`,
`docs/p18_artifact_retention_revocation_support.md`,
`docs/p18_distribution_readiness_decision.md`, and
`docs/p18_boundary_scan_evidence.md`. Package validation evidence is recorded
in `docs/p18_package_validation_evidence.md`. The P18 closure package is
`docs/p18_final_validation_report.md` and `docs/p18_to_p19_handoff.md`.

## P19 Signing Rehearsal And Signed Archive Candidate Gate

P19 decides whether SnapLex has an approved safe throwaway/test signing path for
an isolated signing rehearsal. If approved, the rehearsal stays in ignored local
artifact paths and records verification evidence without committing
certificates, private keys, signed binaries, package outputs, timestamp
responses, screenshots, logs, or secrets. If no safe path is supplied, P19
records SKIPPED or BLOCKED honestly while preserving deterministic base package
and explicit credentials package lanes.

See `docs/p19_signing_rehearsal_signed_archive_candidate_gate_goal_guide.md`.
P19 executor evidence is recorded in
`docs/p19_signing_path_decision.md`,
`docs/p19_base_package_control_evidence.md`,
`docs/p19_credentials_package_candidate_evidence.md`,
`docs/p19_signing_rehearsal_evidence.md`,
`docs/p19_signature_verification_policy.md`,
`docs/p19_signed_archive_stop_conditions.md`,
`docs/p19_signed_archive_candidate_decision.md`, and
`docs/p19_boundary_scan_evidence.md`. The P19 closure package is
`docs/p19_final_validation_report.md` and `docs/p19_to_p20_handoff.md`.

## P20 Approved Signing Path Acquisition And Rehearsal Setup Gate

P20 decides whether SnapLex has explicit approval for a safe throwaway/test
signing path. If approval exists, it sets up and runs only an isolated local
rehearsal in ignored artifact paths with non-secret evidence. If approval is
missing, it records BLOCKED or SKIPPED and keeps signing commands off.

See `docs/p20_approved_signing_path_acquisition_rehearsal_setup_gate_goal_guide.md`.
P20 executor evidence is recorded in
`docs/p20_signing_path_approval_record.md`,
`docs/p20_rehearsal_artifact_directory_policy.md`,
`docs/p20_signing_command_discovery.md`,
`docs/p20_isolated_rehearsal_evidence.md`,
`docs/p20_signature_verification_evidence_policy.md`,
`docs/p20_base_package_control_evidence.md`,
`docs/p20_credentials_package_control_evidence.md`, and
`docs/p20_boundary_scan_evidence.md`. The P20 closure package is
`docs/p20_final_validation_report.md` and `docs/p20_to_p21_handoff.md`.

## P21 Signing Path Unblock Decision Or Pause Gate

P21 makes an explicit decision after P20: either all safe signing-path approval
inputs exist and can be handed to a later rehearsal phase, or signing work is
paused until a human supplies those inputs. P21 does not run signing commands.

See `docs/p21_signing_path_unblock_decision_pause_gate_goal_guide.md`. P21
executor evidence is recorded in
`docs/p21_signing_path_decision.md`,
`docs/p21_signing_unblock_requirements.md`,
`docs/p21_next_phase_recommendation.md`,
`docs/p21_base_package_control_evidence.md`,
`docs/p21_credentials_package_control_evidence.md`, and
`docs/p21_boundary_scan_evidence.md`. The P21 closure package is
`docs/p21_final_validation_report.md` and `docs/p21_to_p22_handoff.md`.

## P22 Non-Signing Private Trial Continuity And Tester Support Gate

P22 continues unsigned/private-trial readiness while signing is paused. It
refreshes tester instructions, support intake, privacy guidance, feedback
triage, artifact transfer/retention, and package-lane evidence without running
signing commands or adding runtime features.

See `docs/p22_non_signing_private_trial_continuity_tester_support_gate_goal_guide.md`.
P22 executor evidence is recorded in
`docs/p22_unsigned_private_trial_release_notes.md`,
`docs/p22_tester_support_intake.md`,
`docs/p22_feedback_triage_criteria.md`,
`docs/p22_base_package_continuity_evidence.md`,
`docs/p22_credentials_package_continuity_evidence.md`,
`docs/p22_artifact_transfer_retention.md`, and
`docs/p22_boundary_scan_evidence.md`. The P22 closure package is
`docs/p22_final_validation_report.md` and `docs/p22_to_p23_handoff.md`.

## P23 Private Trial Feedback Intake And Support Loop Gate

P23 runs one privacy-safe private-trial feedback/support loop using the P22
support and triage docs. If no external tester feedback is supplied, it records
that honestly; if feedback is supplied, it screens, classifies, and responds
without committing personal data, logs, screenshots, package outputs, or
secrets.

See `docs/p23_private_trial_feedback_intake_support_loop_gate_goal_guide.md`
and `docs/p23_todo.md`.

P23 executor evidence is recorded in
`docs/p23_feedback_intake_log.md`,
`docs/p23_privacy_screen_and_triage.md`,
`docs/p23_support_response_decisions.md`,
`docs/p23_next_action_register.md`,
`docs/p23_base_package_continuity_evidence.md`,
`docs/p23_credentials_package_continuity_evidence.md`,
`docs/p23_artifact_retention_support_evidence.md`, and
`docs/p23_boundary_scan_evidence.md`. The P23 closure package will be
`docs/p23_final_validation_report.md` and `docs/p23_to_p24_handoff.md`.

## Current Boundaries

The current implementation intentionally does not include global hotkeys,
browser extension runtime, AI summary runtime, cloud sync, accounts, production
OAuth, billing, or a hosted token broker. Optional local OS keyring support is
lazy and configured only when requested; real capture/OCR adapters and real
translation providers are present but optional. Fake mode remains the
deterministic default for automated tests and packaged release smoke. Later
phases are staged in `docs/phase_plan.md`.
