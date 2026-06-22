# P4 Provider Hardening and Fallbacks Goal Mode Guide

Date: 2026-06-22
Status: execution guide for P4 after accepted P3
Estimated budget: 7 conversation rounds

## 0. Direct Goal Prompt

Use this prompt to execute P4 in goal mode:

```text
Execute SnapLex P4 - Provider Hardening and Fallbacks in 7 conversation rounds.

Required reading before code changes:
- AGENTS.md
- README.md
- docs/development_plan.md
- docs/phase_plan.md
- docs/p0_p7_goal_mode_execution_guide.md
- docs/p3_final_validation_report.md
- docs/p3_to_p4_handoff.md
- docs/p4_todo.md
- docs/p4_provider_hardening_goal_guide.md
- docs/codex-git-workflow.md
- docs/codex-ops-workflow.md

P3 is accepted. Build real translation-provider hardening on top of the P1 TranslationPipeline and the accepted P2/P3 result flows.

Goal:
Add configurable real provider adapters and robust fallback behavior while preserving fake-provider deterministic validation. Provider adapters must stay behind the existing TranslationProvider contract, credentials must come only from environment variables or ignored local configuration, and automated tests must use mocked HTTP/no-network fixtures.

Rules:
- Stay inside P4 scope. Do not implement persistent settings/history UI, PyInstaller packaging, browser extension work, AI summary, global hotkeys, or OCR/capture rewrites.
- Clipboard and screen widgets must keep calling TranslationPipeline; they must not call provider adapters, HTTP clients, or credentials directly.
- Tests must not call real LibreTranslate, OpenAI, DeepL, or other external endpoints.
- Do not commit API keys, local credentials, generated secrets, or real service responses containing private text.
- Every round must include Debug self-check, architecture self-check, validation commands and results, commit hash, push result, next-round target, and whether a buffer round was consumed.
- Validate before commit. Commit and push the successful round before moving to the next round.
```

## 1. Required Context

P3 PASS evidence:

- `docs/p3_final_validation_report.md` is planner-accepted.
- P3 used 10 rounds and 0 buffer rounds.
- P3 delivered screen translation action, region selection, capture/OCR service boundaries, fake capture/OCR flows, lazy optional `mss` and PaddleOCR adapters, shared result view states, and P3 smoke evidence.
- P3 handoff is `docs/p3_to_p4_handoff.md`.

P4 must reuse these accepted boundaries:

- `snaplex/providers/base.py` owns the `TranslationProvider`, `TranslationRequest`, and `TranslationResponse` contract.
- `snaplex/providers/registry.py` owns provider registration and lookup.
- `snaplex/services/translation_service.py` owns provider iteration, cache use, fallback, and async translation.
- `snaplex/storage/config.py` owns provider selection and language defaults.
- `snaplex/ui/translation_result.py` owns UI-friendly translation error mapping.
- Clipboard and screen flows already consume `TranslationPipeline.translate_text_async(...)`.

## 2. Scope

P4 must complete:

- Provider runtime configuration for real provider endpoints, credentials, timeouts, retry count, and fallback order.
- A small injectable HTTP boundary for provider adapters so tests can mock requests without real network calls.
- LibreTranslate adapter for local/self-hosted development.
- OpenAI adapter behind explicit API-key configuration.
- DeepL adapter behind explicit API-key configuration.
- Missing credential, timeout, HTTP error, malformed response, unsupported language, and provider failure handling.
- Retry and timeout behavior that maps to internal `TranslationError` subclasses.
- Fallback ordering through `TranslationPipeline`, preserving fake mode as the deterministic default.
- Provider configuration docs and an ignored-local-secret workflow, including `.env.example` if useful.
- P4 final validation report and P4-to-P5 handoff.

## 3. Non-Scope

Do not implement in P4:

- Persistent settings/history storage or settings/history UI. These belong to P5.
- PyInstaller packaging or packaged-app smoke. These belong to P6.
- Browser extension, AI summary, or post-MVP expansion. These belong to P7.
- Global hotkeys. Keep manual clipboard/screen actions as accepted triggers.
- OCR model, capture overlay, DPI, or multi-monitor rewrites unless a provider change exposes a direct regression.
- Real-service automated tests, checked-in credentials, or checked-in `.env` files.
- A broad dependency migration. Prefer the standard library plus injected test doubles unless a new dependency is explicitly justified in the round report.

## 4. Planner Decisions And Assumptions

- Default runtime remains `fake`; real providers become available only when explicitly configured.
- Provider credentials are read from environment variables or local ignored files. P4 may add `.env.example`, but not `.env`.
- Use a small internal HTTP client/transport protocol with injected fakes for tests. Prefer `urllib.request` or another standard-library implementation unless the executor documents why a dependency is needed.
- Provider-specific response parsing should stay in provider adapters; fallback, cache, and provider order should stay in `TranslationPipeline`.
- Missing credentials should disable or fail that provider with a clear internal provider error, not crash app bootstrap.
- A real provider smoke is optional and should run only when local credentials/endpoints are present. Absence of credentials must not fail P4 acceptance.

## 5. Architecture Boundaries

Hard constraints:

- UI owns user actions and rendering only.
- Provider adapters own provider-specific URLs, payloads, response parsing, and external error mapping.
- The translation pipeline owns provider iteration, fallback, cache, and async boundaries.
- Config models may name providers and environment keys, but must not store runtime provider objects or secrets.
- Provider health/status reporting must not require UI changes unless it is exposed through existing result/error states.
- Tests must use fake HTTP transports, fake providers, and fake config stores.
- Network errors must become internal `TranslationProviderError` or `TranslationProviderTimeoutError` variants.
- Unsupported language must map to `UnsupportedLanguageError` when provider responses make that clear.

## 6. Per-Round Fixed Workflow

Every round report must include:

```text
Round:
Phase: P4 Provider Hardening and Fallbacks
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
- Any P4 scope expansion must be explicitly approved by the architect/PM before implementation.

Debug self-check:

- Can the current change be explained by the smallest relevant provider workflow?
- Can failures be localized to config loading, provider registry, HTTP transport, provider parsing, pipeline fallback, cache, UI error mapping, or docs?
- Are success, missing credential, timeout, retry exhaustion, HTTP error, malformed response, unsupported language, fallback exhaustion, and fake-provider default states covered where relevant?
- If network behavior changed, are all tests mocked/no-network?
- If config changed, are default, env/local override, and missing-secret states covered?

Architecture self-check:

- Does `TranslationPipeline` remain the provider orchestration source of truth?
- Did UI avoid calling provider adapters or HTTP clients directly?
- Are credential discovery, provider runtime config, provider registration, and user settings separated?
- Did this round avoid pulling P5-P7 scope into P4?
- Are unrelated files, generated outputs, `.env`, secrets, and real provider logs left out of git?

## 7. Round Plan

Round 1 - Provider runtime config and HTTP boundary:

- Extend config/runtime models for provider order, endpoints, credential env names, timeout seconds, and retry count.
- Add a minimal injectable HTTP transport protocol and deterministic fake transport tests.
- Add or refine internal provider errors for missing credentials and HTTP/network failures if needed.
- Preserve fake provider as the default no-credential path.

Round 2 - LibreTranslate adapter:

- Add a LibreTranslate provider adapter behind `TranslationProvider`.
- Support configurable base URL and optional API key.
- Map success, timeout, HTTP error, malformed response, and unsupported language into internal errors.
- Add mocked HTTP tests; no external LibreTranslate call is allowed in tests.

Round 3 - OpenAI adapter:

- Add an OpenAI translation adapter behind explicit `SNAPLEX_OPENAI_API_KEY` style configuration.
- Support configurable model/base URL where feasible without broadening scope.
- Parse success and provider error responses into `TranslationResponse` or internal errors.
- Add mocked HTTP tests for success, missing key, timeout, HTTP error, malformed response, and fallback behavior.

Round 4 - DeepL adapter:

- Add a DeepL provider adapter behind explicit `SNAPLEX_DEEPL_API_KEY` style configuration.
- Support free/pro endpoint configuration where practical.
- Map language and quota/provider failures into existing internal error types.
- Add mocked HTTP tests for success, missing key, timeout, HTTP error, malformed response, and unsupported language.

Round 5 - Fallback, retry, timeout, and registration hardening:

- Wire configured real providers into `create_default_provider_registry(...)` or a dedicated factory without breaking fake default behavior.
- Verify provider order across fake, LibreTranslate, OpenAI, and DeepL.
- Add retry/timeout behavior at the provider HTTP boundary or clearly justified pipeline boundary.
- Ensure `TranslationPipeline` fallback and UI error mapping remain unchanged for clipboard and screen flows.

Round 6 - Configuration docs and optional real-provider smoke:

- Document environment variables, local ignored secret handling, provider order, timeout/retry defaults, and no-network test rules.
- Add `.env.example` if it helps users configure providers safely.
- Update README, windows smoke checklist, and development docs for provider setup.
- If credentials/endpoints exist locally, run one real provider manual smoke and record it; if not, record that real smoke was skipped because credentials were absent.

Round 7 - Final validation, docs, and P4 handoff:

- Create `docs/p4_final_validation_report.md`.
- Create `docs/p4_to_p5_handoff.md`.
- Mark `docs/p4_todo.md` complete.
- Run full validation, `git diff --check`, CLI bootstrap checks, provider boundary scans, and mocked HTTP test evidence.
- Commit and push final P4 state.

## 8. Validation Matrix

Required P4 validation:

- `C:\Users\Administrator\.codex\skills\project-ops-workflow\scripts\ops\Validate.cmd`
- `git diff --check`
- `python -m snaplex --version`
- `python -m snaplex --no-gui`
- Mocked HTTP tests for LibreTranslate, OpenAI, and DeepL adapters.
- Pipeline fallback tests covering configured provider order and fallback exhaustion.
- Missing credential tests for all API-key providers.
- Boundary scan showing no checked-in secrets and no automated real-network tests.

Expected automated coverage:

- Provider runtime config defaults and override behavior.
- HTTP transport success, timeout, status error, and malformed body handling.
- Provider adapters for success, missing credential, timeout, HTTP error, malformed response, unsupported language where applicable.
- Pipeline fallback across fake and real-provider names using mocked providers/transports.
- UI/result presenter compatibility through existing translation error mapping tests.

No P4 validation may require:

- Real API credentials.
- Real network access.
- OCR model downloads.
- Visible desktop interaction.
- PyInstaller packaging.
- Persistent settings/history storage.

## 9. PASS Criteria

P4 passes when:

- Fake provider remains the default deterministic validation path.
- LibreTranslate, OpenAI, and DeepL adapters exist behind the provider contract or any infeasible adapter is explicitly documented with a narrow blocker accepted by the architect.
- Provider credentials and endpoints are configured only through safe local/env boundaries.
- Missing credentials do not crash app bootstrap.
- Timeout, retry, HTTP error, malformed response, unsupported language, fallback order, and fallback exhaustion are covered by tests.
- Clipboard and screen flows still go through `TranslationPipeline`.
- Automated tests do not call external services.
- README and smoke docs explain how to configure providers and how to skip real-provider smoke when credentials are absent.
- Final P4 commit is pushed to `origin/main`.

## 10. Final Report Template

```text
P4 final report:
- Status:
- Rounds used:
- Buffer rounds consumed:
- Main deliverables:
- Validation commands and results:
- Mocked provider test evidence:
- Optional real-provider smoke:
- Known limitations:
- Deferred scope:
- Architecture notes:
- Dependency changes:
- Secret/config handling:
- Commit hashes:
- Push result:
- Request for architect/PM acceptance:
- Recommended next phase:
```
