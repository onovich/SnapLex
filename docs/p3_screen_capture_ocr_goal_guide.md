# P3 Screen Capture and OCR MVP Goal Mode Guide

Date: 2026-06-22
Status: execution guide for P3 after accepted P2
Estimated budget: 10 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P3 in goal mode:

```text
Execute SnapLex P3 - Screen Capture and OCR MVP in 10 conversation rounds.

Required reading before code changes:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_goal_mode_execution_guide.md
- docs/p2_final_validation_report.md
- docs/p2_to_p3_handoff.md
- docs/p3_todo.md
- docs/p3_screen_capture_ocr_goal_guide.md
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

P2 is accepted. Build the screen capture and OCR MVP on top of the P1 translation pipeline and P2 result-flow pattern.

Goal:
Deliver a screen-translation vertical slice: the SnapLex shell exposes a screen translation action, the user can select or provide a screen region, capture that region, extract text through an OCR service boundary, translate the OCR text through TranslationPipeline, and render the result through the existing result view/presenter pattern. The app must keep launch responsive through lazy OCR loading and must handle capture cancel, capture failure, OCR failure, empty OCR result, and retry.

Rules:
- Stay inside P3 scope. Do not implement real translation provider HTTP adapters, persistent history/settings UI, PyInstaller packaging, browser extension work, AI summary, or global hotkeys.
- Capture logic must stay behind CaptureService. OCR logic must stay behind OcrService. Translation must stay behind TranslationPipeline.
- Do not make automated tests require screen permissions, PaddleOCR model downloads, network access, API keys, or visible desktop interaction.
- Real OCR/PaddleOCR support must be optional and lazy. If the dependency/model is unavailable, surface a clear unavailable state rather than crashing or slowing app startup.
- Every round must include Debug self-check, architecture self-check, validation commands and results, commit hash, push result, next-round target, and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to the next round.
```

## 1. Required Context

P2 PASS evidence:

- `docs/p2_final_validation_report.md` has been planner-accepted.
- P2 used 8 rounds and 0 buffer rounds.
- P2 delivered a PySide6 shell, clipboard presenter, clipboard service adapter, result states, copy, retry, close, error mapping, and offscreen GUI smoke.
- P2 handoff is `docs/p2_to_p3_handoff.md`.

P3 must reuse these accepted boundaries:

- `TranslationPipeline.translate_text_async(...)` for translation.
- `ClipboardTranslationPresenter` / result-state pattern for loading, success, retry, copy, close, and error states.
- `CaptureService`, `ScreenRegion`, and `CapturedImage` from `snaplex/services/capture_service.py`.
- `OcrService`, `OcrResult`, and `FakeOcrService` from `snaplex/services/ocr_service.py`.

## 2. Scope

P3 must complete:

- Screen translation action in the PySide6 shell.
- Capture presenter/service path that can run with injected fake capture/OCR services.
- Transparent or minimal region-selection overlay with cancel behavior.
- Screenshot capture backend via `mss` or a conservative equivalent adapter behind `CaptureService`.
- OCR service adapter boundary with fake OCR tests and optional PaddleOCR-capable lazy adapter.
- Capture -> OCR -> TranslationPipeline -> result view flow.
- Empty OCR result, OCR failure, capture failure, region cancel, retry, copy, and close states.
- Windows smoke notes for single-monitor capture, cancel, OCR success, empty OCR result, OCR failure, and DPI/multi-monitor limitations.
- P3 final validation report and P3-to-P4 handoff.

## 3. Non-Scope

Do not implement in P3:

- Real LibreTranslate, OpenAI, or DeepL HTTP adapters. These belong to P4.
- Persistent settings/history storage, migrations, or history UI. These belong to P5.
- PyInstaller packaging. This belongs to P6.
- Browser extension, AI summary, or post-MVP expansion. These belong to P7.
- Global hotkeys. Keep the manual screen translation action as the accepted trigger unless the architect explicitly expands scope.
- Automatic OCR model download during app startup.

## 4. Architecture Boundaries

Hard constraints:

- UI owns user actions and rendering only.
- Capture geometry, screenshot implementation, DPI conversion, and cancel/failure states must stay outside translation providers.
- OCR adapters must implement `OcrService` and must not call translation providers.
- Screen translation orchestration may use a presenter/service layer, but widgets must not own capture/OCR/translation rules directly.
- Result-state behavior should be reused or extracted from the P2 presenter pattern instead of duplicating a second incompatible state machine.
- Tests must use fake capture/OCR and fake pipeline/provider fixtures.
- Optional real capture/OCR dependencies must be isolated so no-GUI and unit tests still pass without them.

## 5. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P3 Screen Capture and OCR MVP
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
- Any P3 scope expansion must be explicitly approved by the architect/PM before implementation.

Debug self-check:

- Can the current change be explained by the smallest relevant screen translation workflow?
- Can failures be localized to shell action, region selection, capture service, OCR service, translation pipeline, result presenter, or docs?
- Are success, cancel, invalid region, capture failure, OCR failure, empty OCR result, provider failure, retry, copy, and close states covered where relevant?
- If UI changed, was a repeatable offscreen or manual smoke path added?
- If optional dependencies changed, do tests and app bootstrap still pass without them?

Architecture self-check:

- Does UI call capture/OCR/translation services instead of owning their rules?
- Does OCR stay separate from translation/provider selection?
- Does capture geometry stay separate from overlay rendering?
- Did this round avoid pulling P4-P7 scope into P3?
- Are generated screenshots, model caches, virtual environments, and unrelated files left out of git?

## 6. Round Plan

Round 1 - Screen action and presenter skeleton:

- Add a screen translation action to the shell.
- Add a screen translation presenter/service skeleton with injected fake capture, OCR, and pipeline.
- Reuse or extract common result-state behavior from the P2 presenter where it reduces duplication.
- Add tests for initial state, loading, success path with fake OCR text, and close.

Round 2 - Capture geometry and fake capture integration:

- Strengthen `ScreenRegion` and capture geometry tests.
- Add screen translation flow using `FakeCaptureService`.
- Add invalid region and capture failure states.
- Keep real screenshot backend deferred until fake path is stable.

Round 3 - Region selection overlay:

- Add transparent or minimal region-selection overlay UI.
- Support confirm and cancel behavior.
- Add unit/presenter tests for selection result and cancel state where feasible.
- Add offscreen smoke or documented manual smoke path.

Round 4 - Screenshot backend:

- Add `mss` or conservative screenshot adapter behind `CaptureService`.
- Keep dependency optional and lazy.
- Add tests around adapter construction/error mapping without requiring real screen permissions.
- Document single-monitor and DPI assumptions.

Round 5 - OCR service adapter and fake OCR hardening:

- Strengthen `OcrService` behavior and error taxonomy if needed.
- Add fake OCR scenarios for success, empty result, and failure.
- Add optional PaddleOCR-capable adapter with lazy import and clear unavailable state.
- Automated tests must not download OCR models.

Round 6 - Capture/OCR/pipeline integration:

- Wire capture image -> OCR text -> `TranslationPipeline.translate_text_async(...)`.
- Reuse result view for translated OCR text.
- Add integration tests with fake capture, fake OCR, and fake/fallback pipeline.

Round 7 - UI error, retry, copy, and cancel behavior:

- Map capture failure, OCR failure, empty OCR result, region cancel, and translation errors into user-friendly states.
- Ensure retry reuses the selected region or asks for a new region according to the chosen UX.
- Ensure copy writes only successful translated text.

Round 8 - OCR lazy-loading and performance hardening:

- Verify app launch remains responsive without OCR model initialization.
- Add tests or smoke notes for missing PaddleOCR dependency/model.
- Consume this as buffer if earlier capture/overlay work needs stabilization; otherwise use it for hardening and docs.

Round 9 - Windows smoke and DPI/multi-monitor notes:

- Run or document Windows smoke for single-monitor capture, cancel, OCR success, OCR empty result, OCR failure, and visible result rendering.
- Record DPI and multi-monitor limitations.
- Update `docs/windows_smoke_checklist.md`.

Round 10 - Final validation, docs, and P3 handoff:

- Update README and development docs with P3 usage.
- Create `docs/p3_final_validation_report.md`.
- Create `docs/p3_to_p4_handoff.md`.
- Mark `docs/p3_todo.md` complete.
- Run full validation and P3 smoke checks.
- Commit and push final P3 state.

## 7. Validation Matrix

Required P3 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- PySide6 offscreen smoke for shell launch and injected fake capture/OCR translation flow.
- Windows manual smoke notes for region selection/capture when the overlay exists.

Expected automated coverage:

- Capture geometry and fake capture tests.
- Region selection presenter/overlay tests where feasible.
- Fake OCR success, empty result, and failure tests.
- Screen translation presenter/service tests for loading, success, cancel, empty OCR, capture failure, OCR failure, retry, copy, and close.
- Integration tests using fake capture + fake OCR + P1 pipeline.
- Missing optional dependency tests for real capture/OCR adapters.

No P3 validation may require:

- Real translation API credentials.
- Network access.
- Automatic PaddleOCR model downloads.
- PyInstaller packaging.
- Persistent local history/settings.

## 8. PASS Criteria

P3 passes when:

- A user can trigger screen translation from the desktop shell.
- The accepted path supports region selection or a clearly documented equivalent region input.
- Captured image flows through `OcrService`, then through `TranslationPipeline`, then into the existing result view.
- Fake capture/OCR mode works offline and is covered by tests.
- Real capture adapter exists behind `CaptureService` and handles unavailable/permission failures cleanly.
- OCR adapter boundary exists, lazy-loads optional real OCR dependencies, and handles unavailable model/dependency states cleanly.
- Cancel, invalid region, capture failure, OCR failure, empty OCR result, provider failure, retry, copy, and close states are covered.
- App launch remains responsive without initializing OCR models.
- Automated validation passes.
- Windows smoke evidence and limitations are recorded.
- Final P3 commit is pushed to `origin/main`.

## 9. Final Report Template

```text
P3 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Manual smoke evidence:
- Known limitations:
- Deferred scope:
- Architecture notes:
- Dependency changes:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next phase:
```

