# P1 Core Pipeline Foundation Goal Mode Guide

Date: 2026-06-22
Status: execution guide for P1 after accepted P0
Estimated budget: 6 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P1 in goal mode:

```text
Execute SnapLex P1 - Core Pipeline Foundation in 6 conversation rounds.

Required reading before code changes:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_goal_mode_execution_guide.md
- docs/p0_final_validation_report.md
- docs/p0_to_p1_handoff.md
- docs/p1_todo.md
- docs/p1_core_pipeline_goal_guide.md
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

P0 is accepted. Build only the non-UI translation pipeline foundation for P1.

Goal:
Implement the reusable translation pipeline that later clipboard and OCR flows will call. The pipeline must normalize text, select providers from config, support deterministic fake providers, classify expected pipeline/provider errors, support cache hits, support fallback order, and expose async-friendly boundaries without requiring UI, OCR models, clipboard hotkeys, or network credentials.

Rules:
- Stay inside P1 scope. Do not implement clipboard hotkeys, result popup UI, screen capture, OCR adapters, real LibreTranslate/OpenAI/DeepL network calls, history UI, or packaging.
- Every round must include Debug self-check, architecture self-check, validation commands and results, commit hash, push result, next-round target, and whether a buffer round was consumed.
- Validate before commit.
- Commit and push the successful round before moving to the next round.
- If validation, commit, or push fails, stop and report the blocker instead of moving to the next round.
- Keep tests deterministic and no-network.
- Keep UI thin and unchanged unless a docs-only reference needs updating.
```

## 1. Required Context

P0 PASS evidence:

- `docs/p0_final_validation_report.md` has `Status: PASS`.
- P0 used 4 rounds and 0 buffer rounds.
- Current baseline includes Python project metadata, `python -m snaplex`, service/provider/storage contracts, deterministic fakes, initial tests, and project ops validation.
- Current P1 starting points are:
  - `snaplex/services/text.py`
  - `snaplex/services/translation_service.py`
  - `snaplex/providers/base.py`
  - `snaplex/providers/fake.py`
  - `snaplex/storage/config.py`
  - `tests/test_text.py`
  - `tests/test_fake_provider.py`
  - `tests/test_config.py`

P1 must turn the simple P0 translation service into a reusable, non-UI pipeline for later P2 clipboard and P3 OCR flows.

## 2. Scope

P1 must complete:

- Text normalization for repeated whitespace, empty input, and language-safe line handling.
- Stable pipeline request/response models where useful.
- Provider error taxonomy for empty input, provider failure, timeout, unsupported language, stale result, cache miss/hit behavior, and fallback exhaustion.
- Provider registry and config-driven provider selection.
- Deterministic fake providers for success, failure, timeout, unsupported language, stale result, and fallback-order tests.
- Translation cache keying and in-memory cache.
- Pipeline orchestration around normalization, provider selection, cache, fallback, and error mapping.
- Async-friendly boundary for later PySide6 callers. Prefer a small standard-library-friendly async wrapper or executor boundary over introducing heavy async frameworks.
- Unit tests that run without network or credentials.
- README and handoff docs updates that describe the P1 pipeline.

## 3. Non-Scope

Do not implement in P1:

- Clipboard hotkeys, clipboard workflow UI, or popup UX. These belong to P2.
- Screen capture, region overlay, OCR adapters, or image fixtures beyond fake tests. These belong to P3.
- Real LibreTranslate, OpenAI, or DeepL HTTP adapters. These belong to P4.
- Persistent history, settings UI, file-backed config migration, or privacy UI. These belong to P5.
- PyInstaller packaging. This belongs to P6.
- Browser extension, AI summary, or multilingual UX expansion. These belong to P7.

## 4. Architecture Boundaries

Hard constraints:

- UI must not own provider selection, fallback, cache, normalization, timeout, or error mapping.
- `providers/` owns provider contracts and concrete provider fakes/adapters.
- `services/translation_service.py` may orchestrate translation, but provider registry, cache, and errors should remain explicit and testable.
- `storage/config.py` owns config models/defaults; P1 may extend config for provider order or translation defaults but must not add persistent file storage yet.
- Tests must use fake providers and must not call external services.
- API keys and local credentials must not appear in source, tests, docs examples, or committed files.
- P1 should make P2 easier by exposing simple sync and async-friendly pipeline calls.

## 5. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P1 Core Pipeline Foundation
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
- Any scope expansion must be explicitly approved by the architect/PM before implementation.

Debug self-check:

- Can the current change be explained by the smallest relevant translation pipeline fixture?
- Can failures be localized to normalization, config, registry, cache, provider contract, orchestration, async boundary, or docs?
- Are success, empty input, provider failure, timeout, unsupported language, cache hit, cache miss, stale result, and fallback exhaustion covered where relevant?
- If async behavior changed, is it deterministic and testable without a running UI?
- If config changed, are defaults and invalid-provider states covered?

Architecture self-check:

- Does provider selection remain outside UI?
- Does the provider contract stay stable enough for P4 real adapters?
- Are cache keys independent of provider runtime objects and credentials?
- Are config defaults separated from runtime provider instances?
- Did this round avoid pulling P2-P7 scope into P1?
- Are generated outputs, virtual environments, caches, and unrelated files left out of git?

## 6. Round Plan

Round 1 - Normalize input and define error contracts:

- Expand text normalization behavior.
- Define pipeline/provider error classes or result statuses.
- Add tests for empty input, whitespace, language-safe line handling, and error construction.
- Validate with project ops wrapper.

Round 2 - Provider registry and deterministic fake providers:

- Add provider registry or equivalent explicit selection boundary.
- Support config-driven provider selection and unknown provider errors.
- Add fake providers for success, failure, timeout, unsupported language, and stale result scenarios.
- Add tests for provider lookup and deterministic fake behavior.

Round 3 - Pipeline orchestration:

- Expand `TranslationService` or introduce a small pipeline object that uses config, registry, normalization, provider calls, and error mapping.
- Preserve a simple call surface for later clipboard/OCR callers.
- Add tests for successful translation, empty input, provider errors, unsupported language, and fallback exhaustion without cache concerns.

Round 4 - Cache and fallback behavior:

- Add cache key model and in-memory cache.
- Integrate cache lookup/write into the pipeline.
- Add fallback provider order.
- Add tests for cache hit, cache miss, provider fallback order, and no-cache-on-failure behavior.

Round 5 - Async-friendly boundary and hardening buffer:

- Add async-friendly wrapper or executor boundary for later UI calls.
- Add timeout behavior using deterministic fake providers.
- Harden edge cases found in rounds 1-4.
- Consume this round as buffer only if previous rounds exposed blocking design issues; otherwise use it for tests and docs polish.

Round 6 - Final validation, docs, and P1 handoff:

- Update README, `docs/p1_todo.md`, and create a P1 final validation report.
- Create a P1-to-P2 handoff with exact entry points for clipboard UI work.
- Run full validation.
- Commit and push final P1 state.

## 7. Validation Matrix

Required P1 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`

Expected automated coverage:

- Normalization tests.
- Provider registry tests.
- Fake provider scenario tests.
- Pipeline success and empty-input tests.
- Provider failure, timeout, unsupported-language, stale-result, and fallback-exhaustion tests.
- Cache key, cache hit, cache miss, and fallback-order tests.
- Async-friendly boundary tests that do not require PySide6.
- Config default and unknown provider tests.

No P1 validation may require:

- Network access.
- API keys.
- PySide6 installation.
- PaddleOCR installation.
- Screen capture permissions.

## 8. PASS Criteria

P1 passes when:

- The translation pipeline works without UI and without network.
- Provider registry and config-driven provider selection are implemented and tested.
- Deterministic fake providers cover success, failure, timeout, unsupported language, stale result, and fallback order.
- Cache keying and in-memory cache are implemented and tested.
- Pipeline tests cover empty input, provider failure, timeout, fallback, cache hit, cache miss, unsupported language, stale result, and fallback exhaustion.
- An async-friendly boundary exists for later PySide6 callers and is tested without launching UI.
- README and handoff docs tell P2 where to call the pipeline.
- Full project validation passes.
- Final P1 commit is pushed to `origin/main`.

## 9. Final Report Template

```text
P1 final report:
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

