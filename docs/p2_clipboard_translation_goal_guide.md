# P2 Clipboard Translation MVP Goal Mode Guide

Date: 2026-06-22
Status: execution guide for P2 after accepted P1
Estimated budget: 8 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P2 in goal mode:

```text
Execute SnapLex P2 - Clipboard Translation MVP in 8 conversation rounds.

Required reading before code changes:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_goal_mode_execution_guide.md
- docs/p1_final_validation_report.md
- docs/p1_to_p2_handoff.md
- docs/p2_todo.md
- docs/p2_clipboard_translation_goal_guide.md
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

P1 is accepted. Build the clipboard-to-popup desktop MVP on top of the P1 translation pipeline.

Goal:
Deliver a usable PySide6 clipboard translation flow: a small always-on-top SnapLex widget can trigger clipboard translation, the app reads clipboard text, calls the P1 TranslationPipeline without duplicating provider/cache/fallback logic, and displays source text, translated text, loading, retry, copy result, and user-friendly error states in a popup or result view.

Rules:
- Stay inside P2 scope. Do not implement screen capture, OCR adapters, real LibreTranslate/OpenAI/DeepL network calls, persistent history, PyInstaller packaging, browser extension work, or AI summary.
- UI must call the P1 pipeline; UI must not call provider instances directly.
- Every round must include Debug self-check, architecture self-check, validation commands and results, commit hash, push result, next-round target, and whether a buffer round was consumed.
- Validate before commit.
- Commit and push the successful round before moving to the next round.
- If validation, commit, or push fails, stop and report the blocker instead of moving to the next round.
- Tests must remain deterministic. Use fake clipboard and fake pipeline/provider fixtures for automated tests.
```

## 1. Required Context

P1 PASS evidence:

- `docs/p1_final_validation_report.md` has `Status: PASS`.
- P1 used 6 rounds and 0 buffer rounds.
- P1 delivered `TranslationPipeline.translate_text(...)`, `TranslationPipeline.translate_text_async(...)`, config-driven provider selection, fallback, cache, deterministic fake providers, and expected translation errors.
- P2 handoff is `docs/p1_to_p2_handoff.md`.

P2 should create the first user-facing vertical slice for selected-text translation, while preserving the P1 pipeline as the source of truth for translation behavior.

## 2. Scope

P2 must complete:

- Floating always-on-top PySide6 widget with a clipboard translate action.
- Clipboard service implementation suitable for the desktop flow, plus fake clipboard service tests.
- Result popup or result view with source text, translated text, provider name where useful, copy result, retry, loading, and error states.
- UI orchestration that calls `TranslationPipeline.translate_text_async(...)` or an equivalent non-blocking boundary.
- User-friendly mapping for empty clipboard, unknown provider, provider timeout, fallback exhaustion, and generic provider failure.
- Deterministic UI/service tests that do not require network access or real providers.
- Windows manual smoke checklist for launch, clipboard translate, retry, copy result, and no-GUI fallback.
- Documentation updates showing how to run the P2 clipboard MVP.

## 3. Non-Scope

Do not implement in P2:

- Screen capture, region overlay, OCR adapter, image OCR fixtures, or OCR result flow. These belong to P3.
- Real LibreTranslate, OpenAI, or DeepL HTTP adapters. These belong to P4.
- Persistent settings/history storage, migrations, or history UI. These belong to P5.
- PyInstaller packaging. This belongs to P6.
- Browser extension, AI summary, or post-MVP expansion. These belong to P7.
- Complex global hotkey behavior if it destabilizes the MVP. Investigate and implement only if stable within the P2 budget; otherwise document it as deferred.

## 4. Architecture Boundaries

Hard constraints:

- UI owns presentation state and user actions only.
- Clipboard access stays behind `ClipboardService` or a P2-specific adapter with a matching test double.
- Translation, provider selection, fallback, cache, normalization, and error mapping stay in the P1 pipeline/service layer.
- Widgets must not import concrete provider classes except test fakes inside tests.
- Error-to-message mapping may live in a UI presenter/view-model layer, not directly inside provider or cache code.
- P2 can add lightweight UI state/presenter classes if that keeps widgets thin and testable.
- Tests must not require API keys, network access, PaddleOCR, screen capture permissions, or packaged binaries.

## 5. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P2 Clipboard Translation MVP
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
- Any P2 scope expansion must be explicitly approved by the architect/PM before implementation.

Debug self-check:

- Can the current change be explained by the smallest relevant clipboard translation workflow?
- Can failures be localized to widget, presenter/state, clipboard service, pipeline call, error mapping, or docs?
- Are success, empty clipboard, provider failure, timeout, fallback exhaustion, unknown provider, retry, copy result, and cancellation/close states covered where relevant?
- If UI changed, was a repeatable manual smoke path added or updated?
- If async UI behavior changed, can it be tested without a real network provider?

Architecture self-check:

- Does UI call the pipeline instead of provider instances?
- Does clipboard behavior remain separate from translation behavior?
- Are UI messages/presentation state separate from provider/cache/config semantics?
- Did this round avoid pulling P3-P7 scope into P2?
- Are generated outputs, virtual environments, caches, screenshots, and unrelated files left out of git?

## 6. Round Plan

Round 1 - Clipboard action and UI state skeleton:

- Define a minimal clipboard translation state/presenter boundary.
- Add widget action wiring that can call an injected fake pipeline or presenter.
- Keep actual provider/cache behavior out of widgets.
- Add tests for initial UI/presenter state where feasible.

Round 2 - Result popup or result view:

- Add source/translated text display.
- Add loading, success, empty, and generic error states.
- Add copy result and close behavior at the state or widget boundary.
- Add tests for presenter/state transitions.

Round 3 - Clipboard service integration:

- Add a concrete desktop clipboard service or Qt clipboard adapter.
- Keep an in-memory/fake clipboard for automated tests.
- Add empty clipboard handling.
- Add tests for clipboard read/write and empty text behavior.

Round 4 - Pipeline integration:

- Wire clipboard text into `TranslationPipeline.translate_text_async(...)`.
- Map successful pipeline responses into result state.
- Keep fake provider/fake pipeline paths for deterministic tests.
- Add integration tests for clipboard -> pipeline -> result state.

Round 5 - Error, retry, and copy hardening:

- Map `FallbackExhaustedError`, `UnknownTranslationProviderError`, provider timeout, unsupported language, and stale result into user-friendly UI states.
- Implement retry using the last clipboard/source text where appropriate.
- Ensure failed translations are not copied as success.
- Add tests for error mapping and retry.

Round 6 - Hotkey investigation and optional implementation:

- Investigate a Windows-friendly hotkey path.
- Implement only if it is stable, testable, and does not jeopardize P2.
- If deferred, document the decision and keep manual trigger polished.
- Add smoke notes for whichever path is accepted.

Round 7 - UI polish and Windows smoke:

- Polish sizing, focus, always-on-top behavior, and no-GUI fallback.
- Run/manual-record Windows smoke for launch, translate, retry, copy, close, and fallback states.
- Update `docs/windows_smoke_checklist.md`.

Round 8 - Final validation, docs, and P2 handoff:

- Update README and development docs with P2 usage.
- Create `docs/p2_final_validation_report.md`.
- Create `docs/p2_to_p3_handoff.md` with exact entry points for screen capture/OCR work.
- Run full validation and P2 smoke checks.
- Commit and push final P2 state.

## 7. Validation Matrix

Required P2 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- `python -m snaplex` in an environment with PySide6 installed, for manual GUI smoke.

Expected automated coverage:

- Clipboard service tests with fake/in-memory clipboard.
- UI presenter/state tests for loading, success, empty clipboard, error, retry, copy result, and close.
- Pipeline integration tests using fake providers or fake pipeline.
- Error mapping tests for fallback exhaustion, timeout, unknown provider, unsupported language, stale result, and generic provider failure.
- No-network test run.

No P2 validation may require:

- Real translation API credentials.
- Network access.
- PaddleOCR installation.
- Screen capture permissions.
- PyInstaller packaging.

## 8. PASS Criteria

P2 passes when:

- A user can launch the desktop shell and trigger clipboard translation.
- Clipboard text flows through the P1 pipeline into a visible result popup/view.
- Fake provider mode works offline.
- Empty clipboard, timeout, provider failure, unknown provider, and fallback exhaustion are visible as user-friendly states.
- Result copy and retry work in the accepted UI path.
- UI code does not duplicate provider selection, fallback, cache, normalization, or provider error semantics.
- Automated validation passes.
- Windows manual smoke evidence is recorded.
- README and handoff docs tell P3 where to integrate screen capture/OCR.
- Final P2 commit is pushed to `origin/main`.

## 9. Final Report Template

```text
P2 final report:
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

