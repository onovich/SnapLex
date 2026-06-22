# P5 History, Persistence, and Settings UX Goal Mode Guide

Date: 2026-06-22
Status: execution guide for P5 after accepted P4
Estimated budget: 6 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P5 in goal mode:

```text
Execute SnapLex P5 - History, Persistence, and Settings UX in 6 conversation rounds.

Required reading before code changes:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_goal_mode_execution_guide.md
- docs/p4_final_validation_report.md
- docs/p4_to_p5_handoff.md
- docs/p5_todo.md
- docs/p5_history_persistence_settings_goal_guide.md
- docs/p4_provider_configuration.md
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

P4 is accepted. Build local persistence and settings/history UX on top of the accepted TranslationPipeline, provider runtime config, clipboard flow, and screen flow.

Goal:
Persist user settings and optional recent translation history without storing provider secrets. Settings must feed the existing config/service boundaries, history must be testable without PySide6, and the PySide6 shell should get light, usable settings/history controls without becoming a heavy application.

Rules:
- Stay inside P5 scope. Do not implement PyInstaller packaging, browser extension work, AI summary, OCR/capture rewrites, provider rewrites, or global hotkeys.
- UI must call config/history services; widgets must not duplicate provider, storage, or history rules.
- Do not persist actual OpenAI, DeepL, or LibreTranslate API key values. Persist env var names only.
- Do not commit generated local config files, history files, `.env`, provider request logs, or user data.
- Every round must include Debug self-check, architecture self-check, validation commands and results, commit hash, push result, next-round target, and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to the next round.
```

## 1. Required Context

P4 PASS evidence:

- `docs/p4_final_validation_report.md` is planner-accepted.
- P4 used 7 rounds and 0 buffer rounds.
- P4 delivered provider runtime config, injectable HTTP transport, LibreTranslate/OpenAI/DeepL adapters, retry/fallback hardening, `.env.example`, provider docs, and mocked HTTP tests.
- P4 handoff is `docs/p4_to_p5_handoff.md`.

P5 must reuse these accepted boundaries:

- `snaplex/storage/config.py` owns `AppConfig`, provider runtime config values, and environment config loading.
- `snaplex/services/translation_service.py` owns `TranslationPipeline` and provider fallback.
- `snaplex/providers/config.py` stores env var names and runtime options, not secret values.
- `snaplex/ui/app_shell.py` is the current PySide6 shell entry point.
- `snaplex/ui/translation_result.py`, clipboard presenter, and screen presenter own result states.

## 2. Scope

P5 must complete:

- File-backed local config storage with defaults, atomic-ish writes, malformed-file fallback, and version/migration hooks.
- Persisted provider selection, provider order, source/target language, provider endpoints, API-key env var names, timeout/retry settings, model options, history preferences, and UI preferences.
- Settings service boundary that can load, validate, update, and save settings without PySide6.
- Recent translation history storage with add/list/delete/clear behavior.
- History privacy controls: enabled/disabled setting, max entries, clear all, and no images/screenshots stored.
- Lightweight PySide6 settings controls that update persisted settings and refresh future translations through the existing pipeline/config boundary.
- Lightweight PySide6 history controls that show recent items and support copy/delete/clear.
- Privacy docs and smoke notes for local data paths and cleanup.
- P5 final validation report and P5-to-P6 handoff.

## 3. Non-Scope

Do not implement in P5:

- PyInstaller packaging or packaged-app smoke. These belong to P6.
- Browser extension, AI summary, or post-MVP expansion. These belong to P7.
- Global hotkeys.
- OCR/capture coordinate rewrites or OCR model management.
- New translation provider adapters unless needed only to preserve P4 behavior.
- Cloud sync, accounts, encryption/keychain integration, or remote history.
- Storing raw screenshots, OCR images, provider request logs, or actual API keys.

## 4. Planner Decisions And Assumptions

- Use standard-library JSON files for P5 storage unless the executor documents a clear reason to use something else.
- Default local data directory should be Windows-friendly: `%APPDATA%\SnapLex` when available, with a deterministic fallback under the user home directory for tests/non-Windows.
- Support a test override for the storage directory so automated tests never touch real user data.
- Config files may persist API-key env var names, never API-key values.
- Recent translation history should store text results only: source text, translated text, provider name, source/target language, flow/source type, timestamp, and a stable entry id.
- History should be privacy-first: include an enabled/disabled setting, clear-all path, delete-entry path, and max-entry retention. If the executor chooses default-on history for usability, it must document the privacy rationale and provide an obvious disable/clear path.
- Settings UI should be modest and utilitarian. Prefer a dialog or compact panel over a large redesign of the shell.

## 5. Architecture Boundaries

Hard constraints:

- Storage models and services must be testable without PySide6.
- UI owns controls and rendering only.
- Config storage owns load/save/migration/defaults.
- History storage owns entry lifecycle, retention, and deletion.
- `TranslationPipeline` remains the translation orchestration source of truth.
- Provider adapters continue to read secrets from environment variables only.
- History recording must happen after successful translations through a service boundary, not inside provider adapters.
- Tests must not require real user directories, real network, API keys, visible desktop interaction, or persisted local state outside a temp directory.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P5 History, Persistence, and Settings UX
Round goal:
Completed changes:
Debug self-check:
Architecture self-check:
Validation commands and results:
Commit hash:
Push result:
Buffer consumed:
Risks or blockers:
Next-round target:
```

Progression rules:

- Validation fails: do not commit, do not push, do not move to the next round.
- Validation passes but commit fails: do not move to the next round.
- Commit succeeds but push fails: do not move to the next round.
- Push succeeds: record commit hash and remote branch, then move to the next round.
- Any P5 scope expansion must be explicitly approved by the architect/PM before implementation.

Debug self-check:

- Can the current change be explained by the smallest relevant settings/history workflow?
- Can failures be localized to config model, config file storage, migration, history storage, UI binding, pipeline reload, or docs?
- Are default, missing file, malformed file, save failure, migration, disabled history, retention, delete, clear, and restart states covered where relevant?
- If UI changed, was a repeatable offscreen or documented manual smoke path added?
- If state changed, are export/import boundaries intentionally out of scope or covered?

Architecture self-check:

- Does `AppConfig` remain the configuration source of truth?
- Did UI avoid duplicating provider config, history retention, migration, or storage semantics?
- Are provider secret values still excluded from persisted app config?
- Did this round avoid pulling P6-P7 scope into P5?
- Are unrelated files, generated local app data, `.env`, history data, and user changes left out of git?

## 7. Round Plan

Round 1 - File-backed config storage:

- Add local app data path helpers with temp-directory/test overrides.
- Add JSON file-backed config store with defaults, version field, malformed-file fallback, and migration hooks.
- Preserve P4 provider runtime settings without persisting secret values.
- Add unit tests for missing file, save/load, malformed file, migration, copied mutable fields, and ignored secret values.

Round 2 - Settings service and pipeline wiring:

- Add a settings service boundary for reading/updating provider, language, timeout/retry, model, history, and UI preferences.
- Wire default GUI startup to load persisted config while still allowing environment values where appropriate.
- Ensure future clipboard/screen translations use the updated config through `TranslationPipeline` or a safe pipeline refresh boundary.
- Add tests for update/save/load and fallback to fake provider defaults.

Round 3 - History storage and service:

- Add a history entry model and file-backed history store.
- Support add, list recent, get by id, delete by id, clear, max-entry retention, and disabled-history behavior.
- Record only text/result metadata; do not store screenshots, OCR images, secrets, or provider request payloads.
- Add unit tests for add/list/delete/clear/retention/disabled/malformed history file.

Round 4 - Settings UI integration:

- Add lightweight settings controls to the existing PySide6 shell.
- Include source/target language, provider selection/order, provider endpoint/env-var-name fields, timeout/retry controls, OpenAI/DeepL option fields where practical, history enabled, max entries, and a save/apply path.
- Keep controls compact; do not redesign the whole shell.
- Add presenter/service tests and an offscreen smoke path where feasible.

Round 5 - History UI integration:

- Add lightweight history controls to review recent successful translations.
- Support copy result, delete entry, clear all, and disabled-history messaging.
- Record successful clipboard and screen translations through the history service when enabled.
- Add tests or offscreen smoke for add/display/copy/delete/clear.

Round 6 - Privacy docs, final validation, and P5 handoff:

- Document local data path, config file contents, history file contents, disable/clear behavior, and secret-handling rules.
- Update README, development docs, phase plan, and smoke checklist.
- Create `docs/p5_final_validation_report.md`.
- Create `docs/p5_to_p6_handoff.md`.
- Mark `docs/p5_todo.md` complete.
- Run full validation, `git diff --check`, CLI bootstrap checks, storage boundary scans, and UI smoke where feasible.
- Commit and push final P5 state.

## 8. Validation Matrix

Required P5 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- Config storage tests for defaults, save/load, malformed file, migration, and secret exclusion.
- History storage tests for add/list/delete/clear/retention/disabled behavior.
- UI presenter/offscreen smoke or documented manual smoke for settings and history controls.
- Boundary scan showing no checked-in `.env`, generated config/history files, local secrets, or user data.

Expected automated coverage:

- App config default compatibility with P4 provider runtime config.
- File-backed config load/save with temp directories.
- Settings update service behavior.
- History entry serialization/deserialization and retention.
- History disabled behavior.
- Clipboard and screen successful translation recording when history is enabled.
- Existing provider, clipboard, screen, and OCR tests still pass.

No P5 validation may require:

- Real API credentials.
- Real network access.
- OCR model downloads.
- PyInstaller packaging.
- Browser extension runtime.
- Persistent writes to real user data directories during automated tests.

## 9. PASS Criteria

P5 passes when:

- Settings persist across app restart using local file-backed storage.
- Provider selection/order, language defaults, runtime provider options, and UI/history preferences are persisted without secret values.
- Recent translation history can be enabled/disabled, listed, copied, deleted, cleared, and retention-limited.
- Clipboard and screen flows still go through `TranslationPipeline`.
- Storage and history services are testable without PySide6.
- Automated tests use temp storage and no network/API keys.
- Privacy docs explain local data paths, stored fields, history clearing, and secret boundaries.
- Final P5 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P5 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Settings persistence evidence:
- History behavior evidence:
- UI smoke evidence:
- Known limitations:
- Deferred scope:
- Architecture notes:
- Dependency changes:
- Secret/privacy handling:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next phase:
```
