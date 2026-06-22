# P6 Packaging and Release Readiness Goal Mode Guide

Date: 2026-06-22
Status: execution guide for P6 after accepted P5
Estimated budget: 7 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P6 in goal mode:

```text
Execute SnapLex P6 - Packaging and Release Readiness in 7 conversation rounds.

Required reading before code changes:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_goal_mode_execution_guide.md
- docs/p5_final_validation_report.md
- docs/p5_to_p6_handoff.md
- docs/p5_privacy_and_storage.md
- docs/p6_todo.md
- docs/p6_packaging_release_goal_guide.md
- docs/windows_smoke_checklist.md
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

P5 is accepted. Package the Windows MVP and make release validation repeatable.

Goal:
Create a reproducible Windows packaging path for SnapLex, smoke-test the packaged app, and document release/troubleshooting steps without committing generated binaries, build folders, local user data, OCR model caches, provider secrets, or packaged artifacts.

Rules:
- Stay inside P6 scope. Do not implement browser extension work, AI summary, cloud sync, accounts, keychain integration, global hotkeys, provider rewrites, or new product features.
- Packaging must preserve accepted runtime boundaries: UI calls services, services own settings/history/provider/capture/OCR rules, local data stays outside packaged resources.
- Do not store provider API key values in config, package resources, logs, or release docs.
- Automated tests must remain deterministic and no-network.
- Every round must include Debug self-check, architecture self-check, validation commands and results, commit hash, push result, next-round target, and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to the next round.
```

## 1. Required Context

P5 PASS evidence:

- `docs/p5_final_validation_report.md` is planner-accepted.
- P5 used 6 rounds and 0 buffer rounds.
- P5 delivered JSON settings persistence, local app data path handling, history storage, settings/history services, settings/history presenters, lightweight PySide6 settings/history dialogs, and privacy docs.
- P5 handoff is `docs/p5_to_p6_handoff.md`.

P6 must preserve these accepted boundaries:

- Clipboard flow: `ClipboardService -> TranslationPipeline -> result presenter -> optional HistoryService`.
- Screen flow: `RegionSelector -> CaptureService -> OcrService -> TranslationPipeline -> result presenter -> optional HistoryService`.
- Settings flow: `SettingsPresenter -> SettingsService -> ConfigStore`.
- History flow: `HistoryPresenter -> HistoryService -> HistoryStore`.
- Provider secrets remain environment values only.
- Config/history files live in local app data, not inside packaged resources.

## 2. Scope

P6 must complete:

- Packaging metadata and a repeatable Windows build command.
- PyInstaller spec or equivalent packaging entry for the SnapLex GUI/CLI entry point.
- If a `.spec` file is tracked, update `.gitignore` deliberately to allow only the chosen spec path while keeping generated build artifacts ignored.
- Optional packaging extras/development dependency documentation for PyInstaller.
- Data-file and hidden-import decisions for PySide6, optional `mss`, optional PaddleOCR, and SnapLex package modules.
- Clear handling for optional capture/OCR dependencies: include, exclude with docs, or provide separate build variants.
- Packaged no-GUI/bootstrap launch smoke.
- Packaged GUI launch smoke with fake provider and no credentials.
- Packaged clipboard flow smoke.
- Packaged settings persistence and history clear smoke using a test app data directory.
- Packaged screen flow smoke where GUI/capture/OCR dependencies are available, or a documented limitation if they are not included.
- Release checklist, troubleshooting docs, and versioning convention.
- P6 final validation report and P6-to-P7 handoff.

## 3. Non-Scope

Do not implement in P6:

- Browser extension, AI summary, or post-MVP expansion. These belong to P7.
- Global hotkeys.
- Cloud sync, accounts, keychain integration, encryption, or remote history.
- Provider rewrites or new provider adapters.
- OCR/capture coordinate rewrites beyond packaging fixes required to launch.
- UI redesign beyond packaging smoke fixes.
- Committing packaged binaries, installers, `dist/`, `build/`, virtual environments, OCR model caches, generated config/history files, `.env`, screenshots, or local user data.

## 4. Planner Decisions And Assumptions

- Prefer PyInstaller for the Windows MVP because it is the planned stack.
- Use a tracked packaging entry under a controlled path such as `packaging/` or `scripts/`. Do not track generated binaries.
- Because `.gitignore` currently ignores `*.spec`, P6 must either add a narrow exception for the chosen spec file or use an equivalent tracked build script/config that generates the spec during build.
- Fake provider remains the default packaged smoke path.
- Real provider smoke is optional and local-credential dependent.
- OCR packaging may be heavyweight. It is acceptable to document OCR/capture optional dependency limitations if a full OCR-included package is not stable within P6.
- Use `SNAPLEX_APP_DATA_DIR` for packaged smoke so validation does not write to real user data directories.
- Release artifacts can be produced locally for smoke but must not be committed.

## 5. Architecture Boundaries

Hard constraints:

- Packaging scripts may wire entry points and resource collection, but must not own provider, settings, history, OCR, capture, or UI business rules.
- Local config/history files must continue using `default_app_data_dir(...)` and must remain outside packaged executable resources.
- Provider API key values must not be embedded into the executable, spec, docs, or smoke logs.
- Optional dependencies must be documented clearly so users know which build supports GUI, capture, and OCR.
- Tests and validation must not depend on real provider network calls.
- Generated outputs and user data must remain out of git.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P6 Packaging and Release Readiness
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
- Any P6 scope expansion must be explicitly approved by the architect/PM before implementation.

Debug self-check:

- Can the current change be explained by the smallest relevant packaging workflow?
- Can failures be localized to metadata, dependency restore, PyInstaller/spec, hidden imports, local data paths, GUI launch, provider config, capture/OCR extras, or docs?
- Are clean build, missing optional dependency, no credentials, local data path override, launch failure, and smoke failure states covered where relevant?
- If UI packaging changed, was a repeatable packaged smoke path added or documented?
- If generated outputs were created, are they ignored and left uncommitted?

Architecture self-check:

- Does packaging preserve service/storage/provider/UI boundaries?
- Did packaging avoid embedding secrets or local user data?
- Are config/history files still outside packaged resources?
- Did this round avoid pulling P7 scope into P6?
- Are unrelated files, build outputs, packaged artifacts, model caches, screenshots, and user changes left alone?

## 7. Round Plan

Round 1 - Packaging metadata and build entry:

- Add packaging docs/metadata and a repeatable Windows build command.
- Decide PyInstaller dependency placement, such as a packaging extra, a docs-only install command, or a build requirements file.
- Add a packaging script or command wrapper that can be run locally.
- Keep generated build outputs ignored.

Round 2 - PyInstaller spec or equivalent config:

- Add a controlled PyInstaller spec or equivalent tracked build entry.
- If tracking a `.spec`, update `.gitignore` with a narrow exception for that path.
- Configure app name, entry point, console/window behavior, and basic hidden imports.
- Validate the build command can run or document the exact local blocker.

Round 3 - Dependency and asset inclusion strategy:

- Decide inclusion/exclusion for PySide6, optional `mss`, optional PaddleOCR, and OCR model assets.
- Keep app bootstrap working when capture/OCR extras are absent.
- Ensure local config/history path handling does not write into packaged resources.
- Add troubleshooting docs for missing GUI/capture/OCR/provider config.

Round 4 - Packaged launch smoke:

- Build the package in a local generated output directory.
- Run packaged version/no-GUI/bootstrap smoke where the package supports it.
- Run packaged GUI launch smoke with fake provider and `SNAPLEX_APP_DATA_DIR` pointing to a test directory.
- Document exact commands, output paths, and cleanup steps.

Round 5 - Packaged workflow smoke:

- Smoke packaged clipboard translation, settings persistence, history record/list/copy/delete/clear, and provider fallback with fake/default settings.
- Smoke packaged screen flow where optional capture/OCR dependencies are available.
- If visible screen/OCR smoke is not feasible, document the limitation and keep fake/injected or manual smoke notes clear.

Round 6 - Release docs and troubleshooting:

- Update README, windows smoke checklist, and packaging docs with setup, build, smoke, troubleshooting, and cleanup steps.
- Add a release checklist covering clean tree, validation, package build, smoke, artifact location, artifact exclusion from git, known limitations, and version.
- Document provider secret handling and local data handling in packaged builds.

Round 7 - Final validation and P6 handoff:

- Create `docs/p6_final_validation_report.md`.
- Create `docs/p6_to_p7_handoff.md`.
- Mark `docs/p6_todo.md` complete.
- Run full validation, `git diff --check`, CLI bootstrap checks, packaging build/smoke checks when feasible, and artifact boundary scans.
- Commit and push final P6 state.

## 8. Validation Matrix

Required P6 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- Packaging build command or documented blocker with a concrete remediation path.
- Packaged launch smoke when a package is produced.
- Packaged clipboard/settings/history smoke when a package is produced.
- Boundary scan showing no committed `build/`, `dist/`, packaged binaries, generated local config/history, `.env`, provider keys, OCR model caches, screenshots, or local app data.

Expected automated or scripted coverage:

- Existing 182-test suite remains green.
- Build command exits successfully in the local environment or records a narrow blocker.
- Packaged app can start without provider credentials.
- `SNAPLEX_APP_DATA_DIR` override works in packaged smoke.
- Generated artifacts are ignored and not staged.

No P6 validation may require:

- Real API credentials.
- Real provider network calls.
- Browser extension runtime.
- AI summary service.
- Cloud sync/accounts.
- Committing generated binaries or OCR model caches.

## 9. PASS Criteria

P6 passes when:

- A repeatable Windows packaging command exists and is documented.
- A PyInstaller spec or equivalent packaging entry is tracked deliberately.
- Generated artifacts remain untracked.
- Packaged app launch is smoked, or a narrow packaging blocker is documented for architect acceptance.
- Clipboard, settings, and history packaged smoke pass when a package is produced.
- Screen/capture/OCR packaged behavior is either smoked or clearly documented with optional dependency limitations.
- README and troubleshooting docs explain install, build, smoke, provider config, local data, and cleanup.
- Final P6 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P6 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Packaging command:
- Packaging artifact status:
- Packaged smoke evidence:
- Known limitations:
- Deferred scope:
- Architecture notes:
- Dependency changes:
- Secret/local-data handling:
- Artifact exclusion evidence:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next phase:
```
